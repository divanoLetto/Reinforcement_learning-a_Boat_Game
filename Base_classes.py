from settings import *
from Utils import isClose
from random import randint


table_feasible_directions = {
        "0": [-1, -1],
        "1": [0, -1],
        "2": [1, -1],
        "3": [1, 0],
        "4": [1, 1],
        "5": [0, 1],
        "6": [-1, 1],
        "7": [-1, 0],
        "[-1, -1]": 0,
        "[0, -1]": 1,
        "[1, -1]": 2,
        "[1, 0]": 3,
        "[1, 1]": 4,
        "[0, 1]": 5,
        "[-1, 1]": 6,
        "[-1, 0]": 7
    }


class Object:
    def __init__(self, x, y, image, game):
        self.x = x
        self.y = y
        self.tilesize = TILESIZE
        self.gridheight = GRIDHEIGHT
        self.gridwidth = GRIDWIDTH
        self.game = game
        self.image = image
        self.rect = self.image.get_rect()
        super().__init__()

    def getX(self):
        return self.x

    def getY(self):
        return self.y


class Character(Object):
    #  Actions:
    # Type: Discrete(2)
    #   0 Fire          2 Move center
    #   1 Move sx       3 Move dx
    # codification directions:
    #               0 1 2
    # direction --> 8 x 4
    #               7 6 5
    def __init__(self, x, y, list_images, game, nemesi):
        Object.__init__(self, x, y, pg.image.load(list_images[4]), game)
        self.image_N = pg.image.load(list_images[0])
        self.image_E = pg.image.load(list_images[1])
        self.image_S = pg.image.load(list_images[2])
        self.image_O = pg.image.load(list_images[3])
        self.image_NE = pg.image.load(list_images[4])
        self.image_SE = pg.image.load(list_images[5])
        self.image_SO = pg.image.load(list_images[6])
        self.image_NO = pg.image.load(list_images[7])
        self.direction = [1, -1]
        self.feasible_move = []
        self.nemesi = nemesi
        self.max_direction_code = 8
        for id in [-2, -1, 0, 1, 2]:  # for id in [-1, 0, 1]:
            self.feasible_move.append(FeasibleMove(self.game, self, id))
        self.range_fire = 2
        self.fire_shoots = self.fire_x_init()
        self.hp = 1
        self.max_hp = 2  # todo make this mechanics in powerup
        self.num_actions = 1 + len(self.feasible_move)

    def fire_x_init(self):
        fire_xs = []
        start_fire_dir = [-2, +2]
        for i in range(2):
            fire_xs.append(FireX(self.game, self, i, start_fire_dir[i]))
        return fire_xs

    def update_shoot_and_feasible_moves(self):
        for block in self.feasible_move:
            block.move()
        for fire_shoot in self.fire_shoots:
            fire_shoot.move()

    def move(self, dx, dy):
        self.setDirection(dx, dy)
        self.x += dx
        self.y += dy

    def step_turn(self, action):
        # return True if perform a feasible action. False otherwise
        if self.hp <= 0:
            #  print("Already dead")
            return None
        if action == 0:
            self.shoot_fire()
            return True
        else:
            if not self.feasible_move[action - 1].check_not_collision():
                return False
            else:
                feasible_dir = [
                    table_feasible_directions[str((table_feasible_directions[str(self.direction)] + d.id) % 8)]
                    for d in self.feasible_move]
                choose_move = feasible_dir[action - 1]
                self.move(choose_move[0], choose_move[1])
                return True

    def random_action(self):
        # feasible_dir = [table_feasible_directions[str((table_feasible_directions[str(self.direction)] + d.id) % 8)]for d in self.feasible_move if d.no_collision()]
        # return randint(0, len(feasible_dir))
        return randint(0, self.num_actions - 1)

    def shoot_fire(self):
        for shoot in self.fire_shoots:
            if self.nemesi is None:
                print("error")
            wx = self.nemesi.x
            wy = self.nemesi.y
            if isClose(wx, shoot.getX(), 0.5) and isClose(wy, shoot.getY(), 0.5):
                self.nemesi.damage(1)

    def damage(self, damage):
        # ,print("Damage!")
        self.hp -= damage

    def setDirection(self, dx, dy):
        if dx == 0 and dy == 0:
            print("error direction")
        self.direction = [dx, dy]
        if dx == -1 and dy == -1:
            self.image = self.image_NO
        elif dx == 0 and dy == -1:
            self.image = self.image_N
        elif dx == 1 and dy == -1:
            self.image = self.image_NE
        elif dx == 1 and dy == 0:
            self.image = self.image_E
        elif dx == 1 and dy == 1:
            self.image = self.image_SE
        elif dx == 0 and dy == 1:
            self.image = self.image_S
        elif dx == -1 and dy == 1:
            self.image = self.image_SO
        elif dx == -1 and dy == 0:
            self.image = self.image_O

    def getDirection(self):
        return self.direction

    def set_nemesi(self, character):
        self.nemesi = character


