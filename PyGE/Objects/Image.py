import pygame

from PyGE.Globals.Cache import get_image
from PyGE.Objects.ObjectBase import ObjectBase


class Image(ObjectBase):
    def __init__(self, screen, args, parent):
        ObjectBase.__init__(self, screen, args, parent)
        self.image = get_image(self.get_mandatory_arguement("image", str))
        self.scale = self.get_optional_arguement("scale", 1, float)
        self.reload_image()

    def reload_image(self):
        """
        Reloads the image. This is done automatically whenever a change is made to a property
        """
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * self.scale), int(self.image.get_height() * self.scale)))

    def set_image(self, image:str):
        """
        Sets the image to the specified image in the cache
        :param image: the image to set this object to
        """
        self.image = get_image(image)

    def set_scale(self, scale:float):
        """
        Sets the image scale to the specified value
        :param scale: the scale to set
        """
        self.scale = scale

    def draw(self):
        """
        Draws this image to the screen
        """
        self.draw_to_screen(self.image)
