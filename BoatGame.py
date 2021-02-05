import sys
import pandas
from Map_elements import *
from Player import *
from Enemy import *
from pygame_widgets import Button
import random
import numpy as np
from tabulate import tabulate
from deepcrawl.environment.game import Game
from reinforcements_settings import print_map_during_steps,print_info_during_steps, nums_values_channel


class BoatGame:
    def __init__(self, on_play_mode):
        pg.init()
        self.clock = pg.time.Clock()
        self.print_map_during_steps = print_map_during_steps
        self.print_info_during_steps = print_map_during_steps

        self.SETTING_WIDTH = SETTING_WIDTH
        self.SETTING_HEIGHT = SETTING_HEIGHT
        self.TILESIZE = TILESIZE
        self.GRIDWIDTH = GRIDWIDTH
        self.GRIDHEIGHT = GRIDHEIGHT
        self.HEIGHT = HEIGHT
        self.WIDTH = WIDTH
        self.MIN_START_DISTANCE_PLAYER_ENEMY = MIN_START_DISTANCE_PLAYER_ENEMY
        self.MIN_START_DISTANCE_PLAYER_EXIT = MIN_START_DISTANCE_PLAYER_EXIT
        self.NUM_EXITS = NUM_EXITS
        self.MIN_NUM_POWERUP = MIN_NUM_POWERUP
        self.MAX_NUM_POWERUP = MAX_NUM_POWERUP
        self.MIN_NUM_OBSTACLE = MIN_NUM_OBSTACLE
        self.MAX_NUM_OBSTACLE = MAX_NUM_OBSTACLE
        self.MIN_LENGHT_LINE = MIN_LENGHT_LINE
        self.MAX_LENGHT_LINE = MAX_LENGHT_LINE
        self.MIN_LINES_FOR_OBSTACLES = 1
        self.MAX_LINES_FOR_OBSTACLES = 2
        self.SIMULTAING_ENVIROMENT = SIMULTAING_ENVIROMENT

        self.ENEMY_TURN_EVENT = ENEMY_TURN_EVENT
        self.PLAYER_SHOOT_EVENT = PLAYER_SHOOT_EVENT
        self.PLAYER_GAME_OVER = PLAYER_GAME_OVER

        self.count_resetting = 0
        self.nums_values_channel = nums_values_channel[0]

        self.on_play_mode = on_play_mode
        if on_play_mode:
            self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
            pg.display.set_caption(TITLE)
            pg.key.set_repeat(500, 100)

    def init_game(self):
        # initialize all variables and do all the setup for a new game
        self.reset()

        # fire button
        self.button_x = self.GRIDWIDTH + 60
        self.button_y = self.GRIDHEIGHT - 100
        self.button_width = 93
        self.button_height = 45
        self.button_fire = Button(
            self.screen, self.button_x, self.button_y, self.button_width, self.button_height,
            text='Fire', fontSize=50, margin=20, inactiveColour=(0, 255, 0), hoverColour=(255, 255, 255),
            pressedColour=(255, 0, 0), radius=5, onRelease=lambda: self.fire_shoot_event()
        )

    def fire_shoot_event(self):
        pg.event.post(pg.event.Event(PLAYER_SHOOT_EVENT))

    def reset(self):
        # print("my_reset " + str(self.count_resetting))
        self.count_resetting += 1
        # sprites
        self.all_sprites = pg.sprite.Group()
        self.walls_sprites = pg.sprite.Group()
        self.enemies_sprites = pg.sprite.Group()
        self.exit_sprites = pg.sprite.Group()
        self.power_ups_sprites = pg.sprite.Group()

        self.enemy = None
        self.walls = []
        self.power_ups = []
        # walls
        self.generateMap()

        # player
        # print("player generating:")
        rand_px, rand_py = random.randint(1, self.GRIDWIDTH / self.TILESIZE - 2), random.randint(1, self.GRIDHEIGHT / self.TILESIZE - 2)
        while any(rand_px == w.x and rand_py == w.y for w in self.walls):
            rand_px, rand_py = random.randint(1, self.GRIDWIDTH / self.TILESIZE - 2), random.randint(1, self.GRIDHEIGHT / self.TILESIZE - 2)
        # print("    " + str(rand_px) + " " + str(rand_py))
        self.player = Player(self, rand_px, rand_py, self.on_play_mode)

        # enemies
        # print("enemies generating:")
        rand_ex, rand_ey = random.randint(1, self.GRIDWIDTH / self.TILESIZE - 2), random.randint(1, self.GRIDHEIGHT / self.TILESIZE - 2)
        px, py = int(self.player.getX()), int(self.player.getY())
        try:
            while any(rand_ex == w.x and rand_ey == w.y for w in self.walls + [self.player]): #and np.linalg.norm((int(rand_ex), int(rand_ey)), (px, py) )> MIN_START_DISTANCE_PLAYER_ENEMY:
                rand_ex, rand_ey = random.randint(1, self.GRIDWIDTH / self.TILESIZE - 2), random.randint(1, self.GRIDHEIGHT / self.TILESIZE - 2)
        except Exception as e:
            print("Something else went wrong 1")
        # print("    " + str(rand_ex) + " " + str(rand_ey))
        self.enemy = Enemy(self, rand_ex, rand_ey)
        self.player.set_nemesi(self.enemy)

        # exit
        # print("exit generating:")
        self.exit = []
        if self.NUM_EXITS != 0:
            rand_exit_x, rand_exit_y = random.randint(0, self.GRIDWIDTH / self.TILESIZE - 1), random.randint(0, self.GRIDHEIGHT / self.TILESIZE - 1)
            try:
                while any(rand_exit_x == w.x and rand_exit_y == w.y for w in self.walls + [self.player] + [self.enemy]): # and np.linalg.norm((int(rand_exit_x), int(rand_exit_y)), (int(self.player.getX()), int(self.player.getY()))) > MIN_START_DISTANCE_PLAYER_EXIT:
                    rand_exit_x, rand_exit_y = random.randint(0, self.GRIDWIDTH / self.TILESIZE - 1), random.randint(0, self.GRIDHEIGHT / self.TILESIZE - 1)
            except Exception as e:
                print("Something else went wrong 2")
            self.exit.append(Exit(self, rand_exit_x, rand_exit_y))
        # print("    " + str(rand_exit_x) + " " + str(rand_exit_y))


        # power ups
        # print("power ups generating:")
        num_powerup = random.randint(self.MIN_NUM_POWERUP, self.MAX_NUM_POWERUP)
        for i in range(num_powerup):
            rand_pow_x, rand_pow_y = random.randint(0, self.GRIDWIDTH / self.TILESIZE - 1), random.randint(0, self.GRIDHEIGHT / self.TILESIZE -1)
            rand_effect = 0
            while any(rand_pow_x == w.x and rand_pow_y == w.y for w in
                      self.walls + [self.player] + [self.enemy] + self.power_ups):
                rand_pow_x, rand_pow_y = random.randint(0, self.GRIDWIDTH / self.TILESIZE - 1), random.randint(0, self.GRIDHEIGHT / self.TILESIZE -1)
            self.power_ups.append(PowerUps(self, rand_pow_x, rand_pow_y, rand_effect))
        #     print("    " + str(rand_pow_x) + " " + str(rand_pow_y))

        if self.print_map_during_steps:
            self.print_map()

        return self.calc_observation()

    # reinforcement learning framework functions
    def step(self, actions):
        is_possible_action = self.enemy.step_turn(actions)  # todo fix this
        # pg.time.delay(400)  # just for testing
        player_random_action = self.player.random_action()
        self.player.step_turn(player_random_action)
        for powerup in self.power_ups:
            if self.enemy.getX() == powerup.x and self.enemy.getY() == powerup.y:
                powerup.acquired_by(self.enemy)
            if self.player.getX() == powerup.x and self.player.getY() == powerup.y:
                powerup.acquired_by(self.player)
        self.player.update_shoot_and_feasible_moves()
        self.enemy.update_shoot_and_feasible_moves()
        observation = self.calc_observation()
        done = self.is_game_over()
        reward = self.calc_reward(done, is_possible_action)
        # update last action
        self.enemy.previus_action = actions

        if self.print_info_during_steps:
            print("L'azione: " + str(actions) + " ha prodotto un reward di Reward: " + str(reward))
        if self.print_map_during_steps:
            self.print_map()

        return observation, reward, done

    def calc_observation(self):
        observation = {}
        global_view = self.calculate_global_observation_matrix()
        observation["global_view"] = Game.to_one_hot_static(global_view, self.nums_values_channel)
        observation["local_view_0"] = Game.to_one_hot_static(self.calculate_local_observation_matrix(global_view, 3), self.nums_values_channel)
        observation["local_view_1"] = Game.to_one_hot_static(self.calculate_local_observation_matrix(global_view, 5), self.nums_values_channel)
        observation["property_view_0"] = self.calculate_vector_properties(self.enemy)
        observation["property_view_1"] = self.calculate_vector_properties(self.player)
        observation["prev_action"] = Game.to_one_hot_static(np.array(self.enemy.previus_action), 4)
        return observation

    def calculate_global_observation_matrix(self):
        #  Map Observations
        #     0 = free                                4 = exit
        #     1 = wall                                5 = power-up_1
        #     2 = player                              # 6 = power-up_2
        #     3 = agents/enemies - self if alone

        w, h = int(self.GRIDWIDTH / self.TILESIZE), int(self.GRIDHEIGHT / self.TILESIZE)
        global_matrix = [[0 for y in range(h)] for x in range(w)]
        #  walls
        for wall in self.walls:
            global_matrix[wall.x][wall.y] = 1
        #  player
        global_matrix[self.player.getX()][self.player.getY()] = 2
        #  self agent
        global_matrix[self.enemy.getX()][self.enemy.getY()] = 3
        #  exits
        for ex in self.exit:
            global_matrix[ex.getX()][ex.getY()] = 4
        #  powerups
        for powerup in self.power_ups:
            if powerup.effect == 0:
                global_matrix[powerup.x][powerup.y] = 5
            # else:
            #    global_matrix[powerup.x][powerup.y] = 6
        return np.array(global_matrix)

    def calculate_local_observation_matrix(self, global_matrix, n):
        #  Map Observations
        #     0 = free                                4 = exit
        #     1 = wall                                5 = power-up_1
        #     2 = player
        #     3 = agents/enemies - self if alone
        # print("local observation map:")
        matricx_local_nxn = [[0 for x in range(n)] for y in range(n)]
        cells = [int(i - (n-1)/2) for i in range(n)]
        delta_m = int((n-1)/2)
        for y in cells:
            for x in cells:
                mx, my = self.enemy.getX() + x, self.enemy.getY() + y  # just 1 enemy
                if 0 <= mx < self.GRIDWIDTH / self.TILESIZE and 0 <= my < self.GRIDHEIGHT / self.TILESIZE:
                    # print("   x,y: " + str(x) + " " + str(y) + "and mx,my: " + str(mx) + " " + str(my))
                    matricx_local_nxn[x+delta_m][y+delta_m] = global_matrix[mx][my]
                else:
                    matricx_local_nxn[x+delta_m][y+delta_m] = 1
        return np.array(matricx_local_nxn)

    def calculate_vector_properties(self, character):
        # hp            0 1 2
        # direction --> 8 x 4
        # range         7 6 5
        soglia_1 = character.max_hp + 1
        soglia_2 = soglia_1 + 8 + 1
        return [character.hp, soglia_1 + table_feasible_directions[str(character.direction)],soglia_2 + character.range_fire]

    def is_game_over(self):
        if self.player.hp <= 0 or self.enemy.hp <= 0:
            return True
        else:
            return False

    def calc_reward(self, done, is_possible_action):
        rew = -0.01
        if done and self.player.hp <= 0:
            rew += 10 * self.enemy.hp
        elif not is_possible_action:
            rew = -0.1
        return rew

    # generate map
    def generateMap(self):  # todo togliere power up secondo tipo
        # walls
        num_obstacles = random.randint(self.MIN_NUM_OBSTACLE, self.MAX_NUM_OBSTACLE)
        # print("wall generating:")
        for o in range(num_obstacles):
            rand_center_x = random.randint(3, self.GRIDWIDTH / self.TILESIZE-3)
            rand_center_y = random.randint(3, self.GRIDHEIGHT / self.TILESIZE-3)
            num_lines = random.randint(self.MIN_LINES_FOR_OBSTACLES, self.MAX_LINES_FOR_OBSTACLES)
            for l in range(num_lines):
                rand_x = int(np.random.normal(scale=3)) + rand_center_x
                rand_y = int(np.random.normal(scale=3)) + rand_center_y
                direct = random.randint(0, 3)
                lenght = random.randint(self.MIN_LENGHT_LINE, self.MAX_LENGHT_LINE)
                for x in range(lenght):
                    pos_x, pos_y = 0, 0
                    if direct == 0:
                        pos_x, pos_y = rand_x + x - int(lenght / 2), rand_y - int(lenght / 2)
                    elif direct == 1:
                        pos_x, pos_y = rand_x + int(lenght / 2), rand_y + x + int(lenght / 2)
                    elif direct == 2:
                        pos_x, pos_y = rand_x + x + int(lenght / 2), rand_y + x + int(lenght / 2)
                    elif direct == 3:
                        pos_x, pos_y = rand_x - x + int(lenght / 2), rand_y + x + int(lenght / 2)

                    if 0 < pos_x < int(self.GRIDWIDTH / self.TILESIZE) and 0 < pos_y < int(self.GRIDHEIGHT / self.TILESIZE) :
                        # print("    " + str(pos_x) + " " + str(pos_y))
                        self.walls.append(Wall(self, pos_x, pos_y))

    # online game functions
    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def close(self):
        pg.quit()
        sys.exit()

    def step_function_testing(self):  # just for testing
        action = self.enemy.random_action()  # just for testing
        self.step(action)  # just for testing
        pg.time.delay(400)  # just for testing
        self.player.update_shoot_and_feasible_moves()  # just for testing
        self.enemy.update_shoot_and_feasible_moves()  # just for testing

    def events(self):
        if self.SIMULTAING_ENVIROMENT:
            self.step_function_testing()  # just for testing
            return 0  # just for testing

        # check hover mouse
        events = pg.event.get()
        self.button_fire.listen(events)
        for block in self.player.feasible_move:
            if block.rect.collidepoint(pg.mouse.get_pos()):
                block.image.fill(GREEN)
            else:
                block.image.fill(LIGHTGREY)

        # catch all events here
        for event in events:
            # quit
            if event.type == pg.QUIT:
                self.close()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.close()
            # player turn
            if event.type == pg.MOUSEBUTTONUP:
                # check feasible player move
                for block in self.player.feasible_move:
                    if block.rect.collidepoint(pg.mouse.get_pos()):
                        dx = int(block.rect.x / TILESIZE) - self.player.x
                        dy = int(block.rect.y / TILESIZE) - self.player.y
                        self.player.move(dx, dy)
                        # check powerup
                        for powerup in self.power_ups:
                            if self.player.x == powerup.x and self.player.y == powerup.y:
                                powerup.acquired_by(self.player)
                        # check win
                        for exit in self.exit:
                            if self.player.x == exit.x and self.player.y == exit.y:
                                print("win")
            if event.type == PLAYER_SHOOT_EVENT:
                self.player.shoot_fire()

            # enemy turn
            if event.type == ENEMY_TURN_EVENT:
                pg.time.delay(100)
                enemy_action = self.enemy.random_action()
                self.enemy.step_turn(enemy_action)
                for powerup in self.power_ups:
                    if self.enemy.getX() == powerup.x and self.enemy.getY() == powerup.y:
                        powerup.acquired_by(self.enemy)
                self.player.update_shoot_and_feasible_moves()
                self.enemy.update_shoot_and_feasible_moves()

    # draw funcions
    def update(self):
        # update portion of the game loop
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, self.GRIDWIDTH + self.TILESIZE, self.TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, self.GRIDHEIGHT))
        for y in range(0, self.GRIDHEIGHT + self.TILESIZE, self.TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (self.GRIDWIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        pg.draw.rect(self.screen, SETTING_COLOR, (self.GRIDWIDTH, 0, self.SETTING_WIDTH, self.SETTING_HEIGHT))
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.button_fire.draw()
        pg.display.flip()

    def print_map(self):
        glb_m = self.calculate_global_observation_matrix()
        glb_m = glb_m.T
        df = pandas.DataFrame(glb_m)
        df[self.player.getX()][self.player.getY()] = "###"
        df[self.enemy.getX()][self.enemy.getY()] = "!!!"
        print(tabulate(df, headers='keys', tablefmt='fancy_grid'))
