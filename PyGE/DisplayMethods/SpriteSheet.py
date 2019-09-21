import pygame
from PyGE.DisplayMethods.DisplayBase import DisplayBase
from PyGE.Globals.Cache import get_spritesheet


class SpriteSheet(DisplayBase):
    def __init__(self, screen: pygame.Surface, spritesheet:str):
        """
        This class is to be used for all objects which are represented on the screen by a single sprite sheet
        :param screen: The surface to draw the sprite sheet to
        :param spritesheet: The name of the sprite sheet in the sprite sheet cache. NOTE: The sprite sheet MUST be stored in the cache 
        """
        DisplayBase.__init__(self)
        self.spritesheet = get_spritesheet(spritesheet)
        self.screen = screen
        self.w, self.h = self.spritesheet.current_image.get_size()

    def draw(self, x, y):
        """
        Draws the sprite sheet at the specified position
        :param x: The x position
        :param y: The y position
        """
        self.screen.blit(self.spritesheet.current_image, (x, y))
