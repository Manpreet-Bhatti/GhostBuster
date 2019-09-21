import typing

import pygame
import xmltodict

from PyGE.Screens.Room import Room
from PyGE.Errors import RoomNotDeclaredException, InvalidXMLException
from PyGE.Globals.Objects import PREMADE_OBJECTS

pygame.init()


class PyGE:
    def __init__(self, screen: pygame.Surface, level_data:str, starting_room: str, custom_objects:typing.List):
        """
        This is the most important object in the entire system!
        You can use a custom version of this class by passing in a refrence to the class into the "alt_side_scroller" property
        in the function call which starts the engine. We recomend building a class which inherits from this one and overiding what you need to
        :param screen: the screen to draw the game to
        :param level_data: the XML representation of the level 
        :param starting_room: the name of the room to start the user in
        :param custom_objects: a list of the references to the custom objects which will be used (not including objects provided by the engine)
        """

        self.screen = screen
        self.level_data = level_data
        self.rooms = {}
        self.custom_objects = PREMADE_OBJECTS + custom_objects
        self.load_game()
        self.room = None

        self.set_room(starting_room)

    def load_game(self, level_data: str=None):
        """
        Builds each room, and creates all nessicary objects
        :param level_data: the data to load from. If not specified, use the data which was provided when the class was instantiated 
        """
        if level_data is None:
            level_data = self.level_data

        self.level_data = level_data
        try:
            json = xmltodict.parse(level_data)
        except xmltodict.expat.ExpatError:
            raise InvalidXMLException("The XML Provided Is Invalid (Syntax Error?). Please Check The XML, And Try Again")
        building = json["building"]["room"]

        if "@name" in building:
            building = [building]
        for room in building:
            self.rooms[str(room["@name"])] = Room(self.screen, room, self.custom_objects, self)

    def update(self, events:list):
        """
        Triggers the selected room's update event
        :param events: a list of active events
        """
        self.room.update(events)

    def draw(self):
        """
        Triggers the selected room's draw event. Only objects on screen are drawn
        """
        self.room.draw()

    def set_room(self, room):
        """
        Set the selected room to a different room. Triggers the room leave, and enter event
        :param room: the room to move to
        """
        if self.room is not None:
            self.room.leave_room(room)
        try:
            self.room = self.rooms[room]
        except KeyError:
            raise RoomNotDeclaredException(
                "The Specified Room '{}' Has Not Been Declared In The Provided XML. NOTE: Names Are Case Sensitive"
                    .format(room)
            )
        self.room.enter_room()

    def add_room(self, name):
        """
        Create a new empty room
        :param name: the name to save the room as
        """
        self.rooms[name] = Room(self.screen, {"@name": name}, self.custom_objects, self)
        return self.rooms[name]

    def delete_room(self, name):
        """
        Deletes the specified room
        :param name: the name of the room to delete
        :return: the room which was just deleted
        """
        rm = self.rooms[name]
        del self.rooms[name]
        return rm

    def rename_room(self, old, new):
        """
        Renames the specifed room
        :param old: the current name of the room
        :param new: the new name of the room
        """
        self.rooms[new] = self.rooms[old]
        self.rooms[new].name = new
        self.delete_room(old)

    def reload_room(self, name:str):
        """
        Reloads a specified room
        :param name: the name of the room to reload
        """
        self.rooms[name].reload_room()

    def attempt_quit(self):
        """
        Attempt to close the application.
        This will trigger each object's "onquit" event.
        If any object returns "False" to the "onquit" event, the quit will not happen.
        All object in the selected room will run this event guarenteed
        """
        if self.room.quit_action():
            quit()
