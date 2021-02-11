from settings import *
from Base_classes import Object


class Wall(pg.sprite.Sprite, Object):
    def __init__(self, game, x, y):
        Object.__init__(self, x, y, pg.Surface((TILESIZE - 3, TILESIZE - 3)), game)
        self.groups = game.walls_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image.fill(WALL_COLOR)
        self.rect.x = x * self.tilesize + 2
        self.rect.y = y * self.tilesize + 2


class Exit(pg.sprite.Sprite, Object):
    def __init__(self, game, x, y):
        Object.__init__(self, x, y, pg.Surface((TILESIZE - 3, TILESIZE - 3)), game)
        self.groups = game.exit_sprites
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
        self.groups = game.power_ups_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.rect.x = x * self.tilesize
        self.rect.y = y * self.tilesize
        self.effect = effect

    def acquired_by(self, character):
        if self.effect == 0:
            # more range
            character.range_fire = 4
        elif self.effect == 1:
            # malus: less range
            character.range_fire = 1
        self.game.power_ups.remove(self)
        self.kill()


