from .ObjectBase import ObjectBase
from ..DisplayMethods.Color import Color
from ..utils import convert_color
import pygame


class SolidColor(ObjectBase):
    def __init__(self, screen:pygame.Surface, args: dict, parent):
        ObjectBase.__init__(self, screen, args, parent)
        self.w = self.get_mandatory_arguement("w", int)
        self.h = self.get_mandatory_arguement("h", int)
        self.color = self.get_mandatory_arguement("color", int)
        self.set_display_method(Color(self.screen, convert_color(self.color), self.w, self.h))

    @property
    def metadata(self):
        return {
            "x": self.x,
            "y": self.y,
            "w": self.w,
            "h": self.h,
            "color": self.color
        }

    def draw(self):
        self.draw_to_screen()
