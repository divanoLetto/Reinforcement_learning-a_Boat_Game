from Base_classes import Character, table_feasible_directions
from settings import *
from Utils import isClose


class Enemy(pg.sprite.Sprite, Character):
    #  Actions:
    # Type: Discrete(2)
    #   0 Fire          2 Move center
    #   1 Move sx       3 Move dx
    def __init__(self, game, x, y, on_play_mode):
        self.on_play_mode = on_play_mode
        self.groups = game.characters_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        list_images = [
            'images/player_N2.png',
            'images/player_E2.png',
            'images/player_S2.png',
            'images/player_O2.png',
            'images/player_NE2.png',
            'images/player_SE2.png',
            'images/player_SO2.png',
            'images/player_NO2.png'
        ]
        Character.__init__(self, x, y, list_images, game, game.player, game.feasible_moves_enemy)
        self.previus_action = 0  # todo update that
        self.image_broken = pg.image.load('images/explosion.png')

    def update(self):
        self.rect.x = self.x * self.tilesize
        self.rect.y = self.y * self.tilesize

    def damage(self, damage):
        Character.damage(self, damage)
        if self.hp <= 0 and self.on_play_mode:
            self.kill()
            self.image = self.image_broken
            pg.sprite.Sprite.__init__(self, self.game.characters_sprites)
            pg.time.delay(400)
            pg.event.post(pg.event.Event(PLAYER_GAME_OVER))




