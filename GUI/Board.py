import Matrix
import Player
import pygame
from Bomb import *
from PowerUp import *
from Fire import *

# Constants
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
ORANGE = (230, 126, 34)
LIGHT_BLUE = (0, 255, 255)
BLOCK_SIZE = 50
ROWS = 12
COLUMNS = 18

class Board:

    __instance = None
    matrix = Matrix.Matrix.get_instance()
    board_matrix = matrix.get_matrix()
    players = pygame.sprite.Group()

    @staticmethod
    def get_instace():

        if Board.__instance is None:
            return Board()

        return Board.__instance

    def __init__(self):

        if Board.__instance is not None:
            raise Exception("A board has already been created!")
        else:
            Board.__instance = self
            self.create_players_group()

    def draw_base(self, SCREEN):

        pos_x = 5
        pos_y = 2

        for x in range(pos_x, COLUMNS + pos_x):
            for y in range(pos_y, ROWS + pos_y):

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

                rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(SCREEN, color, rect)

    def draw_board(self, SCREEN):

        x = 5
        y = 2

        for i in self.board_matrix:
            for j in i:

                if not isinstance(j, Matrix.Blank):

                    if isinstance(j, Unbreakable):
                        rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                        pygame.draw.rect(SCREEN, LIGHT_GREY, rect)
                    elif isinstance(j, Breakable):
                        rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                        pygame.draw.rect(SCREEN, BROWN, rect)
                    elif isinstance(j, Player.User):
                        user = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                        pygame.draw.rect(SCREEN, YELLOW, user)
                    elif isinstance(j, Player.Enemy):
                        enemy = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                        pygame.draw.rect(SCREEN, RED, enemy)
                    elif isinstance(j, Bomb):
                        bomb = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                        pygame.draw.rect(SCREEN, BLACK, bomb)
                    elif isinstance(j, Shoe):
                        power_up = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                        pygame.draw.rect(SCREEN, PURPLE, power_up)
                    elif isinstance(j, CrossBomb):
                        power_up = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                        pygame.draw.rect(SCREEN, ORANGE, power_up)
                    elif isinstance(j, Shield):
                        power_up = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                        pygame.draw.rect(SCREEN, BLUE, power_up)
                    elif isinstance(j, Healing):
                        power_up = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                        pygame.draw.rect(SCREEN, PINK, power_up)
                    elif isinstance(j, Fire):
                        fire = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                        pygame.draw.rect(SCREEN, LIGHT_BLUE, fire)

                x = x + 1

            x = 5
            y = y + 1

    def create_players_group(self):

        self.players.add(self.matrix.user)
        self.players.add(self.matrix.enemy0)
        self.players.add(self.matrix.enemy1)
        self.players.add(self.matrix.enemy2)
        self.players.add(self.matrix.enemy3)
        self.players.add(self.matrix.enemy4)
        self.players.add(self.matrix.enemy5)
        self.players.add(self.matrix.enemy6)

    def create_power_up(self, frame):

        """
        Method that spreads the power ups randomly in the matrix
        :param frame
        :return: void
        """

        # 6000 approximately every 14 secs
        # 9000 approximately every 24 secs
        # 12000 approximately 30 secs
        if frame % 500 == 0:

            power_up = PowerUp([0, 0], self.matrix)

    def put_out_fire(self, frame):

        """
        Method that changes fire objects to blank objects after a explosion
        :param frame
        :return: void
        """

        row = self.matrix.user.get_x()
        column = self.matrix.user.get_y()

        if frame % 1000 == 0:

            if self.matrix.user.cross_bomb == True:

                for i in range(0, ROWS): # Vertical change

                    if isinstance(self.board_matrix[i][column], Fire):
                        self.board_matrix[i][column] = Matrix.Blank((i, column))
                        self.reduce_enemy_live(row, column)

                for j in range(0, COLUMNS): # Horizontal change

                    if isinstance(self.board_matrix[row][j], Fire):
                        self.board_matrix[row][j] = Matrix.Blank((row, j))
                        self.reduce_enemy_live(row, column)

                self.matrix.user.cross_bomb_time = 0
                self.matrix.user.cross_bomb = False
                self.return_enemies()

    def return_enemies(self):

        """
        Method that returns the enemies to the matrix after a cross bomb power up
        :return: void
        """

        x = self.matrix.enemy0.get_x()
        y = self.matrix.enemy0.get_y()
        self.board_matrix[x][y] = self.matrix.enemy0

        x = self.matrix.enemy1.get_x()
        y = self.matrix.enemy1.get_y()
        self.board_matrix[x][y] = self.matrix.enemy1

        x = self.matrix.enemy2.get_x()
        y = self.matrix.enemy2.get_y()
        self.board_matrix[x][y] = self.matrix.enemy2

        x = self.matrix.enemy3.get_x()
        y = self.matrix.enemy3.get_y()
        self.board_matrix[x][y] = self.matrix.enemy3

        x = self.matrix.enemy4.get_x()
        y = self.matrix.enemy4.get_y()
        self.board_matrix[x][y] = self.matrix.enemy4

        x = self.matrix.enemy5.get_x()
        y = self.matrix.enemy5.get_y()
        self.board_matrix[x][y] = self.matrix.enemy5

        x = self.matrix.enemy6.get_x()
        y = self.matrix.enemy6.get_y()
        self.board_matrix[x][y] = self.matrix.enemy6

    def reduce_enemy_live(self, row, column):

        """
        Method that decreases enemies live when a bomb touches them
        :param row
        :param column
        :return: void
        """

        x = self.matrix.enemy0.get_x()
        y = self.matrix.enemy0.get_y()

        if x == row and y == column:
            self.matrix.enemy0.lives -= 1

        x = self.matrix.enemy1.get_x()
        y = self.matrix.enemy1.get_y()

        if x == row and y == column:
            self.matrix.enemy1.lives -= 1

        x = self.matrix.enemy2.get_x()
        y = self.matrix.enemy2.get_y()

        if x == row and y == column:
            self.matrix.enemy2.lives -= 1

        x = self.matrix.enemy3.get_x()
        y = self.matrix.enemy3.get_y()

        if x == row and y == column:
            self.matrix.enemy3.lives -= 1

        x = self.matrix.enemy4.get_x()
        y = self.matrix.enemy4.get_y()

        if x == row and y == column:
            self.matrix.enemy4.lives -= 1

        x = self.matrix.enemy5.get_x()
        y = self.matrix.enemy5.get_y()

        if x == row and y == column:
            self.matrix.enemy5.lives -= 1

        x = self.matrix.enemy6.get_x()
        y = self.matrix.enemy6.get_y()

        if x == row and y == column:
            self.matrix.enemy6.lives -= 1
