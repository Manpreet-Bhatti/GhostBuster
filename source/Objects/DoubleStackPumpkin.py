import pygame
import random

from PyGE.Objects.ObjectBase import ObjectBase
from PyGE.Objects.Text import Text
from PyGE.Screens.Room import Room
from PyGE.Globals.Cache import get_image
from PyGE.Misc.AlarmClock import AlarmClock
import PyGE.utils as utils
import source.GlobalVariable as GlobalVariable


class DoubleStackPumpkinHandler(ObjectBase):
    def __init__(self, screen:pygame.Surface, args: dict, parent:'Room'):
        args["@x"], args["@y"] = (-10, -10)
        ObjectBase.__init__(self, screen, args, parent)

        self.spawn_countdown = AlarmClock(1.00)
        self.spawn_countdown.start()

    def oncreate(self):
        GlobalVariable.score = 0

    def update(self, pressed_keys):
        if self.spawn_countdown.finished:
            self.spawn_countdown.restart()
            self.add_object("DoubleStackPumpkin", {}, -31, random.randint(0, self.screen.get_height() - 32))


class DoubleStackPumpkin(ObjectBase):
    def __init__(self, screen:pygame.Surface, args: dict, parent:'Room'):
        ObjectBase.__init__(self, screen, args, parent)
    
        self.image = get_image("doublestackpumpkin")
        self.drawable = self.image

        self.w, self.h = self.image.get_size()

        self.angle = 0

        self.drawable = self.rotate_object(self.image, self.angle - 90)
        self.velocity = 100

        self.scoreboard = self.get_all_type("Text")[0]     # type: Text

        self.screen_c_w, self.screen_c_h = utils.get_surface_center(self.screen)
        self.bulletCounter = 0

    def update(self, pressed_keys):
        self.move_angle_time(self.velocity)

    def oncollide(self, obj:'ObjectBase'):
        if obj.object_type == "Skittle":
            self.bulletCounter = self.bulletCounter + 1
            self.delete(obj)
            if self.bulletCounter == 5:
                self.delete(self)
                self.delete(obj)

                self.change_score(200)
        if obj.object_type == "Ghost":
            self.change_room("menu")

    def onscreenleave(self):
        self.delete(self)
        self.change_score(-500)

    def draw(self):
        self.draw_to_screen(item=self.drawable)

    def change_score(self, delta:int):
        GlobalVariable.score += delta
        if GlobalVariable.score < 0:
            self.change_room("menu")
        self.scoreboard.set_text("Score: {}".format(GlobalVariable.score))