import PyGE

class Verticy:
    def __init__(self, node_a:'PyGE.Node', node_b:'PyGE.Node', color="inherit", thickness=5):
        self.thickness = thickness
        self.color = color
        self.node_b = node_b
        self.node_a = node_a
