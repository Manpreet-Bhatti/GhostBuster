from PyGE.Engine import side_scroller
from source.Objects.Skittle import Skittle
from source.Objects.Pumpkin import Pumpkin, PumpkinHandler
from source.Objects.Ghost import Ghost
from source.Objects.Button import Button
from source.Objects.Background import BackgroundImage
from source.Objects.DoubleStackPumpkin import DoubleStackPumpkin, DoubleStackPumpkinHandler
from source.Objects.Menu import MenuImage


def run():
    side_scroller(
        xml=open("resources/xml/rooms.xml").read(),
        start_room="menu",
        images={
            "ghost": {"path": "resources/images/ghost/ghost.png", "w": 32, "h": 32},
            "pumpkin": {"path": "resources/images/pumpkins/pumpkin.png", "w": 32, "h": 32},
            "doublestackpumpkin": {"path": "resources/images/pumpkins/doublestackpumpkin.png", "w": 32, "h": 32},
            "skittle": {"path": "resources/images/skittles/skittle.png", "w": 32, "h": 32},
            "background": {"path": "resources/images/background/background.jpg", "w": 800, "h": 500},
            "menu": {"path": "resources/images/background/menu.jpg", "w": 800, "h": 500}
        },
        sprite_sheets={

        },
        sounds={
        },
        font={
          "Querround16": {"path": "resources/font/halloween/halloween.TTF", "size": 16}
        },
        custom_objects=[
            Ghost, Skittle, Pumpkin, PumpkinHandler, Button, BackgroundImage, DoubleStackPumpkin, DoubleStackPumpkinHandler, MenuImage
        ],
        initial_variables={
        },
        development_screen_size=(800, 500),
        fullscreen=False,
        auto_scale=False,
        background_color=(10, 10, 10)
    )