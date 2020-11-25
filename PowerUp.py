import random
from Matrix import Blank
from Fire import *
from Block import *
from Player import Enemy


ROWS = 12
COLUMNS = 18


class PowerUp:

    """
    Class for the power up objects
    """

    power_up_list = ['CrossBomb', 'Healing', 'Shield', 'Shoe']

    def __init__(self, position, matrix):

        """
        PowerUp constructor
        :param position: list
        :param matrix: Matrix
        """

        self.matrix = matrix.matrix
        self.position = position

        flag = False

        while flag == False:
            pos_i = random.randint(0, ROWS - 1)
            pos_j = random.randint(0, COLUMNS - 1)

            if isinstance(self.matrix[pos_i][pos_j], Blank):
                flag = True

        self.position[0] = pos_i
        self.position[1] = pos_j

        index = random.randint(0, 3)
        power_up = self.power_up_list[index]

        if power_up == 'CrossBomb':
            self.matrix[pos_i][pos_j] = CrossBomb((pos_i, pos_j), self.matrix)
        elif power_up == 'Healing':
            self.matrix[pos_i][pos_j] = Healing((pos_i, pos_j), self.matrix)
        elif power_up == 'Shield':
            self.matrix[pos_i][pos_j] = Shield((pos_i, pos_j), self.matrix)
        elif power_up == 'Shoe':
            self.matrix[pos_i][pos_j] = Shoe((pos_i, pos_j), self.matrix)

    def get_x(self):
        return self.position[0]

    def get_y(self):
        return self.position[1]

    def get_power_up(self, x, y):
        return self.matrix[x][y]


class CrossBomb(PowerUp):

    def __init__(self, position, matrix):

        self.matrix = matrix
        self.position = position

    def activate(self, player):

        """
        Method that spread the cross bomb in the matrix
        :return: void
        """

        player.leave_cross_bomb()

        pos_i = player.get_x()
        pos_j = player.get_y()

        for i in range(0, ROWS): # Horizontal explosion

            if isinstance(self.matrix[i][pos_j], Blank) or \
               isinstance(self.matrix[i][pos_j], Breakable) or \
               isinstance(self.matrix[i][pos_j], Enemy):

                self.matrix[i][pos_j] = Fire((pos_i, pos_j), self.matrix)

        for j in range(0, COLUMNS): # Vertical explosion

            if isinstance(self.matrix[pos_i][j], Blank) or \
               isinstance(self.matrix[pos_i][j], Breakable) or \
               isinstance(self.matrix[pos_i][j], Enemy):

                self.matrix[pos_i][j] = Fire((pos_i, pos_j), self.matrix)

    def __str__(self):

        """
        ASCII identifier for the cross bomb power up
        :return: "c"
        """

        return "c"


class Healing(PowerUp):

    def __init__(self, position, matrix):

        self.matrix = matrix
        self.position = position
        self.player = None

    def activate(self, player):

        """
        Method that increases the user o enemy live
        :return: void
        """

        player.lives += 1  # one is OK or should be better more of them

    def __str__(self):

        """
        ASCII identifier for the healing power up
        :return: "h"
        """

        return "h"


class Shield(PowerUp):

    def __init__(self, position, matrix):

        self.matrix = matrix
        self.position = position
        self.duration = 30  # quantity in frames

    def activate(self, player):

        player.has_shield = True

    def __str__(self):

        """
        ASCII identifier for the shield power up
        :return: "s"
        """

        return "s"


class Shoe(PowerUp):

    def __init__(self, position, matrix):

        self.matrix = matrix
        self.position = position
        self.kick_radius = 3  # how many nodes are necessary?

    def activate(self, player):

        # change bomb position in the matrix
        pass

    def __str__(self):

        """
        ASCII identifier for the shoe power up
        :return: "z"
        """

        return "z"
