import pygame

from PyGE.utils import convert_color
from PyGE.Globals.Cache import get_font
from PyGE.DisplayMethods.DisplayBase import DisplayBase


class Text(DisplayBase):
    def __init__(self, screen: pygame.Surface, font:str, text:str, color, antialiasing=True):
        """
        This class is to be used for all objects which are represented on the screen by text
        :param screen: The main pygame surface to draw the text to
        :param font: The reference to the font in the cache to use
        :param text: The text to render in the font
        :param color: The color to draw the text
        :param antialiasing: If antialiasing should be used
        """
        DisplayBase.__init__(self)
        self.color = convert_color(color)
        self.screen = screen
        self.font = get_font(font)
        self.text = text
        self.antialiasing = antialiasing

        self.text_object = None

        self.reload_text()

    def reload_text(self):
        """
        Reloads the text object
        """
        self.text_object = self.font.render(self.text, self.antialiasing, self.color)
        self.w, self.h = self.text_object.get_size()

    def set_text(self, text:str):
        """
        Sets the text to the specified value
        :param text: the text
        """
        self.text = text
        self.reload_text()

    def set_font(self, font:str):
        """
        Sets the font to the specified font in the cache
        :param font: the font
        """
        self.font = get_font(font)
        self.reload_text()

    def set_color(self, color):
        """
        Sets the color to the specified value
        :param color: the color
        """
        self.color = convert_color(color)
        self.reload_text()

    def draw(self, x ,y):
        """
        Draws the text at the specified position
        :param x: The x position
        :param y: The y position
        """
        self.screen.blit(self.text_object, (x, y))
