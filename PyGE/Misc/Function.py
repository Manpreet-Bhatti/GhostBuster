import time
from math import *


class Function:
    def __init__(self, func:str):
        """
        This function represents a mathimatical function. Note: it has access to the "math" library
        :param func: The string of a math expression, where "x" is the independent variable. ex. "2**x" for an exponential function, or "sin(x)" for a sinusodial function
        """
        self.func = func
        self.start = time.time()

    def restart(self):
        """
        Restarts the function creation time
        """
        self.start = time.time()

    def get_y(self, x=None):
        """
        Returns the value of "y" given "x"
        If "x" is not provided, the amount of time since the class instantiation (or last call to "restart") is used in place of "x"
        :param x: The "x" value to calculate "y" with 
        :return: The value of "y"
        """
        if x is None:
            x = time.time() - self.start
        return eval(self.func.replace("x", str(x)))
