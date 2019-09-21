import PyGE

class Node:
    def __init__(self, x, y, z, color="inherit", size=5):
        self.x = x
        self.y = y
        self.z = z
        self.color = color
        self.size = size
        self.rel_size = self.get_relative_size()

    def get_relative_size(self):
        return PyGE.get_relative_size(self.size, self.z)