class FeasibleMove(pg.sprite.Sprite, Object):
    def __init__(self, game, player, id):
        Object.__init__(self, None, None,  pg.Surface((TILESIZE - 3, TILESIZE - 3)), game)
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.player = player
        self.id = id

        self.image.fill(LIGHTGREY)
        self.move()

        self.fix_dxdy = 2
        self.no_collision = True
        self.rect.x = self.x * self.tilesize
        self.rect.y = self.y * self.tilesize

    def move(self):
        d = self.player.getDirection()
        dx, dy = table_feasible_directions[str((table_feasible_directions[str(d)] + self.id) % 8)]
        self.x = self.player.getX() + dx
        self.y = self.player.getY() + dy
        self.no_collision = True
        for wall in self.game.walls:
            if isClose(wall.getX(), self.x, 0.5) and isClose(wall.getY(), self.y, 0.5):
                self.no_collision = False
        if self.x >= self.gridwidth / self.tilesize or self.x < 0 or self.y >= self.gridheight / self.tilesize or self.y < 0:
            self.no_collision = False
        if self.player.nemesi:
            if isClose(self.player.nemesi.getX(), self.x, 0.5) and isClose(self.player.nemesi.getY(), self.y, 0.5):
                self.no_collision = False

    def check_not_collision(self):
        return self.no_collision

    def update(self):
        if self.no_collision:
            self.rect.x = self.x * self.tilesize + self.fix_dxdy
            self.rect.y = self.y * self.tilesize + self.fix_dxdy
        else:
            self.rect.x = -10  # todo fix this
            self.rect.y = -10


class FireX(pg.sprite.Sprite, Object):
    def __init__(self, game, player,  id, traj):
        Object.__init__(self, None, None, pg.image.load('images/fire_x.png'), game)
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.player = player
        self.id = id
        self.trajectory_offset = traj
        self.move()

    def move(self):
        traj = table_feasible_directions[str((table_feasible_directions[str(self.player.getDirection())] + self.trajectory_offset) % 8)]
        range_fire = self.player.range_fire
        stop = False
        for i in range(1, range_fire + 1):
            x = self.player.getX() + traj[0] * i
            y = self.player.getY() + traj[1] * i
            #  check collision with walls or enemy
            enemy = []
            if self.player.nemesi is not None:
                enemy.append(self.player.nemesi)
            for coll in self.game.walls + enemy:
                if isClose(x, coll.x, 0.5) and isClose(y, coll.y, 0.5):
                    if isinstance(coll, Character):
                        range_fire = i
                    else:
                        range_fire = i - 1
                    stop = True
                    break
            #  check out-of-map problem
            if x >= self.gridwidth / self.tilesize or x < 0 or y >= self.gridheight / self.tilesize or y < 0:
                range_fire = i - 1
                stop = True
            if stop:
                break
        if range_fire > 0:
            self.x = self.player.getX() + traj[0] * range_fire
            self.y = self.player.getY() + traj[1] * range_fire
        else:
            self.x = -10  # todo fix this
            self.y = -10

    def update(self):
        self.rect.x = self.x * self.tilesize
        self.rect.y = self.y * self.tilesize


