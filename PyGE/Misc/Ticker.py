from time import time


class Ticker:
    def __init__(self):
        """
        This class returns the amount of time between each call of the "tick" property
        """
        self.last = time()

    @property
    def tick(self):
        """
        :return: the time since the last call to this property 
        """
        delta = time() - self.last
        self.last = time()
        return delta
