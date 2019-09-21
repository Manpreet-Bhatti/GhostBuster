import math
import typing

import matplotlib.path as mpl_path
import numpy as np
import pygame

from PyGE.DisplayMethods.Color import Color, DisplayBase
from PyGE.Globals.GlobalVariable import get_sys_var, new_thread, get_var, set_var
from PyGE.BackgroundTasks import frequency_monitor
from PyGE.Misc.Ticker import Ticker
from PyGE.utils import get_mandatory, rect_a_touch_b, get_optional, point_in_rect, rect_a_in_b, get_surface_center, convert_color


class ObjectBase:
    def __init__(self, screen:pygame.Surface, args: dict, parent):
        """
        This is the object ALL objects MUST inherit from to be used in a room.
        This is the parent of ALL objects.
        :param screen: The screen to draw the object to
        :param args: The dictionary of properties specified in the XML.
        :param parent: The room the object will live in 
        """
        self.screen = screen
        self.args = self.modify_args(args)
        self.parent = parent

        self.angle = 0

        # self.should_center_width = get_mandatory(args, "@x", str) == "c"
        # self.should_center_height = get_mandatory(args, "@y", str) == "c"

        self.locked = get_optional(args, "locked", "false")

        self.screen_w, self.screen_h = self.screen.get_size()

        self.display = Color(screen, (255, 0, 255), 10, 10)
        w, h = self.display.get_size()

        self.w = get_optional(args, "w", None)
        self.h = get_optional(args, "h", None)
        
        if self.w is None:
            self.w = w
            
        if self.h is None:
            self.h = h
            
        self.positional_vars = {}
        self.reload_vars()

        self.x = None
        self.y = None
        self.recalculate_position()

        self.on_screen_cache = True
        self.on_mouse_over_cache = False
        self.deleted = False

        self.ticker = Ticker()
        self.time_delta = self.ticker.tick

        self.states = {}
        self.state = None

        self.x_delta = 0
        self.y_delta = 0

        self.model_type = type(self).__name__

        self.debug_color = get_sys_var("debug-color")

        self.siblings = self.parent.props.array

        self.oncreate()

        self.frequency_monitor_thread = None

        self.zindex = 10

    def reload_vars(self):
        self.positional_vars = {
            "sw": self.screen_w,
            "sh": self.screen_h,
            "cw": self.calculate_center(self.w)[0],
            "ch": self.calculate_center(None, self.h)[1],
            "mw": self.w,
            "mh": self.h
        }

    def recalculate_position(self):
        self.reload_vars()
        self.x = self.evaluate_variables(get_mandatory(self.args, "x", str))
        self.y = self.evaluate_variables(get_mandatory(self.args, "y", str))
        
    def evaluate_variables(self, data:str):
        for key, val in self.positional_vars.items():
            data = data.replace(key, str(val))
        return eval(data)

    def modify_args(self, args:dict):
        """
        This method provides you with onbe final chance to modify the arguements before they are used by the object
        :param args: the current arguement dictionary. Note that items coming from XML will have the "@" sign before the key. Don't worry about this. 
        :return: the modified arguement dictionary.
        """
        return args

    def center_width(self):
        """
        Forces the object to the center of the screen along the x axis
        :return: the new x position
        """
        self.x = (self.screen.get_width() / 2) - (self.w / 2)
        return self.x

    def center_height(self):
        """
        Forces the object to the center of the screen along the y axis
        :return: the new y position
        """
        self.y = (self.screen.get_height() / 2) - (self.h / 2)
        return self.y

    def set_width(self, w:int):
        """
        Sets this object's width
        We strongly recomend you use this method, and not set the value directly, as this allows for calculation updates
        :param w: the new width
        """
        self.w = w
        # if self.should_center_width:
        #     self.center_width()

    def set_height(self, h:int):
        """
        Sets this object's height
        We strongly recomend you use this method, and not set the value directly, as this allows for calculation updates
        :param h: the new height
        """
        self.h = h
        # if self.should_center_height:
        #     self.center_height()

    def set_display_method(self, method:'DisplayBase'):
        """
        Sets the display method of the object
        :param method: The display method
        """
        self.display = method
        self.w, self.h = self.display.get_size()

    @property
    def is_onscreen(self):
        """
        Returns if this object is completly on the screen
        """
        return rect_a_touch_b(self.rect, (0, 0, self.screen_w, self.screen_h))

    @property
    def is_touching_screen(self):
        """
        Returns if this object is completly on the screen
        """
        return rect_a_in_b(self.rect, (0, 0, self.screen_w, self.screen_h))

    @property
    def rect(self):
        """
        Returns the rect representation of the object in the format (x, y, width, height)
        """
        return self.x, self.y, self.w, self.h

    @property
    def point_array(self):
        """
        Returns this object as a point array in the format [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
        """
        return (self.x, self.y), (self.x, self.y + self.h), (self.x + self.w, self.y + self.h), (self.x + self.w, self.y)

    @property
    def polygon(self):
        """
        Returns a polygon representaion of the object (As a MatPlotLib Path object)
        """
        return mpl_path.Path(np.array(self.point_array))

    @property
    def metadata(self):
        """
        Returns this object's metadata (the values which will be written to the XML file)
        """
        return {
            "x": self.x,
            "y": self.y,
            "locked": self.locked
        }

    @property
    def rooms(self):
        """
        Returns a dictionary representation of the rooms in memory
        """
        return self.parent.parent.rooms

    @property
    def object_type(self):
        """
        Gets this object's class name as a string
        """
        return self.__class__.__name__

    def set_zindex(self, zindex):
        """
        Sets this object's zindex. The lower the zindex is, the further back it is drawn. Example: zindex 10 is drawn on top of zindex 1  
        :param zindex: the zindex to use
        """
        self.zindex = zindex

    def get_zindex(self):
        """
        Returns this object's current zindex
        :return: the zindex
        """
        return self.zindex

    def start_frequency_monitor(self):
        """
        Starts the frequency monitoring system. This is a thread which can not be stopped (yet)
        To get the frequency of the primary audio input, use "self.get_var("current_pitch")"
        This is accessable accross all objects, so DO NOT call this more than once!
        """
        self.frequency_monitor_thread = new_thread(frequency_monitor, "fm", True)

    def get_var(self, name):
        """
        Gets a globally set variable
        :param name: the name of the variable
        :return: the value of the variable
        """
        return get_var(name)

    def set_var(self, name, value):
        """
        Sets the value of a global variable
        :param name: the name of the variable
        :param value: the value of the variable
        """
        set_var(name, value)

    def do_if_condition(self, condition:bool, action:callable, args=None):
        """
        Runs the specified function with specified arguements if the specified contition is True
        :param condition: the condition to process
        :param action: the reference to the functon to call if True
        :param args: the arguements to call the function with
        :return: if the action was taken
        """
        if args is None:
            args = []
        if condition:
            action(*args)
        return condition

    def rotate_display_method(self, radians):
        self.display.rotate(radians)

    def set_metadata(self, values:dict):
        """
        Reloads the object from the provided metadata
        :param values: the dictonary to load the object from
        """
        for v in list(values.keys()):
            values["@{}".format(v)] = values[v]
        self.__init__(self.screen, values, self.parent)
        self.oncreate()

    def get_optional_arguement(self, key: str, default, return_type:type=None, is_literal_value=False, blank_means_unset=False):
        """
        Returns either the value in a dictionary, or a default value specified if the value is not in the dictionary
        :param key: The key to look for in the arguement dictionary
        :param default: The value to return if the value does not exits
        :param return_type: The datatype to cast the result to (regardless if it is found or not)
        :param is_literal_value: If the key specified is the literal key (True), or if it should try both the value, and the value preceded by the  @ sign
        :param blank_means_unset: If a blank value is found (""), treat it as unset. Default is False
        :return: Either the value in the dictionary, or the default value
        """
        return get_optional(self.args, key, default, return_type=return_type, is_literal_value=is_literal_value, blank_means_unset=blank_means_unset)


    def get_mandatory_arguement(self, key: str, return_type:type=None, is_literal_value=False):
        """
        Returns the value in a dictionary. If the value does not exist, raise a ValueError
        :param key: The key to look for in the arguement dictionary
        :param return_type: The datatype to cast the result to (regardless if it is found or not)
        :param is_literal_value: If the key specified is the literal key (True), or if it should try both the value, and the value preceded by the  @ sign
        :return: The value in the dictionary
        """
        return get_mandatory(self.args, key, return_type=return_type, is_literal_value=is_literal_value)


    def draw_to_screen(self, item=None, x=None, y=None):
        """
        Draws the item to the screen
        :param item: the object to draw. This can be an object which inherits from the "DisplayBase" class (SideScroller.DisplayMethods.DisplayBase.DisplayBase), or a pygame surface. If not specified, the set display method will be used
        :param x: the x position to draw the object at. If not specified, the object's x position will be used.
        :param y: the y position to draw the object at. If not specified, the object's y position will be used.
        """
        if item is None:
            item = self.display
        if x is None:
            x = self.x
        if y is None:
            y = self.y

        if isinstance(item, DisplayBase):
            item.draw(x, y)
        elif type(item) is pygame.Surface:
            self.screen.blit(item, (x, y))
        else:
            raise ValueError("Unknown Object Type \"{}\" ({}). Please only use objects which inherit from the \"DisplayBase\" class, or are Pygame Surfaces".format(item.__class__.__name__, type(item)))

    def register_object(self, path: str, class_name:str):
        """
        Registers a new object class
        :param path: the path to the file of the new object
        :param class_name: the name of the class from the file to create from
        :return: the reference to the class of the registered object
        """
        return self.parent.register_object(path, class_name)

    def add_room(self, name):
        """
        Creates a new empty room object
        :param name: the reference name of the room
        :return: the newly created room object
        """
        return self.parent.add_room(name)

    def is_touching_mouse(self):
        """
        Returns if this object is touching the mouse cursor
        """
        return point_in_rect(pygame.mouse.get_pos(), self.rect)

    def delete_room(self, name):
        """
        Deletes the room with the specified name
        :param name: the name of the room to delete
        """
        self.parent.delete_room(name)

    def rename_room(self, old, new):
        """
        Renames a room
        :param old: the current name of the room
        :param new: the new name of the room 
        """
        self.parent.rename_room(old, new)

    def system_onroomenter(self):
        self.ticker = Ticker()

    def system_update(self):
        self.parent_update()
        self.time_delta = self.ticker.tick

    def move(self, x, y, fire_onscreen_event=True):
        """
        This is the foundation for how this object is able to move
        Note: The object CAN NOT move if the "locked" property is set to True
        :param x: the x position change (in pixels)
        :param y: the y position change (in pixels)
        :param fire_onscreen_event: If the "onmove" event will be fired after movingf the object
        """
        if self.locked == "true":
            return True
        self.x += x
        self.y -= y
        self.x_delta = x
        self.y_delta = y
        onscreen = self.is_onscreen
        if fire_onscreen_event:
            if onscreen != self.on_screen_cache:
                if onscreen:
                    self.onscreenenter()
                else:
                    self.onscreenleave()
                self.on_screen_cache = onscreen
            self.onmove(x, y)
            self.collision_detecion(self.parent.props.array)

        return onscreen

    def add_object(self, class_type: str, args, x=None, y=None):
        """
        Creates a new object, and adds it to the current room
        :param class_type: The name of the class to add
        :param args: A dictionary of arguments to send to the new object (The '@' sign is not a mandatory prefix for each object)
        :param x: The x position of the object (if left blank, the x position specified in the 'args' dict will be used in place 
        :param y: The x position of the object (if left blank, the x position specified in the 'args' dict will be used in place
        :return: The newly created object
        """
        return self.parent.add_object(class_type, args, x, y)

    def collision_detecion(self, objects: typing.List['ObjectBase']):
        """
        Checks collision between this object, and a list of other objects.
        If collision is detected, the "oncollide" event of both objects is run
        :param objects: The list of objects to check
        """
        for obj in objects:
            if rect_a_touch_b(self.rect, obj.rect):
                self.oncollide(obj)
                obj.oncollide(self)

    def is_touching(self, other:'ObjectBase'):
        """
        Determines if this object is touching another object
        NOTE: Will NOT fire the "oncollide" event
        :param other: The object to check against
        :return: If the objects are touching
        """
        me = self.polygon
        you = other.point_array

        for p in you:
            if me.contains_point(p):
                return True
        return False

    def calculate_center(self, width:int=None, height:int=None):
        """
        Calculates the x, y position to place the specified object in the center of the screen 
        :param width: The width of the object to center (ommit and "None" will be returned for the "x" position)
        :param height: The height of the object to center (ommit and "None" will be returned for the "y" position)
        :return: the x, y position to place the object to center it
        """
        c = get_surface_center(self.screen)
        w, h = None, None
        if width is not None:
            w = c[0] - (width / 2)
        if height is not None:
            h = c[1] - (height / 2)
        return w, h

    def run_func_in_sec(self, func:callable, delay:float, *args, **kwargs):
        """
        Runs the specified function after the specified delay
        :param func: the reference to the function to run
        :param delay: the delay in s
        NOTE: after the delay, you may pass in poisional and named arguements which will be passed into the function which is run
        """
        self.parent.run_func_in_sec(func, delay, args, kwargs)

    def time_move(self, x_velocity:float, y_velocity:float):
        """
        Moves the object based on time (not framerate)
        This is the funtion which should be used for all object movement
        :param x_velocity: the velocity (speed) in the x direction
        :param y_velocity: the velocity (speed) in the y direction
        """
        self.move(x_velocity * self.time_delta, y_velocity * self.time_delta)

    def undo_last_move(self):
        """
        Undoes the object's last movement
        This DOES NOT fire the "onmove" event
        """
        self.move(-self.x_delta, -self.y_delta, fire_onscreen_event=False)

    def delete(self, obj:'ObjectBase'=None, fire_event:bool=True):
        """
        Deletes this object from memory
        This also fires the "ondelete" event
        :param obj: The reference of the object to delete (leave blank to delete this object)
        :param fire_event: If the "ondelete" event should also be triggered
        """
        delete = self
        if obj is not None:
            delete = obj
        if fire_event: delete.ondelete()
        delete.deleted = True

    def change_room(self, new_room):
        """
        Changes the current room to a different one
        This fires the "onroomleave" event for all objects in this room, and "onroomenter" for the objects in the new room
        :param new_room: The room to move to
        """
        self.parent.parent.set_room(new_room)

    def is_touching_type(self, model:str):
        """
        Checks if this object is touching another object of a specified type (from a specified Class)
        NOTE: Will NOT fire the "oncollide" event
        :param model: The name of the type/class to check against
        :return: If there is colloision
        """
        for obj in self.parent.props.array:
            if obj.model_type == model:
                if rect_a_touch_b(self.rect, obj.rect):
                    return True
        return False

    def get_touching_type(self, model:str):
        """
        returns all of the objects which are of the specified model, and are touching this object
        NOTE: Will NOT fire the "oncollide" event
        :param model: The name of the type/class to check against
        :return: the collided objects
        """
        touching = []
        for obj in self.parent.props.array:
            if obj.model_type == model and obj != self:
                if rect_a_touch_b(self.rect, obj.rect):
                    touching.append(obj)
        return touching

    def get_all_type(self, model:str):
        """
        Gets all of the objets of a specified class/type
        :param model: The class/type to select from
        :return: A list of matches
        """
        matches = []
        for obj in self.parent.props.array:
            if obj.model_type == model:
                matches.append(obj)
        return matches

    def highlight_point(self, point, y=None, color=(255, 255, 255), radius=3):
        """
        Highlights a specified point (if run in the object's "draw" method) with a circle
        :param point: The point to highlight in the format (x, y), or the x position of the point
        :param y: If the "point" parameter contains the 'x' position, this MUST contain the y position
        :param color: The color to draw the circle as
        :param radius: The radius of the circle
        """
        if y is None:
            x, y = point
        else:
            x = point
        pygame.draw.circle(self.screen, color, (int(x), int(y)), radius)

    def draw_alpha(self, source, opacity, pos=None):
        """
        Draws the pygame Surface with transparency
        :param source: the pygame Surface
        :param opacity: the opacity of the object (0 = invisible, 255 = visible)
        :param pos: the location to draw the object at (levae blank for the location of this object)
        """
        if pos is None:
            x, y = (self.x, self.y)
        else:
            x, y = pos
        # noinspection PyArgumentList
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(self.screen, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)
        self.screen.blit(temp, (x, y))

    def rotate_object(self, surf: pygame.Surface, angle=None):
        """
        Rotates and returns a surface relative to the surface's center
        :param surf: the surface to rotate
        :param angle: the angle to rotate by. Leave blank to use this object's angle
        :return: 
        """
        if angle is None:
            angle = self.angle
        orig_rect = surf.get_rect()
        rot_image = pygame.transform.rotate(surf, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def move_angle(self, velocity, angle=None):
        """
        Moves this object along a specified angle
        :param velocity: the velocity to move the object
        :param angle: The angle to move the object. If not specified, the object's angle will be used
        """
        if angle is None:
            angle = self.angle
        self.move(
            int(velocity * math.cos(angle * (math.pi / 180))),
            int(velocity * math.sin(angle * (math.pi / 180)))
        )

    def move_angle_time(self, velocity, angle=None):
        """
        Moves this object along a specified angle using time-based movement
        :param velocity: the velocity to move the object
        :param angle: The angle to move the object. If not specified, the object's angle will be used
        """
        if angle is None:
            angle = self.angle
        self.move(
            int(velocity * math.cos(angle * (math.pi / 180)) * self.time_delta),
            int(velocity * math.sin(angle * (math.pi / 180)) * self.time_delta)
        )

    def reload_room(self, name:str=None):
        """
        Reloads the specified room
        WARNING: DO NOT run this method in the "oncreate", or "onroomenter" events to avoid recursion
        :param name: the name of the room to reload (if blank, the room containing this object will be reloaded)
        """
        self.parent.reload_room(name)

    def attempt_quit(self):
        """
        Attempt to quit the game. This will run the "onquit" event for each object.
        If "False" is returned by any object's "onquit" event, the program will not be quit
        """
        self.parent.attempt_quit()

    def reproduce(self, screen:pygame.Surface=None, args:dict=None, parent=None, add_to_room:bool=True):
        """
        Reproduces this object
        :param screen: the screen to draw this object to. If left blank, this object's screen will be used
        :param args: the arguements to use. If left blank, this object's arguements will be used
        :param parent: the parent "Room" object to add this object to. If left blank, this object's room will be used
        :param add_to_room: if the object should automatically be added to the specified room
        :return: the new object
        """
        if screen is None:
            screen = self.screen

        if args is None:
            args = self.args

        if parent is None:
            parent = parent

        obj = self.__class__(screen, args, parent)
        if add_to_room:
            parent.add_created_object(obj)
        return obj

    def broadcast_message(self, message, self_included=False):
        """
        Sends the specified message to ALL objects in the same room as this one
        :param message: the message to send out
        :param self_included: if the message should be setnt out to this object as well. (Default is False)
        """
        destanations = self.siblings[:]
        if self_included is False:
            destanations.remove(self)
        self.multicast_message(message, destanations)

    def multicast_message(self, message, destanations: 'typing.List[ObjectBase]'):
        """
        Sends the specifeid message to the objects in the specified list
        :param message: the message to send
        :param destanations: the objects to send the message to
        """
        self.parent.send_message(message, destanations)

    def unicast_message(self, message, destanation:'ObjectBase'):
        """
        Sends the specified message to the one single object which has been specified
        :param message: the message to send
        :param destanation: the single object to send the message to
        """
        self.multicast_message(message, [destanation])

    def draw_rect(self, color, x:int, y:int, w:int, h:int, width:int=0):
        """
        Draws a rectangle on the screen
        :param color: The color of the rectangle
        :param x: the x position of the rectangle
        :param y: the y position of the rectangle
        :param w: the width of the rectangle
        :param h: the height of the rectangle
        :param width: the line thickness of the rectangle (0 to fill completly)
        :return: the rectangle which surrounds this object (pygame rect)
        """
        return pygame.draw.rect(self.screen, convert_color(color), (x, y, w, h), width)

    def draw_polygon(self, color, points:list, width:int=0):
        """
        Draws a polygon to the screen
        :param color: The color of the polygon
        :param points: the list of points (ex: [(x1, y1), (x2, y2), (x3, y3)] ) The first and last points will connect. Must have more than 3 points.
        :param width: the line thickness of the polygon (0 to fill completly)
        :return: the rectangle which surrounds this object (pygame rect)
        """
        return pygame.draw.polygon(self.screen, convert_color(color), points, width)

    def draw_circle(self, color, x:int, y:int, radius:int, width:int=0):
        """
        Draws a circle to the screen
        :param color: the color of the circle
        :param x: the x position of the circle
        :param y: the y position of the circle
        :param radius: the radius of the circle
        :param width: the line thickness of the circle (0 to fill completly)
        :return: the rectangle which surrounds this object (pygame rect)
        """
        return pygame.draw.circle(self.screen, convert_color(color), (x, y), radius, width)

    def draw_elipse(self, color, x:int, y:int, w:int, h:int, width:int=0):
        """
        Draws an elipse to the screen
        :param color: the color of the circle
        :param x: the x position of the elipse
        :param y: the y position of the elipse
        :param w: the width of the elipse
        :param h: the height of the elipse
        :param width: the line thickness of the elipse (0 to fill completly)
        :return: the rectangle which surrounds this object (pygame rect)
        """
        return pygame.draw.ellipse(self.screen, convert_color(color), (x, y, w, h), width)

    def draw_arc(self, color, x:int, y:int, w:int, h:int, angle1:float, angle2:float, width:int=1):
        """
        Draws an arc to the screen
        :param color: the color of the arc
        :param x: the x position of the arc
        :param y: the y position of the arc
        :param w: the width of the arc
        :param h: the height of the arc
        :param angle1: The starting angle in radians
        :param angle2: The ending angle in radians
        :param width: the line thickness of the arc
        :return: the rectangle which surrounds this object (pygame rect)
        """
        return pygame.draw.arc(self.screen, convert_color(color), (x, y, w, h), angle1, angle2, width)

    def draw_line(self, color, x1:int, y1:int, x2:int, y2:int, width:int=1):
        """
        Draws a line to the screen
        :param color: the color of the line
        :param x1: the x position of the line's starting point
        :param y1: the y position of the line's starting point
        :param x2: the x position of the line's ending point
        :param y2: the y position of the line's ending point
        :param width: the line thickness
        :return: the rectangle which surrounds this object (pygame rect)
        """
        return pygame.draw.line(self.screen, convert_color(color), (x1, y1), (x2, y2), width)

    def draw_lines(self, color, closed:bool, points:list, width:int=1):
        """
        Draws a series of lines to the screen
        :param color: the color of the lines
        :param closed: if the engine should draw an additional line between the first an last point
        :param points: a list of points to be connected by lines (ex: [(x1, y1), (x2, y2), (x3, y3)] ) Must have more than 3 points.
        :param width: the line thicknesses
        :return: the rectangle which surrounds this object (pygame rect)
        """
        return pygame.draw.lines(self.screen, convert_color(color), closed, points, width)

    def draw_aaline(self, color, x1: int, y1: int, x2: int, y2: int, width: int = 1):
        """
        Draws an antialiased line to the screen
        :param color: the color of the line
        :param x1: the x position of the line's starting point
        :param y1: the y position of the line's starting point
        :param x2: the x position of the line's ending point
        :param y2: the y position of the line's ending point
        :param width: the line thickness
        :return: the rectangle which surrounds this object (pygame rect)
        """
        return pygame.draw.aaline(self.screen, convert_color(color), (x1, y1), (x2, y2), width)

    def draw_aalines(self, color, closed: bool, points: list, width: int = 1):
        """
        Draws a series of antialiased lines to the screen
        :param color: the color of the lines
        :param closed: if the engine should draw an additional line between the first an last point
        :param points: a list of points to be connected by lines (ex: [(x1, y1), (x2, y2), (x3, y3)] ) Must have more than 3 points.
        :param width: the line thicknesses
        :return: the rectangle which surrounds this object (pygame rect)
        """
        return pygame.draw.aalines(self.screen, convert_color(color), closed, points, width)

    def parent_update(self):
        """
        This method is here in the event another update is needed (like a parent object)
        """
        pass

    def update(self, pressed_keys):
        """
        Overridable method run once per frame. This is for all of the logic the object requires
        DO NOT do any drawing here. It will NOT get displayed
        :param pressed_keys: The list of the states of each key. Indexes are based on ASCII values. Ex. 101=e, so pressed_keys[101] = state of the 'e' key
        """
        pass

    def draw(self):
        """
        Overridable method run once per frame. This is for all of the drawing which needs to be done.
        It is stronlgy recomended to keep all of your logic in the "update" method, and your visual updates here.
        NOTE: this method WILL NOT run if the object is off the screen
        """
        pass

    def onclick(self, button, pos):
        """
        Overridable event run each time this object is clicked (the mouse changes to the down state)
        :param button: A tuple of the states of the mouse in the format (left_mouse, middle_mouse/mouse_wheel, right_mouse)
        :param pos: The position of the mouse cursor
        """
        pass

    def onnotclick(self, button, pos):
        """
        Overridable event run each time the user clicks, but has not clicked this object (the mouse changes to the down state)
        :param button: A tuple of the states of the mouse in the format (left_mouse, middle_mouse/mouse_wheel, right_mouse)
        :param pos: The position of the mouse cursor
        """
        pass

    def onrelease(self, button, pos):
        """
        Overridable event run each time this object is released (the mouse changes to the up state)
        :param button: A tuple of the states of the mouse in the format (left_mouse, middle_mouse/mouse_wheel, right_mouse)
        :param pos: The position of the mouse cursor
        """
        pass

    def onmousedown(self, button, pos):
        """
        Overridable event run each time the mouse changes to the down state (regardless if it is over this object)
        :param button: A tuple of the states of the mouse in the format (left_mouse, middle_mouse/mouse_wheel, right_mouse)
        :param pos: The position of the mouse cursor 
        """
        pass

    def onmouseup(self, button, pos):
        """
        Overridable event run each time the mouse changes to the down state (regardless if it is over this object)
        :param button: A tuple of the states of the mouse in the format (left_mouse, middle_mouse/mouse_wheel, right_mouse)
        :param pos: The position of the mouse cursor
        """
        pass

    def onmousemotion(self, position, relative, buttons):
        """
        Overridable event run each time the mouse moves
        :param position: The position of the mouse cursor on the screen
        :param relative: The amount of distance the mouse has moved since the last method call
        :param buttons: A tuple of the states of the mouse in the format (left_mouse, middle_mouse/mouse_wheel, right_mouse)
        """
        pass

    def onmouseover(self, position, relative, buttons):
        """
        Overridable event run each time the mouse moves on top of this object
        :param position: The position of the mouse cursor on the screen
        :param relative: The amount of distance the mouse has moved since the last method call
        :param buttons: A tuple of the states of the mouse in the format (left_mouse, middle_mouse/mouse_wheel, right_mouse)
        """
        pass

    def onmouseleave(self, position, relative, buttons):
        """
        Overridable event run each time the mouse moves off of this object
        :param position: The position of the mouse cursor on the screen
        :param relative: The amount of distance the mouse has moved since the last method call
        :param buttons: A tuple of the states of the mouse in the format (left_mouse, middle_mouse/mouse_wheel, right_mouse)
        """
        pass

    def onkeydown(self, unicode, key, modifier, scancode):
        """
        Overridable event run each time any key on the keyboard is changed to the down state
        :param unicode: The character version of the key pressed (affected by keyboard modifiers)
        :param key: the character code of the key presed (ex. e=101)
        :param modifier: a bitmask representation of the keyboard modifiers used. Use "SideScroller.utils.deconstruct_modifier_bitmask" to convert to a list of modifiers
        :param scancode: The platform-specific key code (WARNING: Can be different between different keyboards)
        """
        pass

    def onkeyup(self, key, modifier, scancode):
        """
        Overridable event run each time any key on the keyboard is changed to the up state 
        :param key: the character code of the key presed (ex. e=101)
        :param modifier: a bitmask representation of the keyboard modifiers used. Use "SideScroller.utils.deconstruct_modifier_bitmask" to convert to a list of modifiers
        :param scancode: The platform-specific key code (WARNING: Can be different between different keyboards)
        """
        pass

    def onroomenter(self):
        """
        Overridable event run each time the user enters the room which contains this object
        """
        pass

    def onroomleave(self, next_room):
        """
        Overridable event run each time the user leaves the room which contains this object
        :param next_room: The name of the room the user is moving to
        """
        pass

    def onquit(self):
        """
        Overridable event run when the game is quit (closed)
        """
        pass

    def ondelete(self):
        """
        Overridable event run when this object is deleted from memory
        """
        pass

    def oncreate(self):
        """
        Overridable event run when this object is created
        """
        pass

    def onevent(self, event):
        """
        Overridable event run each time ANY pygame event takes place
        :param event: The pygame event object
        """
        pass

    def onscreenenter(self):
        """
        Overridable event run each time the object moves from being off the screen to back on the screen
        """
        pass

    def onscreenleave(self):
        """
        Overridable event run each time the object moves from being on the screen to off the screen
        """
        pass

    def onmove(self, x_change, y_change):
        """
        Overridable event run each time this object is moved
        :param x_change: the change in the x direction the object has moved
        :param y_change: the change in the y direction the object has moved
        """
        pass

    def oncollide(self, obj:'ObjectBase'):
        """
        Overridable event run each time this object collides with another
        :param obj: the object which this object has collided with
        """
        pass

    def onmessagerecieve(self, message:str):
        """
        Overridable event run when this object recieves a message
        :param message: the message recieved
        """
        pass
