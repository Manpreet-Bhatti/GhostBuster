from PyGE import ObjectBase


class ObjectBase3D(ObjectBase):
    def __init__(self, screen, args: dict, parent):
        ObjectBase.__init__(self, screen, args, parent)
