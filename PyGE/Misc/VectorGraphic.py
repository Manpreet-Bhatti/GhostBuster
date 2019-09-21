import pygame
from pygame import gfxdraw
import numpy
import math
from PyGE.utils import rotate_point


class VectorGraphic:
    def __init__(self, screen:pygame.Surface, points:list, x:int, y:int, color:tuple, fill:bool=True, connect:bool=True, outline:tuple=None, thickness:int=1):
        """
        This class is for a single vector graphic
        - A geometric shape shape defined by coordinates of verticies
        - Easy to apply geometric transformations on
        :param screen: the surface to draw the graphic onto
        :param points: the list of points to create the graphic from - [(x, y), (x, y)...]
        :param x: the x position to place the center of the image
        :param y: the y position to place the center of the image
        :param color: the color to draw the graphic in
        :param fill: if the graphic should be filled
        :param connect: if the graphic should connect first and last points (if disabled, the graphic CAN NOT be filled in)
        :param outline: the outline color of the graphic (will only work if graphic is filled)
        :param thickness: the thickness of the lines
        """
        self.screen = screen
        self.origin = numpy.array(points)
        self.points = numpy.array(points)
        self.color = color
        self.fill = fill
        self.connect = connect
        self.outline = outline
        self.thickness = thickness
        self.pos = numpy.array([x, y])
        self.reposition()

    @property
    def center(self):
        """
        Returns the mean of x and y coordiates (the shape center)
        :return: the center point of the shape (x, y)
        """
        return self.points.mean(0)

    def scale(self, factor):
        """
        Scales the shape by the specified factor
        :param factor: the factor to scale the points
        """
        numpy.multiply(self.points, factor, out=self.points, casting="unsafe")
        numpy.multiply(self.origin, factor, out=self.origin, casting="unsafe")
        self.reposition()

    def set_pos(self, x, y):
        """
        moves the graphic to the specified x and y position
        :param x: the x coordinate to move the graphic to
        :param y: the y coordinate to move the graphic to
        """
        self.pos = numpy.array([x, y])
        self.reposition()

    def reposition(self):
        """
        Recenters the graphic arround its position
        (you will probabally not need to use this one)
        """
        numpy.add(self.points, self.pos - self.center, out=self.points, casting="unsafe")

    def rotate_degrees(self, deg):
        """
        Rotates the graphic by a specified number of degrees
        :param deg: the amount of degrees to rotate the graphic by
        """
        self.rotate(deg * (math.pi / 180))

    def rotate(self, rad):
        """
        Rotates the graphic by a specified number of radians
        :param rad: the amount of radians to rotate the graphic by
        """
        self.points = numpy.array([rotate_point(x, self.pos, rad) for x in self.origin + self.center / 2])
        self.reposition()


    def reflect(self, horizontal:bool=True, vertical:bool=True):
        """
        Refleccts the graphic along either/both axis
        :param horizontal: if the graphic should be reflected along the horizontal axis (horizontally)
        :param vertical: if the graphic should be reflected along the vertical axis (vertically)
        """
        if horizontal:
            self.points = numpy.flipud(self.points)
        if vertical:
            self.points = numpy.fliplr(self.points)

    def draw(self):
        """
        Draws the graphic to the screen
        """
        if self.fill and self.connect:
            pygame.gfxdraw.filled_polygon(self.screen, self.points, self.color)
            if self.outline is not None:
                pygame.draw.lines(self.screen, self.outline, self.connect, self.points, self.thickness)
        else:
            pygame.draw.lines(self.screen, self.color, self.connect, self.points, self.thickness)

    def copy(self):
        """
        Returns an exact copy of this object
        :return: a copy
        """
        return VectorGraphic(
            self.screen, list(self.points), self.pos[0], self.pos[1], self.color,
            self.fill, self.connect, self.outline, self.thickness
        )

