import pygame
from time import time

from PyGE.utils import scale_image


class SpriteSheet:
    def __init__(self, image:str, w:int, h:int, duration:float=None, final_size:tuple=None, invisible_color:tuple=(0, 0, 1)):
        """
        This class is for creating spritesheets
        :param image: the path to the image of the sheet
        :param w: the width of each frame in the sheet
        :param h: the height of each frame in the sheet
        :param duration: the number of seconds to stay on each frame
        :param final_size: the final size to scale the image to
        :param invisible_color: the color which is invisible (DO NOT PICK A COLOR ON YOUR SPRITESHEET!)
        """
        self.base_image = pygame.image.load(image)
        self.path = image
        self.w = w
        self.h = h
        self.images = []
        self.duration = duration
        self.last_change = time()
        self.selected_image = 0
        sprite_w = self.base_image.get_width() / w
        sprite_h = self.base_image.get_height() / h
        self.final_size = final_size
        self.invisible_color = invisible_color
        if final_size is None:
            self.final_size = (int(sprite_w), int(sprite_h))

        x = 0
        y = 0
        for i in range(h):
            for _ in range(w):
                self.images.append(scale_image(pygame.transform.scale(self.get_image(x, y, sprite_w, sprite_h), self.final_size)))
                x += sprite_w
            x = 0
            y += sprite_h

    def get_image(self, x, y, width, height):
        """
        Gets a sub-image of the parent image  
        :param x: the x pos to start the selection
        :param y: the y pos to start the selection
        :param width: the width of the selection
        :param height: the heigh of the selection
        :return: the sub-image
        """
        # noinspection PyArgumentList
        image = pygame.Surface([width, height]).convert()
        image.fill(self.invisible_color)
        image.blit(self.base_image, (0, 0), (x, y, width, height))
        image.set_colorkey(self.invisible_color)
        return image

    @property
    def current_image(self):
        """
        Returns the current selected image
        This function is also used to flip between the images,
        and should be called in your game's main loop 
        """
        if time() - self.last_change >= self.duration:
            self.selected_image += 1
            if self.selected_image >= len(self.images):
                self.selected_image = 0
            self.last_change = time()
        return self.images[self.selected_image]

    def get_size(self):
        return self.final_size
