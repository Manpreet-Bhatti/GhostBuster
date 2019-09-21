import pygame

from PyGE.Objects.ObjectBase import ObjectBase
from PyGE.Screens.Room import Room
from PyGE.Globals.Cache import get_font
import PyGE.utils as utils


class PhysicsObjectBase(ObjectBase):
    def __init__(self, screen:pygame.Surface, args: dict, parent:'Room'):
        ObjectBase.__init__(self, screen, args, parent)
        self.can_fall = False

    def parent_update(self):
        if self.can_fall:
            pass


    def set_can_fall(self, state:bool):
        self.can_fall = state


