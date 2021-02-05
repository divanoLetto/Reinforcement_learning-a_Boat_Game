from Base_classes import Character, table_feasible_directions
from settings import *
from Utils import isClose


class Enemy(pg.sprite.Sprite, Character):
    #  Actions:
    # Type: Discrete(2)
    #   0 Fire          2 Move center
    #   1 Move sx       3 Move dx
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemies_sprites
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
        Character.__init__(self, x, y, list_images, game, game.player)
        self.previus_action = 0  # todo update that
        self.image_broken = pg.image.load('images/explosion.png')

    def update(self):
        self.rect.x = self.x * self.tilesize
        self.rect.y = self.y * self.tilesize

    def damage(self, damage):
        Character.damage(self, damage)
        if self.hp <= 0:
            self.kill()
            self.image = self.image_broken
            pg.sprite.Sprite.__init__(self, self.game.all_sprites, self.game.walls_sprites)




