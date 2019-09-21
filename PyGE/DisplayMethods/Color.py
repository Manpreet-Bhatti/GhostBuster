import pygame
from PyGE.DisplayMethods.DisplayBase import DisplayBase


class Color(DisplayBase):
    def __init__(self, screen: pygame.Surface, color:tuple, width:int, height:int):
        """
        This class is to be used for all objects which are represented on the screen by a single rectangle
        :param screen: The main pygame surface to draw the rectangle to
        :param color: The color to draw the rectangle (R, G, B)
        :param width: The width of the rectangle
        :param height: The height of the rectangle
        """
        DisplayBase.__init__(self)
        self.color = color
        self.screen = screen
        self.w, self.h = width, height
        self.angle = 0
        self.surf = pygame.Surface((self.w, self.h))
        self.surf.fill(self.color)
        self.rotated = None

        self.rotate(0)

    def draw(self, x ,y):
        """
        Draws the rectangle at the specified position
        :param x: The x position
        :param y: The y position
        """
        self.screen.blit(self.rotated, (x, y))

    def rotate(self, radians):
        self.angle += radians
        self.rotated = pygame.transform.rotate(self.surf, self.angle)
