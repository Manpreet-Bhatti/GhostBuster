from PyGE.Objects.ObjectBase import ObjectBase
from PyGE.Globals.Cache import get_image

class MenuImage(ObjectBase):
    def oncreate(self):
        self.image = get_image("background")
        
    def draw(self):
        self.draw_to_screen(self.image)