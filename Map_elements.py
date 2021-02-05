from settings import *
from Base_classes import Object
from Base_classes import FeasibleMove
import math


class Wall(pg.sprite.Sprite, Object):
    def __init__(self, game, x, y):
        Object.__init__(self, x, y, pg.Surface((TILESIZE - 3, TILESIZE - 3)), game)
        self.groups = game.all_sprites, game.walls_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image.fill(WALL_COLOR)
        self.rect.x = x * self.tilesize + 2
        self.rect.y = y * self.tilesize + 2


class Exit(pg.sprite.Sprite, Object):
    def __init__(self, game, x, y):
        Object.__init__(self, x, y, pg.Surface((TILESIZE - 3, TILESIZE - 3)), game)
        self.groups = game.all_sprites, game.exit_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image.fill(YELLOW)
        self.rect.x = x * self.tilesize + 2
        self.rect.y = y * self.tilesize + 2


class PowerUps(pg.sprite.Sprite, Object):
    def __init__(self, game, x, y, effect):
        image = pg.image.load('images/benefits.png')
        if effect == 1:
            image = pg.image.load('images/medicine.png')
            print("Error powerup not supported")
        Object.__init__(self, x, y, image, game)
        self.groups = game.all_sprites, game.power_ups_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.rect.x = x * self.tilesize
        self.rect.y = y * self.tilesize
        self.effect = effect

    def acquired_by(self, character):
        if self.effect == 0:
            character.range_fire = 4
        elif self.effect == 1:
            character.range_fire = 1
            # min = math.inf
            # max = - math.inf
            # for feasible in character.feasible_move:
            #     if feasible.id > max:
            #         max = feasible.id
            #     if feasible.id < min:
            #         min = feasible.id
            # for i in [min - 1, max + 1]:
            #     character.feasible_move.append(FeasibleMove(self.game, self.game.player, i))
        self.kill()


