import pygame

from PyGE.Objects.ObjectBase import ObjectBase
from PyGE.Screens.Room import Room
from PyGE.Globals.Cache import get_image


class Skittle(ObjectBase):
    def __init__(self, screen:pygame.Surface, args: dict, parent:'Room'):
        ObjectBase.__init__(self, screen, args, parent)
        self.angle = self.get_mandatory_arguement("angle", float)
        self.velocity = self.get_optional_arguement("velocity", 200, float)
        self.radius = 1

        self.image = get_image("skittle")
        self.drawable = self.image

        self.w = self.radius * 1
        self.h = self.radius * 2

    def draw(self):
        self.draw_to_screen(self.drawable, self.x, self.y)

    def update(self, pressed_keys):
        self.move_angle_time(self.velocity)

    def onscreenleave(self):
        self.delete(self)