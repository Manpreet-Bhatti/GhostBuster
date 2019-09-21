import pygame

from PyGE.Objects.ObjectBase import ObjectBase


class AbstractObjectBase(ObjectBase):
    def __init__(self, screen:pygame.Surface, args: dict, parent):
        """
        Objects which will not be drawn to the screen may inherit from this class instead of the ObjectBase class
        :param screen: The screen to draw the object to
        :param args: The dictionary of properties specified in the XML.
        :param parent: The room the object will live in 
        """
        args["@x"] = 0
        args["@y"] = 0
        ObjectBase.__init__(self, screen, args, parent)
