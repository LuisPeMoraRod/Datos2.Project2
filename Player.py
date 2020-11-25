import Matrix
import pygame
from Bomb import *
from PowerUp import *

# Constants
TIME_BETWEEN_MOVEMENTS = 150


class Player (pygame.sprite.Sprite):

    """
    Class for player objects.
    """

    def __init__(self, position, matrix):

        """
        Player constructor
        :param position: list
        :param matrix: Matrix
        """

        super().__init__()
        # Position attributes
        self.matrix = matrix.matrix
        self.position = position

        # Bomb control attribute
        self.new_bomb = False

        # Movement attributes
        self.last_movement_time = pygame.time.get_ticks()

        # Power ups attributes
        self.cross_bomb = False
        self.shield = False
        self.shoe = False

    def get_x(self):
        return self.position[0]

    def get_y(self):
        return self.position[1]

    def move_right(self):

        """
        Method that moves the player to the right in the matrix
        """

        pos_i = self.get_x()
        pos_j = self.get_y()

        if not pos_j < Matrix.COLUMNS - 1:
            return ""

        if isinstance(self.matrix[pos_i][pos_j + 1], Matrix.Blank):
            self.matrix[pos_i][pos_j + 1] = self

            if self.new_bomb:
                self.leave_bomb()

            self.position[1] += 1

        elif isinstance(self.matrix[pos_i][pos_j], CrossBomb):
            CrossBomb.activate(self)
            self.position[1] += 1

        elif isinstance(self.matrix[pos_i][pos_j], Healing):
            Healing.activate(self)
            self.position[1] += 1

        elif isinstance(self.matrix[pos_i][pos_j], Shield):
            Shield.activate(self)
            self.position[1] += 1

        elif isinstance(self.matrix[pos_i][pos_j], Shoe):
            Shoe.activate(self)
            self.position[1] += 1
        else:
            self.matrix[pos_i][pos_j] = Matrix.Blank((pos_i, pos_j))
            self.position[1] += 1



    def move_left(self):

        """
        Method that moves the player to the left in the matrix
        """

        pos_i = self.get_x()
        pos_j = self.get_y()

        if not pos_j > 0:
            return ""

        if isinstance(self.matrix[pos_i][pos_j - 1], Matrix.Blank):
            self.matrix[pos_i][pos_j - 1] = self

            if self.new_bomb:
                self.leave_bomb()

            self.position[1] -= 1

        elif isinstance(self.matrix[pos_i][pos_j], CrossBomb):
            CrossBomb.activate(self)
            self.position[1] -= 1

        elif isinstance(self.matrix[pos_i][pos_j], Healing):
            Healing.activate(self)
            self.position[1] -= 1

        elif isinstance(self.matrix[pos_i][pos_j], Shield):
            Shield.activate(self)
            self.position[1] -= 1

        elif isinstance(self.matrix[pos_i][pos_j], Shoe):
            Shoe.activate(self)
            self.position[1] -= 1

        else:
            self.matrix[pos_i][pos_j] = Matrix.Blank((pos_i, pos_j))
            self.position[1] -= 1

    def move_up(self):

        """
        Method that moves the player up in the matrix
        """

        pos_i = self.get_x()
        pos_j = self.get_y()

        if not pos_i > 0:
            return ""

        if isinstance(self.matrix[pos_i - 1][pos_j], Matrix.Blank):
            self.matrix[pos_i - 1][pos_j] = self

            if self.new_bomb:
                self.leave_bomb()

            self.position[0] -= 1

        elif isinstance(self.matrix[pos_i][pos_j], CrossBomb):
            CrossBomb.activate(self)
            self.position[0] -= 1

        elif isinstance(self.matrix[pos_i][pos_j], Healing):
            Healing.activate(self)
            self.position[0] -= 1

        elif isinstance(self.matrix[pos_i][pos_j], Shield):
            Shield.activate(self)
            self.position[0] -= 1

        elif isinstance(self.matrix[pos_i][pos_j], Shoe):
            Shoe.activate(self)
            self.position[0] -= 1

        else:
            self.matrix[pos_i][pos_j] = Matrix.Blank((pos_i, pos_j))
            self.position[0] -= 1

    def move_down(self):

        """
        Method that moves the player down in the matrix
        """

        pos_i = self.get_x()
        pos_j = self.get_y()

        if not pos_i < Matrix.ROWS - 1:
            return ""

        if isinstance(self.matrix[pos_i + 1][pos_j], Matrix.Blank):
            self.matrix[pos_i + 1][pos_j] = self

            if self.new_bomb:
                self.leave_bomb()

            self.position[0] += 1

        elif isinstance(self.matrix[pos_i][pos_j], CrossBomb):
            CrossBomb.activate(self)
            self.position[0] += 1

        elif isinstance(self.matrix[pos_i][pos_j], Healing):
            Healing.activate(self)
            self.position[0] += 1

        elif isinstance(self.matrix[pos_i][pos_j], Shield):
            Shield.activate(self)
            self.position[0] += 1

        elif isinstance(self.matrix[pos_i][pos_j], Shoe):
            Shoe.activate(self)
            self.position[0] += 1

        else:
            self.matrix[pos_i][pos_j] = Matrix.Blank((pos_i, pos_j))
            self.position[0] -= 1

    def leave_bomb(self):

        """
        Method that allows the player to leave a bomb where he is
        """

        pos_i = self.get_x()
        pos_j = self.get_y()
        self.matrix[pos_i][pos_j] = Bomb((pos_i, pos_j), self.matrix)
        self.new_bomb = False






    def leave_cross_bomb(self):

        """
        Method that allows the player to user cross bomb power
        """

        pos_i = self.get_x()
        pos_j = self.get_y()
        self.matrix[pos_i][pos_j] = CrossBomb((pos_i, pos_j), self.matrix)
        self.cross_bomb = False








    def get_cross_bomb(self):
        return self.cross_bomb

    def get_shield(self):
        return self.cross_bomb

    def get_shoe(self):
        return self.cross_bomb


