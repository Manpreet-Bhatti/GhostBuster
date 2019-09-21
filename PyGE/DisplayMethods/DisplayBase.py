class DisplayBase:
    def __init__(self):
        """
        This is the class in which ALL display methods MUST inherit from (takes no arguements)
        """
        self.w, self.h = (0, 0)
        self.angle = 0

    def draw(self, x, y):
        """
        Overridable method for drawing the object to the screen
        :param x: The x position
        :param y: The y position
        """
        pass

    def get_size(self):
        """
        Gets the size of the display object
        :return: (width, height)
        """
        return self.w, self.h

    def get_width(self):
        """
        Gets just the width of the display object
        :return: width
        """
        return self.w

    def get_height(self):
        """
        Gets just the height of the display object
        :return: height
        """
        return self.h
