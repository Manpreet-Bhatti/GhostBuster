import pygame

from PyGE.Globals.Cache import get_spritesheet
from PyGE.Objects.ObjectBase import ObjectBase


class SpriteSheet(ObjectBase):
    def __init__(self, screen, args, parent):
        ObjectBase.__init__(self, screen, args, parent)
        self.spritesheet = get_spritesheet(self.get_mandatory_arguement("src", str))

    def set_sprite_sheet(self, src:str):
        """
        Sets the sprite sheet to the specified sprite sheet in the cache
        :param src: the sprite sheet to set this object to
        """
        self.spritesheet = get_spritesheet(src)

    def draw(self):
        """
        Draws this image to the screen
        """
        self.draw_to_screen(self.spritesheet.current_image)
