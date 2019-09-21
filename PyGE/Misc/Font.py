import pygame
import os


class Font:
    def __init__(self, path, size, bold=False, italic=False):
        self.path = path
        self.size = size
        self.bold = bold
        self.italic = italic

        if not os.path.isfile(path):
            print("WARNING: Font File '{}' Could Not Be Located!".format(path))
            print("System Font Will Be Used In Place. This WILL cause a fatal error when project is exported")
            self.font = pygame.font.SysFont(path, size, bold=bold, italic=italic)
        else:
            self.font = pygame.font.Font(path, size, bold=bold, italic=italic)

    def render(self, text, antialias, color, background=None):
        return self.font.render(text, antialias, color, background)

    def size(self, text):
        return self.font.size(text)

    def set_underline(self, bool):
        self.font.set_underline(bool)

    def get_underline(self):
        return self.font.get_underline()

    def set_bold(self, bool):
        self.font.set_bold(bool)

    def get_bold(self):
        return self.font.get_bold()

    def set_italic(self, bool):
        self.font.set_italic(bool)

    def get_italic(self):
        return self.font.get_italic()

    def metrics(self, text):
        return self.font.metrics(text)

    def get_linesize(self):
        return self.font.get_linesize()

    def get_height(self):
        return self.font.get_height()

    def get_ascent(self):
        return self.font.get_ascent()

    def get_descent(self):
        return self.font.get_descent()