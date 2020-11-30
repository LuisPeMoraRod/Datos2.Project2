import random
import Player
import Matrix
from GUI import Board
from Block import *
from Fire import *

ROWS = 12
COLUMNS = 18


class PowerUp:

    """
    Class for the power up objects
    """

    #power_up_list = ['CrossBomb', 'Healing', 'Shield', 'Shoe']
    power_up_list = ['CrossBomb', 'CrossBomb', 'CrossBomb', 'CrossBomb']

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

            if isinstance(self.matrix[pos_i][pos_j], Matrix.Blank):
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

        pos_i = self.get_x()
        pos_j = self.get_y()

        for i in range(pos_i, -1, -1): # Vertical up explosion

            if isinstance(self.matrix[i][pos_j], Fire):
                pass
            elif not isinstance(self.matrix[i][pos_j], Matrix.Unbreakable):
                self.matrix[i][pos_j] = Fire((i, pos_j), self.matrix)
            else:
                break

            """
            if isinstance(self.matrix[i][pos_j], Matrix.Blank) or \
               isinstance(self.matrix[i][pos_j], Breakable) or \
               isinstance(self.matrix[i][pos_j], Player.User) or \
               isinstance(self.matrix[i][pos_j], Player.Enemy) or \
               isinstance(self.matrix[i][pos_j], CrossBomb) or \
               isinstance(self.matrix[i][pos_j], Healing) or \
               isinstance(self.matrix[i][pos_j], Shield) or \
               isinstance(self.matrix[i][pos_j], Shoe):
                self.matrix[i][pos_j] = Fire((i, pos_j), self.matrix)
            elif isinstance(self.matrix[i][pos_j], Matrix.Unbreakable):
                break
            """

        for j in range(pos_i, ROWS): # Vertical down explosion

            if isinstance(self.matrix[j][pos_j], Fire):
                pass
            elif not isinstance(self.matrix[j][pos_j], Matrix.Unbreakable):
                self.matrix[j][pos_j] = Fire((j, pos_j), self.matrix)
            else:
                break

            """
            if isinstance(self.matrix[j][pos_j], Matrix.Blank) or \
               isinstance(self.matrix[j][pos_j], Breakable) or \
               isinstance(self.matrix[j][pos_j], Player.User) or \
               isinstance(self.matrix[j][pos_j], Player.Enemy) or \
               isinstance(self.matrix[j][pos_j], CrossBomb) or \
               isinstance(self.matrix[j][pos_j], Healing) or \
               isinstance(self.matrix[j][pos_j], Shield) or \
               isinstance(self.matrix[j][pos_j], Shoe):
                self.matrix[j][pos_j] = Fire((j, pos_j), self.matrix)
            elif isinstance(self.matrix[j][pos_j], Matrix.Unbreakable):
                break
            """

        for k in range(pos_j, -1, -1): # Horizontal left explosion

            if isinstance(self.matrix[pos_i][k], Fire):
                pass
            elif not isinstance(self.matrix[pos_i][k], Matrix.Unbreakable):
                self.matrix[pos_i][k] = Fire((pos_i, k), self.matrix)
            else:
                break

            """
            if isinstance(self.matrix[pos_i][k], Matrix.Blank) or \
               isinstance(self.matrix[pos_i][k], Breakable) or \
               isinstance(self.matrix[pos_i][k], Player.User) or \
               isinstance(self.matrix[pos_i][k], Player.Enemy) or \
               isinstance(self.matrix[pos_i][k], CrossBomb) or \
               isinstance(self.matrix[pos_i][k], Healing) or \
               isinstance(self.matrix[pos_i][k], Shield) or \
               isinstance(self.matrix[pos_i][k], Shoe):
                self.matrix[pos_i][k] = Fire((pos_i, k), self.matrix)
            elif isinstance(self.matrix[pos_i][k], Matrix.Unbreakable):
                break
            """

        for l in range(pos_j, COLUMNS): # Horizontal right explosion

            if isinstance(self.matrix[pos_i][l], Fire):
                pass
            elif not isinstance(self.matrix[pos_i][l], Matrix.Unbreakable):
                self.matrix[pos_i][l] = Fire((pos_i, l), self.matrix)
            else:
                break

            """
            if isinstance(self.matrix[pos_i][l], Matrix.Blank) or \
               isinstance(self.matrix[pos_i][l], Breakable) or \
               isinstance(self.matrix[pos_i][l], Player.User) or \
               isinstance(self.matrix[pos_i][l], Player.Enemy) or \
               isinstance(self.matrix[pos_i][l], CrossBomb) or \
               isinstance(self.matrix[pos_i][l], Healing) or \
               isinstance(self.matrix[pos_i][l], Shield) or \
               isinstance(self.matrix[pos_i][l], Shoe):
                self.matrix[pos_i][l] = Fire((pos_i, l), self.matrix)
            elif isinstance(self.matrix[pos_i][l], Matrix.Unbreakable):
                break
            """

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

        """
        Method that activates user o enemy shield
        :return: void
        """

        player.shield = True

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

        """
        Method that activates user o enemy shoe
        :return: void
        """

        player.shoe = True

    def __str__(self):

        """
        ASCII identifier for the shoe power up
        :return: "z"
        """

        return "z"
