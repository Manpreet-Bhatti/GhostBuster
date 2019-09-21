from PyGE.Objects.ObjectBase import ObjectBase
from PyGE.Globals.Cache import get_image

class BackgroundImage(ObjectBase):
    def oncreate(self):
        self.image = get_image("menu")
        
    def draw(self):
        self.draw_to_screen(self.image)