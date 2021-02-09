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

    def move(self, dx, dy):
        Character.move(self, dx, dy)
        if self.on_play_mode:
            pg.event.post(pg.event.Event(ENEMY_TURN_EVENT))

    def shoot_fire(self):
        Character.shoot_fire(self)
        if self.on_play_mode:
            pg.event.post(pg.event.Event(ENEMY_TURN_EVENT))

    def update(self):
        self.rect.x = self.x * self.tilesize
        self.rect.y = self.y * self.tilesize

    def damage(self, damage):
        Character.damage(self, damage)
        if self.hp <= 0:
            if self.on_play_mode:
                pg.event.post(pg.event.Event(PLAYER_GAME_OVER))
