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
LIGHT_GREEN = (120, 187, 82)
DARK_GREEN = (113, 177, 76)
DARK_GREY = (61, 64, 75)
LIGHT_GREY = (145, 147, 156)
BROWN = (169, 109, 69)
YELLOW = (233, 247, 14)
RED = (247, 14, 14)
BLACK = (0, 0, 0)
BLUE = (0, 168, 187)
PURPLE = (108, 52, 131)
PINK = (240, 54, 192)
WHITE = (255, 255, 255)
ORANGE = (230, 126, 34)
TIME_BETWEEN_POWER_UPS = 10000

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
            self.BLOCK_SIZE = int(2 * self.WIDTH / 60)

            images = Image.get_instance(self.BLOCK_SIZE)


    def draw_base(self, SCREEN):
        """
        Draws the base of the game board as it
        was a matrix fulled with Blanck objects
        """
        start_x = 7
        start_y = 3
        # Alternates the colors of  the blank spaces
        for x in range(start_x, COLUMNS + start_x + 2):
            for y in range(start_y, ROWS + start_y + 2):
                if x == start_x or x == (COLUMNS + start_x + 1) or y == start_y or y == (ROWS + start_y + 1):
                    color = DARK_GREY
                else:
                    if x % 2 == 0:
                        if y % 2 == 0:
                            color = LIGHT_GREEN
                        else:
                            color = DARK_GREEN
                    else:
                        if y % 2 == 0:
                            color = DARK_GREEN
                        else:
                            color = LIGHT_GREEN

                rect = pygame.Rect(x * self.BLOCK_SIZE, y * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE)
                pygame.draw.rect(SCREEN, color, rect)

    def draw_board(self, SCREEN):
        """
        Method that draws the game matrix, updates the matrix
        everytime it is called
        """
        x = 8
        y = 4
        row = 0
        column = 0
        for i in self.board_matrix:
            for j in i:  # j represents every object in the matrix
                if not isinstance(j, Blank):
                    if isinstance(j, Unbreakable):
                        # Unbreakable blocks will have light gray color
                        rect = pygame.Rect(x * self.BLOCK_SIZE, y * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE)
                        pygame.draw.rect(SCREEN, LIGHT_GREY, rect)
                    elif isinstance(j, Breakable):
                        # Breakable blocks will have brown color
                        rect = pygame.Rect(x * self.BLOCK_SIZE, y * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE)
                        pygame.draw.rect(SCREEN, BROWN, rect)
                    elif isinstance(j, User):
                        # Users will have yellow color
                        user = pygame.Rect(x * self.BLOCK_SIZE, y * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE)
                        pygame.draw.rect(SCREEN, YELLOW, user)
                    elif isinstance(j, Enemy):
                        # Enemies will have red color
                        enemy = pygame.Rect(x * self.BLOCK_SIZE, y * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE)
                        pygame.draw.rect(SCREEN, RED, enemy)
                    elif isinstance(j, Bomb):
                        detonated_bomb = self.board_matrix[row][column]
                        # Bombs will have black color
                        bomb = pygame.Rect(x * self.BLOCK_SIZE, y * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE)
                        pygame.draw.rect(SCREEN, BLACK, bomb)
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
                        power_up = pygame.Rect(x * self.BLOCK_SIZE, y * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE)
                        pygame.draw.rect(SCREEN, PURPLE, power_up)
                    elif isinstance(j, CrossBomb):
                        # Crossbomb power ups will have white color
                        power_up = pygame.Rect(x * self.BLOCK_SIZE, y * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE)
                        pygame.draw.rect(SCREEN, WHITE, power_up)
                    elif isinstance(j, Shield):
                        # Shield power ups will have blue color
                        power_up = pygame.Rect(x * self.BLOCK_SIZE, y * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE)
                        pygame.draw.rect(SCREEN, BLUE, power_up)
                    elif isinstance(j, Healing):
                        # Healing power ups will have pink color
                        power_up = pygame.Rect(x * self.BLOCK_SIZE, y * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE)
                        pygame.draw.rect(SCREEN, PINK, power_up)
                    elif isinstance(j, Fire):
                        # Fire positions will have orange color
                        fire = pygame.Rect(x * self.BLOCK_SIZE, y * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE)
                        pygame.draw.rect(SCREEN, ORANGE, fire)
                        # The fire stops after a certain amount of time defined in Fire.py
                        off_fire = j.check_fire_state()
                        if off_fire:
                            self.create_blank((row, column))

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
                print(str(bomb_owner)+" "+"kills: "+str(bomb_owner.kills))
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
