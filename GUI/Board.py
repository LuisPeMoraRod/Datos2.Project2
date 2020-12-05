from Matrix import *
from PowerUp import *
from Fire import *
from Route import *
import random
import pygame.time
from GUI.Window import *
from GUI.Image import *
import pyautogui

# constants
TIME_BETWEEN_POWER_UPS = 5000

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
            self.WIDTH = window_width
            self.HEIGHT = window_heigth
            self.BLOCK_SIZE = int(self.WIDTH / 30)

            self.images = Image.get_instance(self.BLOCK_SIZE)


    def draw_base(self, SCREEN):
        """
        Draws the base of the game board as it
        was a matrix fulled with Blanck objects
        """
        start_x = 7
        start_y = 2
        # Alternates the colors of  the blank spaces
        for x in range(start_x, COLUMNS + start_x + 2):
            for y in range(start_y, ROWS + start_y + 2):
                if x == start_x or x == (COLUMNS + start_x + 1) or y == start_y or y == (ROWS + start_y + 1):
                    element = self.images.border
                else:
                    if x % 2 == 0:
                        if y % 2 == 0:
                            element = self.images.light_grass
                        else:
                            element = self.images.dark_grass
                    else:
                        if y % 2 == 0:
                            element = self.images.dark_grass
                        else:
                            element = self.images.light_grass
                SCREEN.blit(element, (x * self.BLOCK_SIZE, y * self.BLOCK_SIZE))

    def draw_board(self, SCREEN):
        """
        Method that draws the game matrix, updates the matrix
        everytime it is called
        """
        x = 8
        y = 3
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
                        # Bombs will have black color
                        element = self.images.bomb
                        # Bomb detonates after a certain amount of time defined in Bomb.py
                        detonate_bomb = j.detonate()
                        if detonate_bomb:
                            # This iteration controls the places that will convert into Fire
                            # during an explosion
                            for k in range(1, j.radius):
                                # j.radius represents the radius of the bomb
                                if row - k >= 0 and self.enable_up:
                                    self.enable_up = self.create_fire((j.position[0] - k, column))
                                if row + k < ROWS and self.enable_down:
                                    self.enable_down = self.create_fire((j.position[0] + k, column))
                                if column - k >= 0 and self.enable_left:
                                    self.enable_left = self.create_fire((row, j.position[1] - k))
                                if column + k < COLUMNS and self.enable_right:
                                    self.enable_right = self.create_fire((row, j.position[1] + k))
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

                    SCREEN.blit(element, (x * self.BLOCK_SIZE, y * self.BLOCK_SIZE))
                x = x + 1
                column = column + 1
            x = 8
            column = 0

            row = row + 1
            y = y + 1

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
        # A power up will be generated after a certain amount of time
        if actual_time - self.last_power_up_time > TIME_BETWEEN_POWER_UPS:
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

    def create_fire(self, position):
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
                self.killed_player = element.lose_live()
                self.killed_player_row = row
                self.killed_player_column = column
                if self.killed_player is None:  # This happens when the player dies
                    self.board_matrix[row][column] = Fire(position)
                    return True
                # When the player is being bombed the movement stops
                self.killed_player.is_movement_denied = True
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
        if self.killed_player is None:
            self.board_matrix[row][column] = Blank((row, column))
        elif self.killed_player_row == row \
                and self.killed_player_column == column:
            self.board_matrix[row][column] = self.killed_player
            self.killed_player.is_movement_denied = False
            self.killed_player = None

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

        self.draw_pu_stats(pos_x, start_y, screen, self.matrix.enemy0)
        self.draw_pu_stats(pos_x, start_y + self.BLOCK_SIZE * 2 + 1, screen, self.matrix.enemy1)
        self.draw_pu_stats(pos_x, start_y + self.BLOCK_SIZE * 4 + 1, screen, self.matrix.enemy2)
        self.draw_pu_stats(pos_x, start_y + self.BLOCK_SIZE * 6 + 1, screen, self.matrix.enemy3)
        self.draw_pu_stats(pos_x, start_y + self.BLOCK_SIZE * 8 + 1, screen, self.matrix.enemy4)
        self.draw_pu_stats(pos_x, start_y + self.BLOCK_SIZE * 10 + 1, screen, self.matrix.enemy5)
        self.draw_pu_stats(pos_x, start_y + self.BLOCK_SIZE * 12 + 1, screen, self.matrix.enemy6)


    def draw_titles(self, screen):

        game_name = self.images.title
        enemy_title = self.images.enemy_title

        screen.blit(enemy_title, (self.WIDTH - 0.95*self.WIDTH, self.HEIGHT - 0.98*self.HEIGHT))
        screen.blit(game_name, (self.WIDTH/2 - (game_name.get_width()/2), self.HEIGHT - 0.99*self.HEIGHT))

    def draw_pu_stats(self, pos_x, pos_y, screen, enemy):

        e_portrait_width = self.images.e0_portrait.get_width()
        e_portrait_height = self.images.e0_portrait.get_height()
        pu_stat_width = self.images.cross_bomb_e_stat.get_width()
        pu_stat_height = self.images.cross_bomb_e_stat.get_height()

        if enemy.has_shoe:
            shoe_stat = self.images.shoe_e_collected
        else:
            shoe_stat = self.images.shoe_e_stat
        if enemy.has_shield:
            shield_stat = self.images.shield_e_collected
        else:
            shield_stat = self.images.shield_e_stat
        if enemy.has_cross_bomb:
            cross_bomb_stat = self.images.cross_bomb_e_collected
        else:
            cross_bomb_stat = self.images.cross_bomb_e_stat

        screen.blit(shoe_stat, (pos_x, pos_y +10))
        screen.blit(shield_stat, (pos_x, pos_y + e_portrait_height/2 - pu_stat_height/2))
        screen.blit(cross_bomb_stat, (pos_x, pos_y + e_portrait_height - pu_stat_height-10))

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