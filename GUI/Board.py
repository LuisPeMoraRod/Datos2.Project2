from Matrix import *
from PowerUp import *
from Fire import *
from Route import *
import random
import pygame.time
from GUI.Window import *
from GUI.Image import *
from Bomb import *
import pyautogui
import PlayersList
import threading

# constants

TIME_BETWEEN_POWER_UPS = 9000
TIME_BETWEEN_VELOCITY_UPDATE = 3000
TIME_BETWEEN_DETONATION_UPDATE = 3000

ROWS = 12
COLUMNS = 14


class Board:
    # Class constants
    __instance = None
    matrix = Matrix.Matrix.get_instance()
    board_matrix = matrix.get_matrix()
    users = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    enable_up = True
    enable_down = True
    enable_left = True
    enable_right = True

    @staticmethod
    def get_instance(window_width, window_height):
        """
        Singleton method get_instance()
        returns the only Board in the game or
        a new one if there is no Board
        """
        if Board.__instance is None:
            print(window_width, window_height)
            return Board(window_width, window_height)
        return Board.__instance

    def __init__(self, window_width, window_heigth):
        """
        Class constructor
        """
        if Board.__instance is not None:
            raise Exception("A board has already been created!")
        else:
            Board.__instance = self
            self.create_players_group()
            self.killed_player = None
            self.killed_player_row = 0
            self.killed_player_column = 0
            self.last_power_up_time = pygame.time.get_ticks()
            self.last_velocity_update = pygame.time.get_ticks()
            self.last_detonation_time_update = pygame.time.get_ticks()
            self.WIDTH = window_width
            self.HEIGHT = window_heigth
            self.BLOCK_SIZE = int(self.WIDTH / 30)
            self.images = Image.get_instance(self.BLOCK_SIZE)
            self.alive_players = []
            self.amount_of_alive_players = 8

    def draw_base(self, SCREEN):
        """
        Draws the base of the game board as it
        was a matrix fulled with Blanck objects
        """
        start_x = self.WIDTH / 2 - self.BLOCK_SIZE * COLUMNS / 2 - self.BLOCK_SIZE
        start_y = self.HEIGHT / 2 - self.BLOCK_SIZE * ROWS / 2 - self.BLOCK_SIZE
        # Alternates the colors of  the blank spaces

        light_grass = True
        dark_grass = False

        x = start_x
        y = start_y

        while y < start_y + self.BLOCK_SIZE * ROWS + 2 * self.BLOCK_SIZE:
            while x < start_x + self.BLOCK_SIZE * COLUMNS + 2 * self.BLOCK_SIZE:
                if x == start_x or x == start_x + self.BLOCK_SIZE * COLUMNS + self.BLOCK_SIZE or y == start_y or y == start_y + self.BLOCK_SIZE * ROWS + self.BLOCK_SIZE:
                    element = self.images.border
                else:
                    if light_grass:
                        light_grass = False
                        dark_grass = True
                        element = self.images.light_grass
                    elif dark_grass:
                        dark_grass = False
                        light_grass = True
                        element = self.images.dark_grass
                SCREEN.blit(element, (x, y))
                x = x + self.BLOCK_SIZE
            light_grass = not light_grass
            dark_grass = not dark_grass
            x = start_x
            y = y + self.BLOCK_SIZE

    def draw_board(self, SCREEN):
        """
        Method that draws the game matrix, updates the matrix
        everytime it is called
        """

        start_x = self.WIDTH / 2 - (self.BLOCK_SIZE * COLUMNS / 2)
        start_y = self.HEIGHT / 2 - (self.BLOCK_SIZE * ROWS / 2)
        x = start_x
        y = start_y
        row = 0
        column = 0
        for i in self.board_matrix:
            for j in i:  # j represents every object in the matrix
                if not isinstance(j, Blank):
                    if isinstance(j, Unbreakable):
                        # Unbreakable blocks will have light gray color
                        element = self.images.unbreakable_block
                    elif isinstance(j, Breakable):
                        # Breakable blocks will have brown color
                        element = self.images.breakable_block
                    elif isinstance(j, User):
                        # Users will have yellow color
                        element = self.images.user
                    elif isinstance(j, Enemy):
                        # Enemies will have red color
                        if j is self.matrix.enemy0:
                            element = self.images.enemy0
                        elif j is self.matrix.enemy1:
                            element = self.images.enemy1
                        elif j is self.matrix.enemy2:
                            element = self.images.enemy2
                        elif j is self.matrix.enemy3:
                            element = self.images.enemy3
                        elif j is self.matrix.enemy4:
                            element = self.images.enemy4
                        elif j is self.matrix.enemy5:
                            element = self.images.enemy5
                        elif j is self.matrix.enemy6:
                            element = self.images.enemy6
                    elif isinstance(j, Bomb):
                        detonated_bomb = self.board_matrix[row][column]
                        # Bombs will have black color
                        element = self.images.bomb
                        # Bomb detonates after a certain amount of time defined in Bomb.py
                        detonate_bomb = j.detonate()
                        if detonate_bomb:
                            bomb_owner = detonated_bomb.player
                            # This iteration controls the places that will convert into Fire
                            # during an explosion
                            for k in range(1, j.radius):
                                # j.radius represents the radius of the bomb
                                if row - k >= 0 and self.enable_up:
                                    self.enable_up = self.create_fire((j.position[0] - k, column), bomb_owner)
                                if row + k < ROWS and self.enable_down:
                                    self.enable_down = self.create_fire((j.position[0] + k, column), bomb_owner)
                                if column - k >= 0 and self.enable_left:
                                    self.enable_left = self.create_fire((row, j.position[1] - k), bomb_owner)
                                if column + k < COLUMNS and self.enable_right:
                                    self.enable_right = self.create_fire((row, j.position[1] + k), bomb_owner)
                            self.board_matrix[row][column] = Fire((row, column))
                        self.restart_enables()
                    elif isinstance(j, Shoe):
                        # Shoe power ups will have purple color
                        element = self.images.shoe
                    elif isinstance(j, CrossBomb):
                        # Crossbomb power ups will have white color
                        element = self.images.cross_bomb
                    elif isinstance(j, Shield):
                        # Shield power ups will have blue color
                        element = self.images.shield
                    elif isinstance(j, Healing):
                        # Healing power ups will have pink color
                        element = self.images.healing
                    elif isinstance(j, Fire):
                        # Fire positions will have orange color
                        element = self.images.fire
                        # The fire stops after a certain amount of time defined in Fire.py
                        off_fire = j.check_fire_state()
                        if off_fire:
                            self.create_blank((row, column))

                    SCREEN.blit(element, (x, y))
                x = x + self.BLOCK_SIZE
                column = column + 1
            x = start_x
            column = 0

            row = row + 1
            y = y + self.BLOCK_SIZE

    def create_players_group(self):
        """
        Defines the sprites needed in the game
        """
        self.users.add(self.matrix.user)
        self.enemies.add(self.matrix.enemy0)
        self.enemies.add(self.matrix.enemy1)
        self.enemies.add(self.matrix.enemy2)
        self.enemies.add(self.matrix.enemy3)
        self.enemies.add(self.matrix.enemy4)
        self.enemies.add(self.matrix.enemy5)
        self.enemies.add(self.matrix.enemy6)

    def create_power_up(self, actual_time):
        """
        Auxiliary method to create power ups every certain
        amount of time in the matrix
        """
        if self.amount_of_alive_players < 3:
            return
        power_ups = self.count_power_ups()
        # A power up will be generated after a certain amount of time
        if actual_time - self.last_power_up_time > TIME_BETWEEN_POWER_UPS and power_ups < 3:  # Maximum 3 power ups at the same time
            self.last_power_up_time = actual_time
            power_up_number = random.randint(0, 3)  # Random power up
            if power_up_number == 0:
                crossbomb = CrossBomb(self.matrix)
                self.matrix.matrix[crossbomb.get_x()][crossbomb.get_y()] = crossbomb
            elif power_up_number == 1:
                healing = Healing(self.matrix)
                self.matrix.matrix[healing.get_x()][healing.get_y()] = healing
            elif power_up_number == 2:
                shield = Shield(self.matrix)
                self.matrix.matrix[shield.get_x()][shield.get_y()] = shield
            elif power_up_number == 3:
                shoe = Shoe(self.matrix)
                self.matrix.matrix[shoe.get_x()][shoe.get_y()] = shoe

    def change_velocity(self, actual_time):
        if actual_time - self.last_velocity_update > TIME_BETWEEN_VELOCITY_UPDATE:
            self.last_velocity_update = actual_time
            for enemy in PlayersList.PlayersList.get_instance().players_list:
                if enemy.velocity < 1700:
                    enemy.velocity += 50

    def change_detonation_time(self, actual_time):
        if actual_time - self.last_detonation_time_update > TIME_BETWEEN_DETONATION_UPDATE:
            self.last_detonation_time_update = actual_time
            if Bomb.TIME_TO_DETONATE >= 1500:
                Bomb.TIME_TO_DETONATE -= 10

    def count_power_ups(self):
        counter = 0
        for i in range(len(self.board_matrix)):
            for j in range(len(self.board_matrix[i])):
                if isinstance(self.board_matrix[i][j], PowerUp):
                    counter += 1
        return counter

    def create_fire(self, position, bomb_owner):
        """
        Method that creates the fire objects needed in the explosion
        :brief: The fire doesn't destruct bombs nor unbreakable blocks
        always makes a player loose a live and destructs the Breakable
        blocks and the power ups
        """
        row = position[0]
        column = position[1]
        element = self.board_matrix[row][column]
        if not isinstance(element, Unbreakable) and not isinstance(element, Bomb):
            if isinstance(element, User) or isinstance(element, Enemy):
                bomb_owner.kills += 1
                #element.is_movement_denied = True
                self.killed_player_row = row
                self.killed_player_column = column
                element.lose_live("Kill")
                self.killed_player = element
            self.board_matrix[row][column] = Fire(position)
            if isinstance(element, Breakable) or isinstance(element, Bomb):
                return False
            return True
        else:
            return False

    def create_blank(self, position):
        """
        This method restores the object after every explosion
        considers if there was player underneath and if the Fire killed him
        """
        row = position[0]
        column = position[1]
        if self.killed_player_row == row \
                and self.killed_player_column == column\
                and isinstance(self.killed_player, Player.Player)\
                and self.killed_player.lives > 0:
            self.board_matrix[row][column] = self.killed_player
            self.killed_player = None
        else:
            self.board_matrix[row][column] = Blank((row, column))

    def restart_enables(self):
        """
        Auxiliary method used to reset values
        used to control the fire in draw board
        """
        self.enable_up = True
        self.enable_right = True
        self.enable_left = True
        self.enable_down = True

    def draw_stats(self, screen):

        e_portrait_width = self.images.e0_portrait.get_width()
        e_portrait_height = self.images.e0_portrait.get_height()
        pu_stat_width = self.images.cross_bomb_e_stat.get_width()
        pu_stat_height = self.images.cross_bomb_e_stat.get_height()

        pos_x = self.WIDTH - 0.99 * self.WIDTH + e_portrait_width + 2
        start_y = self.HEIGHT - 0.9 * self.HEIGHT

        self.draw_portraits(screen)

        self.draw_epu_stats(pos_x, start_y, screen, self.matrix.enemy0)
        self.draw_epu_stats(pos_x, start_y + self.BLOCK_SIZE * 2 + 1, screen, self.matrix.enemy1)
        self.draw_epu_stats(pos_x, start_y + self.BLOCK_SIZE * 4 + 1, screen, self.matrix.enemy2)
        self.draw_epu_stats(pos_x, start_y + self.BLOCK_SIZE * 6 + 1, screen, self.matrix.enemy3)
        self.draw_epu_stats(pos_x, start_y + self.BLOCK_SIZE * 8 + 1, screen, self.matrix.enemy4)
        self.draw_epu_stats(pos_x, start_y + self.BLOCK_SIZE * 10 + 1, screen, self.matrix.enemy5)
        self.draw_epu_stats(pos_x, start_y + self.BLOCK_SIZE * 12 + 1, screen, self.matrix.enemy6)

        self.draw_upu_stats(screen, self.matrix.user)

    def draw_titles(self, screen):

        game_name = self.images.title
        enemy_title = self.images.enemy_title

        screen.blit(enemy_title, (self.WIDTH - 0.95 * self.WIDTH, self.HEIGHT - 0.98 * self.HEIGHT))
        screen.blit(game_name, (self.WIDTH / 2 - (game_name.get_width() / 2), self.HEIGHT - 0.99 * self.HEIGHT))

    def draw_epu_stats(self, pos_x, pos_y, screen, player):

        e_portrait_width = self.images.e0_portrait.get_width()
        e_portrait_height = self.images.e0_portrait.get_height()
        pu_stat_width = self.images.cross_bomb_e_stat.get_width()
        pu_stat_height = self.images.cross_bomb_e_stat.get_height()

        shoe_stat, shield_stat, cross_bomb_stat = self.check_power_up(player)

        screen.blit(shoe_stat, (pos_x, pos_y + 10))
        screen.blit(shield_stat, (pos_x, pos_y + e_portrait_height / 2 - pu_stat_height / 2))
        screen.blit(cross_bomb_stat, (pos_x, pos_y + e_portrait_height - pu_stat_height - 10))

        lb_lives = self.generate_label(int(0.35 * self.BLOCK_SIZE), "Lives: " + str(player.lives))
        lb_velocity = self.generate_label(int(0.35 * self.BLOCK_SIZE), "Velocity: " + str(player.velocity))
        lb_explosion_radius = self.generate_label(int(0.35 * self.BLOCK_SIZE),
                                                  "Bomb radius: " + str(player.explosion_radius))
        lb_evasion = self.generate_label(int(0.35 * self.BLOCK_SIZE), "Evasion: " + str(player.evasion))
        screen.blit(lb_lives, (pos_x + pu_stat_width + 10, pos_y + 10))
        screen.blit(lb_velocity, (pos_x + pu_stat_width + 10, pos_y + 10 + 0.35 * self.BLOCK_SIZE))
        screen.blit(lb_explosion_radius, (pos_x + pu_stat_width + 10, pos_y + 10 + 2 * (0.35 * self.BLOCK_SIZE)))
        screen.blit(lb_evasion, (pos_x + pu_stat_width + 10, pos_y + 10 + 3 * (0.35 * self.BLOCK_SIZE)))

    def draw_upu_stats(self, screen, player):

        u_portrait_height = self.images.user_portrait.get_height()
        u_portrait_width = self.images.user_portrait.get_width()
        pos_x = self.WIDTH - 0.18 * self.WIDTH
        pos_y = self.HEIGHT - 0.9 * self.HEIGHT + + self.BLOCK_SIZE + 2 + u_portrait_height + 10

        shoe_stat, shield_stat, cross_bomb_stat = self.check_power_up(player)

        lb_lives = self.generate_label(int(0.5 * self.BLOCK_SIZE), "Lives: " + str(player.lives))

        screen.blit(shoe_stat, (pos_x, pos_y))
        screen.blit(shield_stat, (pos_x + u_portrait_width / 2 - shield_stat.get_width() / 2, pos_y))
        screen.blit(cross_bomb_stat, (pos_x + u_portrait_width - cross_bomb_stat.get_width(), pos_y))
        screen.blit(lb_lives, (pos_x, pos_y + shoe_stat.get_height() + 10))

    def check_power_up(self, player):

        if isinstance(player, Enemy):
            if player.has_shoe:
                shoe_stat = self.images.shoe_e_collected
            else:
                shoe_stat = self.images.shoe_e_stat
            if player.has_shield:
                shield_stat = self.images.shield_e_collected
            else:
                shield_stat = self.images.shield_e_stat
            if player.has_cross_bomb:
                cross_bomb_stat = self.images.cross_bomb_e_collected
            else:
                cross_bomb_stat = self.images.cross_bomb_e_stat

        else:
            if player.has_shoe:
                shoe_stat = self.images.shoe_u_collected
            else:
                shoe_stat = self.images.shoe_u_stat
            if player.has_shield:
                shield_stat = self.images.shield_u_collected
            else:
                shield_stat = self.images.shield_u_stat
            if player.has_cross_bomb:
                cross_bomb_stat = self.images.cross_bomb_u_collected
            else:
                cross_bomb_stat = self.images.cross_bomb_u_stat

        return shoe_stat, shield_stat, cross_bomb_stat

    def draw_portraits(self, screen):
        pos_x = self.WIDTH - 0.99 * self.WIDTH
        start_y = self.HEIGHT - 0.9 * self.HEIGHT

        e0p = self.images.e0_portrait
        e1p = self.images.e1_portrait
        e2p = self.images.e2_portrait
        e3p = self.images.e3_portrait
        e4p = self.images.e4_portrait
        e5p = self.images.e5_portrait
        e6p = self.images.e6_portrait
        user_p = self.images.user_portrait

        screen.blit(e0p, (pos_x, start_y))
        screen.blit(e1p, (pos_x, start_y + self.BLOCK_SIZE * 2 + 1))
        screen.blit(e2p, (pos_x, start_y + self.BLOCK_SIZE * 4 + 1))
        screen.blit(e3p, (pos_x, start_y + self.BLOCK_SIZE * 6 + 1))
        screen.blit(e4p, (pos_x, start_y + self.BLOCK_SIZE * 8 + 1))
        screen.blit(e5p, (pos_x, start_y + self.BLOCK_SIZE * 10 + 1))
        screen.blit(e6p, (pos_x, start_y + self.BLOCK_SIZE * 12 + 1))
        screen.blit(user_p, (self.WIDTH - 0.18 * self.WIDTH, start_y + self.BLOCK_SIZE + 2))

    def generate_label(self, size, text):

        my_font = pygame.font.SysFont("monospace", size)
        label = my_font.render(text, 1, (255, 255, 255))

        return label

    def check_alive_players(self):
        """
        Checks the amount of players that haven't lost yet
        and save them in a list attribute
        """
        alive_players_list = []
        alive_players_count = 0
        for player in PlayersList.PlayersList.get_instance().players_list:
            if player.lives > 0:
                alive_players_count += 1
                alive_players_list.append(player)
        self.amount_of_alive_players = alive_players_count
        self.alive_players = alive_players_list
