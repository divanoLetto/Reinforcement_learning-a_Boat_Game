from Base_classes import Character
from settings import *
from Utils import isClose


class Player(pg.sprite.Sprite, Character):
    #  Actions:
    # Type: Discrete(2)
    #   0 Fire          2 Move center
    #   1 Move sx       3 Move dx
    def __init__(self, game, x, y, on_play_mode):
        self.groups = game.all_sprites
        self.on_play_mode = on_play_mode
        pg.sprite.Sprite.__init__(self, self.groups)
        list_images = [
            'images/player_N.png',
            'images/player_E.png',
            'images/player_S.png',
            'images/player_O.png',
            'images/player_NE.png',
            'images/player_SE.png',
            'images/player_SO.png',
            'images/player_NO.png'
        ]
        Character.__init__(self, x, y, list_images, game, game.enemy)
        # self.image_N = pg.image.load('images/player_N.png')
        # self.image_E = pg.image.load('images/player_E.png')
        # self.image_S = pg.image.load('images/player_S.png')
        # self.image_O = pg.image.load('images/player_O.png')
        # self.image_NE = pg.image.load('images/player_NE.png')
        # self.image_SE = pg.image.load('images/player_SE.png')
        # self.image_SO = pg.image.load('images/player_SO.png')
        # self.image_NO = pg.image.load('images/player_NO.png')

    def move(self, dx, dy):
        Character.move(self, dx, dy)
        if self.on_play_mode:
            pg.event.post(pg.event.Event(ENEMY_TURN_EVENT))

    def shoot_fire(self):
        Character.shoot_fire(self)
        if self.on_play_mode:
            pg.event.post(pg.event.Event(ENEMY_TURN_EVENT))

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def damage(self, damage):
        Character.damage(self, damage)
        if self.hp <= 0:
            if self.on_play_mode:
                pg.event.post(pg.event.Event(PLAYER_GAME_OVER))
