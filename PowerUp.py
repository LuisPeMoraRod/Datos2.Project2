import random
import Player
import Matrix
import threading
import time

# Constants
SHIELD_TIME = 10  # in seconds

class PowerUp:
    """
    Class for the power up objects
    """
    power_up_list = ['CrossBomb', 'Healing', 'Shield', 'Shoe']

    def __init__(self, matrix):
        """
        PowerUp constructor
        :param matrix: Matrix
        """
        self.matrix = matrix.matrix
        self.position = [0, 0]
        flag = False
        while not flag:
            pos_i = random.randint(0, Matrix.ROWS - 1)
            pos_j = random.randint(0, Matrix.COLUMNS - 1)
            if isinstance(self.matrix[pos_i][pos_j], Matrix.Blank):
                flag = True
        self.position[0] = pos_i
        self.position[1] = pos_j

    def get_x(self):
        return self.position[0]

    def get_y(self):
        return self.position[1]

    def activate(self, player):
        pass


class CrossBomb(PowerUp):

    def __init__(self, matrix):
        super().__init__(matrix)

    def activate(self, player):
        player.has_cross_bomb = True
        pos_i = self.get_x()
        pos_j = self.get_y()
        self.matrix[pos_i][pos_j] = Matrix.Blank((pos_i, pos_j))

    def __str__(self):
        """
        ASCII identifier for the cross bomb power up
        :return: "+"
        """
        return "+"


class Healing(PowerUp):

    def __init__(self, matrix):
        super().__init__(matrix)

    def activate(self, player):
        """
        Method that makes the player gain a live
        Theres a maximum live stat that limits this value
        """
        player.lives += 1
        pos_i = self.get_x()
        pos_j = self.get_y()
        self.matrix[pos_i][pos_j] = Matrix.Blank((pos_i, pos_j))

    def __str__(self):
        """
        ASCII identifier for the cross bomb power up
        :return: "h"
        """
        return "h"


class Shield(PowerUp, threading.Thread):

    def __init__(self, matrix):
        super().__init__(matrix)
        threading.Thread.__init__(self)

    def run(self):
        time.sleep(SHIELD_TIME)
        self.player.has_shield = False

    def activate(self, player):
        """
        Method that makes the player have a shield, this is
        similar to an extra live but just for a certain amount of time
        """
        self.player = player
        self.player.has_shield = True
        self.start()
        pos_i = self.get_x()
        pos_j = self.get_y()
        self.matrix[pos_i][pos_j] = Matrix.Blank((pos_i, pos_j))

    def __str__(self):
        """
        ASCII identifier for the shield power up
        :return: "@"
        """
        return "@"


class Shoe(PowerUp):

    def __init__(self, matrix):
        super().__init__(matrix)

    def activate(self, player):
        """
        Method that makes the player have a shoe
        """
        player.has_shoe = True
        pos_i = self.get_x()
        pos_j = self.get_y()
        self.matrix[pos_i][pos_j] = Matrix.Blank((pos_i, pos_j))

    def __str__(self):
        """
        ASCII identifier for the cross bomb power up
        :return: "s"
        """
        return "s"