class User(Player):

    def __init__(self, position, matrix):

        super().__init__(position, matrix)
        # User stats
        self.lives = 3
        self.velocity = TIME_BETWEEN_MOVEMENTS
        self.explosion_radius = 2

    def __str__(self):

        """
        ASCII identifier for the user's player
        :return: "u"
        """

        return "u"

    def update(self):

        """
        Method that reads the user movements from the keyboard
        """

        keys = pygame.key.get_pressed()

        # Leave bomb control
        if keys[pygame.K_o]:
            self.new_bomb = True
        # Movement control
        actual_time = pygame.time.get_ticks()

        if actual_time - self.last_movement_time < self.velocity:
            return

        if keys[pygame.K_d]:
            self.move_right()

        if keys[pygame.K_a]:
            self.move_left()

        if keys[pygame.K_w]:

            self.move_up()

        if keys[pygame.K_s]:
            self.move_down()

        self.last_movement_time = actual_time


class Enemy(Player):

    def __init__(self, position, matrix):
        super().__init__(position, matrix)

        def define_stats():

            lives = random.randrange(3, 6)
            velocity = random.randrange(5, 7)
            explosion_radius = random.randrange(1, 4)
            evasion = 14 - lives - velocity - explosion_radius
            stats = [lives, velocity, explosion_radius, evasion]

            return stats

        enemy_stats = define_stats()
        self.lives = enemy_stats[0]
        self.velocity = enemy_stats[1]*100
        self.explosion_radius = enemy_stats[2]
        self.evasion = enemy_stats[3]

    def __str__(self):

        """
        ASCII identifier for the enemies
        :return: "e"
        """

        return "e"

    def update(self):

        """
        Method that reads the enemy movements based on the genetic algorithm
        """

        pass
