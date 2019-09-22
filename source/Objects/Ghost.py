import pygame

from PyGE.Objects.ObjectBase import ObjectBase
from PyGE.Screens.Room import Room
from PyGE.Globals.Cache import get_image
from PyGE.Misc.AlarmClock import AlarmClock
import PyGE.utils as utils


class Ghost(ObjectBase):
    def __init__(self, screen:pygame.Surface, args: dict, parent:'Room'):
        ObjectBase.__init__(self, screen, args, parent)

        self.angle = 90
        self.velocity = 100

        self.number = self.get_mandatory_arguement("number", int)

        self.image = self.rotate_object(get_image("ghost".format(self.number)))

        self.w, self.h = self.image.get_size()

        self.shot_cool_down = AlarmClock(0.250)
        self.shot_cool_down.start()

    @property
    def bullet_y(self):
        return self.y + (self.h / 2)

    def draw(self):
        self.draw_to_screen(self.image)

    def update(self, pressed_keys):
        # print(len(self.siblings))

        if (pressed_keys[pygame.K_w] == 1 and self.number == 1) or (pressed_keys[pygame.K_UP] == 1 and self.number == 2):
            self.time_move(0, self.velocity)
            self.boundary_check()

        if (pressed_keys[pygame.K_s] == 1 and self.number == 1) or (pressed_keys[pygame.K_DOWN] == 1 and self.number == 2):
            self.time_move(0, -self.velocity)
            self.boundary_check()

        if self.shot_cool_down.finished:
            self.add_object("Skittle", {"angle": self.angle + 90}, x=self.x, y=self.bullet_y)
            self.shot_cool_down.restart()

    def boundary_check(self):
        if not utils.rect_a_in_b(self.rect, self.screen.get_rect()):
            self.undo_last_move()

    def onkeydown(self, unicode, key, modifier, scancode):
        if key == 27:
            self.change_room("menu")