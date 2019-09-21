from PyGE.Globals.Cache import get_font
from PyGE.Objects.ObjectBase import ObjectBase

import pygame


class Button(ObjectBase):
    def __init__(self, screen:pygame.Surface, args: dict, parent):
        ObjectBase.__init__(self, screen, args, parent)

        self.color = (255, 255, 255)

        self.font_name = self.get_mandatory_arguement("font", str)
        self.font = get_font(self.font_name)

        self.value = self.get_mandatory_arguement("text", str)
        self.text = self.font.render(self.value, True, self.color)

        self.set_width(self.get_optional_arguement("w", self.text.get_width(), int))
        self.set_height(self.get_optional_arguement("h", self.text.get_height(), int))

        self.sup = self.get_mandatory_arguement("supplementary", str)

        self.outline = pygame.Rect(self.rect)

        self.visible = bool(self.get_optional_arguement("visible", 1, int))

        self.text_x = self.x + ((self.w / 2) - (self.text.get_width() / 2))
        self.text_y = self.y + ((self.h / 2) - (self.text.get_height() / 2))

    def draw(self):
        if self.visible:
            pygame.draw.rect(self.screen, self.color, self.outline, 1)
            self.draw_to_screen(self.text, self.text_x, self.text_y)

    def onclick(self, button, pos):
        if self.sup == "1":
            self.change_room("arenaSingle")
        elif self.sup == "2":
            self.attempt_quit()

    def onroomleave(self, next_room):
        self.reload_room(next_room)

    @property
    def rect(self):
        return self.x, self.y, self.w, self.h
