import pygame

from PyGE.Objects.ObjectBase import ObjectBase
from PyGE.Screens.Room import Room
from PyGE.Globals.Cache import get_font
import PyGE.utils as utils


class Text(ObjectBase):
    def __init__(self, screen:pygame.Surface, args: dict, parent:'Room'):
        ObjectBase.__init__(self, screen, args, parent)

        self.font = get_font(self.get_mandatory_arguement("font", str))     # type: pygame.font.Font

        self.text = self.get_mandatory_arguement("text", str)
        self.antialiasing = bool(self.get_optional_arguement("antialiasing", 1, int, blank_means_unset=True))
        self.color = utils.convert_color(self.get_optional_arguement("color", "White", str, blank_means_unset=True))

        self.text_object = None
        self.rebuild_text_object()

    @property
    def metadata(self):
        return {
            "x": self.x,
            "y": self.y,
            "font": self.font,
            "text": self.text,
            "antialiasing": self.antialiasing,
            "color": self.color
        }

    def set_text(self, text:str):
        self.text = text
        self.rebuild_text_object()

    def set_color(self, color:str):
        self.color = utils.convert_color(color)
        self.rebuild_text_object()

    def set_antialiasing(self, antialiasing:bool):
        self.antialiasing = antialiasing
        self.rebuild_text_object()

    def set_font(self, font:str):
        self.font = get_font(font)
        self.rebuild_text_object()

    def rebuild_text_object(self):
        self.text_object = self.font.render(self.text, self.antialiasing, self.color)
        self.w, self.h = self.text_object.get_size()
        self.recalculate_position()

    def draw(self):
        self.draw_to_screen(self.text_object)
