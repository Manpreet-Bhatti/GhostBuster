from PyGE.Engine import side_scroller
from source.Objects.Bullet import Bullet
from source.Objects.Enemy import Enemy, EnemyHandler
from source.Objects.Player import Player
from source.Objects.Button import Button
from source.Objects.Background import BackgroundImage
from source.Objects.Enemy2 import Enemy2, EnemyHandler2
from source.Objects.Menu import MenuImage


def run():
    side_scroller(
        xml=open("resources/xml/rooms.xml").read(),
        start_room="menu",
        images={
            "player1": {"path": "resources/images/player/player1.png", "w": 32, "h": 32},
            "player2": {"path": "resources/images/player/player2.png", "w": 32, "h": 32},
            "enemy": {"path": "resources/images/enemy/enemy1.png", "w": 32, "h": 32},
            "enemy2": {"path": "resources/images/enemy/enemy2.png", "w": 32, "h": 32},
            "bullet": {"path": "resources/images/bullets/bullet.png", "w": 32, "h": 32},
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
            Player, Bullet, Enemy, EnemyHandler, Button, BackgroundImage, Enemy2, EnemyHandler2, MenuImage
        ],
        initial_variables={
        },
        development_screen_size=(800, 500),
        fullscreen=False,
        auto_scale=False,
        background_color=(10, 10, 10)
    )