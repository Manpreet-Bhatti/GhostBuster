import typing

import pygame

from PyGE.Screens.ScreenBase import ScreenBase
from PyGE.ASQL import ASQL
from PyGE.utils import get_mandatory, point_in_rect
from PyGE.Objects.ObjectBase import ObjectBase
from PyGE.utils import rect_a_touch_b
from PyGE.Globals.GlobalVariable import get_sys_var
from PyGE.Errors import ObjectNotDeclaredException

HALL = 0


class Room(ScreenBase):
    def __init__(self, screen, data:dict, custom_objects:typing.List, parent):
        """
        The object which manages, and stores every object in a room
        NOTE: Only key functions are documented, which are available to each object via the "parent" variable in each class
        """
        ScreenBase.__init__(self, screen)
        self.name = get_mandatory(data, "@name")
        self.props = ASQL()
        self.custom_objects = custom_objects
        self.parent = parent
        self.data = data
        self.load_room()

    def load_room(self):
        self.props = ASQL()
        for item in self.data:
            if type(self.data[item]) is list:
                for count in range(len(self.data[item])):
                    if not item.startswith("@"):
                        found = False
                        for c in self.custom_objects:
                            if c.__name__ == item:
                                self.props.append(c(self.screen, self.data[item][count], self))
                                found = True
                                break
                        if found is False:
                            raise ObjectNotDeclaredException("The Object '{0}' Is Referenced In The XML, But Is Not Declared. Please Place A Reference To The '{0}' Class In The 'custom_objects' List When Calling The 'side_scroller' Function.".format(item))
            else:
                if not item.startswith("@"):
                    found = False
                    for c in self.custom_objects:
                        if c.__name__ == item:
                            if self.data[item] is None:
                                self.data[item] = {}
                            self.props.append(c(self.screen, self.data[item], self))
                            found = True
                            break
                    if found is False:
                        raise ObjectNotDeclaredException(
                            "The Object '{0}' Is Referenced In The XML, But Is Not Declared. Please Place A Reference To The '{0}' Class In The 'custom_objects' List When Calling The 'side_scroller' Function.".format(
                                item))

    def register_object(self, path:str, class_name:str):
        path = path.replace("\\", ".").replace("/", ".").replace(".py", "")
        class_name = class_name.replace(".py", "")
        mod = __import__(path, fromlist=[''])
        class_ref = getattr(mod, class_name)
        self.custom_objects.append(class_ref)
        return class_ref

    def enter_room(self):
        for prop in self.props.array:
            prop.system_onroomenter()
            prop.onroomenter()

    def leave_room(self, new_room):
        for prop in self.props.array:
            prop.onroomleave(new_room)


    def quit_action(self):
        can_quit = True
        for prop in self.props.array:
            if prop.onquit() is False:
                can_quit = False
        return can_quit

    def draw(self):
        for prop in self.props.array:
            if prop.on_screen_cache:
                prop.draw()
            if get_sys_var("debug"):
                pygame.draw.rect(self.screen, prop.debug_color, prop.rect, 3)

    def update(self, events:list):
        for prop in self.props.array:
            if prop.deleted:
                self.props.array.remove(prop)
                continue
            prop.system_update()
            prop.update(pygame.key.get_pressed())
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if point_in_rect(event.pos, prop.rect):
                        prop.onclick(event.button, event.pos)
                    else:
                        prop.onnotclick(event.button, event.pos)
                    prop.onmousedown(event.button, event.pos)
                if event.type == pygame.MOUSEBUTTONUP:
                    if point_in_rect(event.pos, prop.rect):
                        prop.onrelease(event.button, event.pos)
                    prop.onmouseup(event.button, event.pos)
                if event.type == pygame.MOUSEMOTION:
                    prop.onmousemotion(event.pos, event.rel, event.buttons)
                    if point_in_rect(event.pos, prop.rect):
                        if prop.on_mouse_over_cache is False:
                            prop.on_mouse_over_cache = True
                            prop.onmouseover(event.pos, event.rel, event.buttons)
                    else:
                        if prop.on_mouse_over_cache:
                            prop.on_mouse_over_cache = False
                            prop.onmouseleave(event.pos, event.rel, event.buttons)
                if event.type == pygame.KEYDOWN:
                    prop.onkeydown(event.unicode, event.key, event.mod, event.scancode)
                if event.type == pygame.KEYUP:
                    prop.onkeyup(event.key, event.mod, event.scancode)
                prop.onevent(event)

    def move_many(self, objects: typing.List['ObjectBase'], x, y, fire_onscreen_event:bool=True, static: typing.List['ObjectBase']=None):
        """
        Moves many objects by a factor of x, and y
        :param objects: The list of objects to move
        :param x: The distance (in pixels) to move each object by along the x axis
        :param y: The distance (in pixels) to move each object by along the y axis
        :param fire_onscreen_event: If the "onscreen" event should be fired if an object moves on screen while being moved
        :param static: The list of objects which each object that is moving should check collision against. If not specified, use all objects. If there is collision, all movement will be undone  
        """
        if static is None:
            static = self.props

        abort = False
        for p in objects:
            p.move(x, y, fire_onscreen_event)
            for s in static:
                if rect_a_touch_b(p.rect, s.rect):
                    abort = True

        if abort:
            for p in objects:
                p.undo_last_move()

    def add_object(self, class_type:str, args:dict, x=None, y=None):
        """
        Creates a new object, and adds it to the current room
        :param class_type: The name of the class to add
        :param args: A dictionary of arguments to send to the new object (The '@' sign is not a mandatory prefix for each object)
        :param x: The x position of the object (if left blank, the x position specified in the 'args' dict will be used in place 
        :param y: The x position of the object (if left blank, the x position specified in the 'args' dict will be used in place 
        :return: The newly created object
        """
        if x is not None:
            args["@x"] = x

        if y is not None:
            args["@y"] = y

        for a in list(args.keys())[:]:
            if not a.startswith("@"):
                args["@" + a] = args[a]

        for c in self.parent.custom_objects:
            if c.__name__ == class_type:
                obj = c(self.screen, args, self)
                self.props.append(obj)
                return obj

    def add_created_object(self, o):
        self.props.append(o)

    def send_message(self, message, destanations: 'typing.List[ObjectBase]'):
        for d in destanations:
            d.onmessagerecieve(message)

    def add_room(self, name):
        return self.parent.add_room(name)

    def delete_room(self, name):
        self.parent.delete_room(name)

    def rename_room(self, old, new):
        self.parent.rename_room(old, new)

    def reload_room(self, name:str=None):
        if name is None:
            self.load_room()
        else:
            self.parent.reload_room(name)

    def attempt_quit(self):
        self.parent.attempt_quit()
