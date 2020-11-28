import random
import Player
import Matrix
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

            print(str(i) + "," + str(pos_j))

            if isinstance(self.matrix[pos_i][i], Matrix.Blank) or \
               isinstance(self.matrix[pos_i][i], Breakable) or \
               isinstance(self.matrix[pos_i][i], Player.User) or \
               isinstance(self.matrix[pos_i][i], Player.Enemy) or \
               isinstance(self.matrix[pos_i][i], CrossBomb) or \
               isinstance(self.matrix[pos_i][i], Healing) or \
               isinstance(self.matrix[pos_i][i], Shield) or \
               isinstance(self.matrix[pos_i][i], Shoe):
                self.matrix[i][pos_j] = Fire((i, pos_j), self.matrix)
            elif isinstance(self.matrix[i][pos_j], Matrix.Unbreakable):
                print("Unbreakable")
                break

        print("")

        for j in range(pos_i, ROWS): # Vertical down explosion

            print(str(j) + "," + str(pos_j))

            if isinstance(self.matrix[pos_i][j], Matrix.Blank) or \
               isinstance(self.matrix[pos_i][j], Breakable) or \
               isinstance(self.matrix[pos_i][j], Player.User) or \
               isinstance(self.matrix[pos_i][j], Player.Enemy) or \
               isinstance(self.matrix[pos_i][j], CrossBomb) or \
               isinstance(self.matrix[pos_i][j], Healing) or \
               isinstance(self.matrix[pos_i][j], Shield) or \
               isinstance(self.matrix[pos_i][j], Shoe):
                self.matrix[j][pos_j] = Fire((j, pos_j), self.matrix)
            elif isinstance(self.matrix[j][pos_j], Matrix.Unbreakable):
                print("Unbreakable")
                break

        print("")

        for k in range(pos_j, -1, -1): # Horizontal left explosion

            print(str(pos_i) + "," + str(k))

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
                print("Unbreakable")
                break

        print("")

        for l in range(pos_j, COLUMNS): # Horizontal right explosion

            print(str(pos_i) + "," + str(l))

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
                print("Unbreakable")
                break

        print("")

    """


        for j in range(0, ROWS): # Horizontal explosion

            if isinstance(self.matrix[pos_i][j], Blank) or \
               isinstance(self.matrix[pos_i][j], Breakable) or \
               isinstance(self.matrix[pos_i][j], Player) or \
               isinstance(self.matrix[pos_i][j], Enemy):

                self.matrix[pos_i][j] = Fire((pos_i, j), self.matrix)

        for i in range(0, COLUMNS): # Vertical explosion

            if isinstance(self.matrix[i][pos_j], Blank) or \
               isinstance(self.matrix[i][pos_j], Breakable) or \
               isinstance(self.matrix[i][pos_j], Player) or \
               isinstance(self.matrix[i][pos_j], Enemy):

                self.matrix[i][pos_j] = Fire((i, pos_j), self.matrix)
                
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

        print("live" + str(player.lives))

        player.lives += 1  # one is OK or should be better more of them

        print("live" + str(player.lives))

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

        print("sheld" + str(player.shield))

        player.shield = True

        print("sheld" + str(player.shield))

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
        print("shoe" + str(player.shoe))

        player.shoe = True

        print("shoe" + str(player.shoe))

    def __str__(self):

        """
        ASCII identifier for the shoe power up
        :return: "z"
        """

        return "z"
