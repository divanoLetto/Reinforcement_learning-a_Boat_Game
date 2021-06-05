from Base_classes import Object
import pygame as pg

from settings import DARKGREY, WHITE, LIGHTGREY


class Powerups_visualization(pg.sprite.Sprite, Object):
    sy = 0
    def __init__(self, game, effect):
        deltax = 1
        deltay = 1
        x = 14 + deltax
        y = self.sy + deltay
        Powerups_visualization.sy = self.sy + deltay
        image = pg.image.load('images/benefits.png')
        if effect == 1:
            image = pg.image.load('images/medicine.png')
        elif effect == 2:
            image = pg.image.load('images/powerup2.png')
        Object.__init__(self, x, y, image, game)
        self.groups = game.powerups_visualization_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.rect.x = x * self.tilesize - (self.tilesize/2)
        self.rect.y = y * self.tilesize - (self.tilesize/2)
        self.effect = effect

        if effect is 0:
            text = "Gittata aumentata"
        elif effect is 1:
            text = "Cannone frontale"
        else:
            text = "Cannoni posteriori"

        text_x = (x + 1) * self.tilesize - (self.tilesize / 2)
        text_y = y * self.tilesize - (self.tilesize / 2)

        self.text = TextPowerup(game, text, text_x + 5, text_y + 8)


class TextPowerup(pg.sprite.Sprite):
    def __init__(self, game, text, x, y):
        self.groups = game.powerups_visualization_text_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        font = pg.font.Font('freesansbold.ttf', 15)
        text = font.render(text, True, WHITE, LIGHTGREY)
        self.image = text
        self.rect = text.get_rect()
        self.rect.x = x
        self.rect.y = y