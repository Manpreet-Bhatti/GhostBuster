from .ObjectBase import ObjectBase
from ..utils import get_mandatory
import pygame


class Cube(ObjectBase):
    def __init__(self, screen:pygame.Surface, args: dict, parent):
        ObjectBase.__init__(self, screen, args, parent)
        self.full_w = get_mandatory(args, "@w", int)
        self.full_h = get_mandatory(args, "@h", int)
        self.w = self.full_w
        self.h = self.full_h
        self.z = 0

    @property
    def metadata(self):
        return {
            "x": self.x,
            "y": self.y,
            "w": self.w,
            "h": self.h
        }

    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 255), (self.x, self.y, self.w, self.h), 2)

    def update(self, pressed_keys):
        if pressed_keys[97] == 1:
            self.time_move(100, 0)

        if pressed_keys[100] == 1:
            self.time_move(-100, 0)
    #     self.z += 1
    #
    #     self.w = self.full_w / self.z
    #     self.h = self.full_h / self.z