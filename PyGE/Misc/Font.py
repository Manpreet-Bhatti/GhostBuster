import logging
import pygame
import os


class Font:
    def __init__(self, path, size, bold=False, italic=False):
        """
        This object is essentialy a wrapper for the pygame.Font object with additional features
        :param path: the path to the .ttf/.otf file or name of system font. NOTE: Using System fonts are bad practice. Use .ttf or .otf files
        :param size: the size of the font
        :param bold: if the font should be bolded (warning: experamental)
        :param italic: if the font should be italisized (warning: experamental)
        """
        self.path = path
        self.size = size
        self.bold = bold
        self.italic = italic

        if not os.path.isfile(path):
            logging.warning("WARNING: Font File '{}' Could Not Be Located! The System Font Will Be Used In Place. This WILL cause a fatal error when project is exported".format(path))
            self.font = pygame.font.SysFont(path, size, bold=bold, italic=italic)
        else:
            self.font = pygame.font.Font(path, size, bold=bold, italic=italic)

    def render(self, text, antialias, color, background=None):
        """
        Renders the speicified text in this font configuration
        :param text: The text to render
        :param antialias: if antialiasing should be used (smoothens out the rendered text)
        :param color: the color to render the text in
        :param background: the background color to surround the text
        :return: the rendered font
        """
        return self.font.render(text, antialias, color, background)

    def size(self, text):
        return self.font.size(text)

    def set_underline(self, state:bool):
        """
        Sets if this font should enable an underline
        :param state: if the underline should be enabled
        """
        self.font.set_underline(state)

    def get_underline(self):
        """
        Returns if this object has an underline enabled
        :return: if there is an underline
        """
        return self.font.get_underline()

    def set_bold(self, state:bool):
        """
        Sets if this font should be bold (warning: experamental)
        :param state: if this font should be bold
        """
        self.font.set_bold(state)

    def get_bold(self):
        """
        Returns if this object is bold (warning: experamental)
        :return: if the object is bold
        """
        return self.font.get_bold()

    def set_italic(self, state:bool):
        """
        Sets if this font should be italisized (warning: experamental)
        :param state: if this font should be italic
        """
        self.font.set_italic(state)

    def get_italic(self):
        """
        Returns if this object is italic (warning: experamental)
        :return: if the object is italic
        """
        return self.font.get_italic()

    def metrics(self, text:str):
        """
        Returns font metrics of the specified text with this font
        Each character returns a tuple in the format (minx, maxx, miny, maxy, advance)
        If a character is unrecognized, None is returned
        :param text: the text to get metrics on
        :return: the metrics of the text
        """
        return self.font.metrics(text)

    def get_linesize(self):
        """
        The recomented space between lines if the font is used accross multiple lines
        :return: the line space
        """
        return self.font.get_linesize()

    def get_height(self):
        return self.font.get_height()

    def get_ascent(self):
        return self.font.get_ascent()

    def get_descent(self):
        return self.font.get_descent()