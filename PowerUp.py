import random
import Player
from Matrix import Blank

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

    """
    def activate(self):
    Activate the power up when is collect it
    The power up does what it has to do
    It depends on the power up type
    """


class CrossBomb(PowerUp):

    def __init__(self, position, matrix):

        self.matrix = matrix
        self.position = position
        self.up_radius = 1
        self.down_radius = 1
        self.right_radius = 1
        self.left_radius = 1

    def is_Blank(self, direction):
        """
        Method that checks if the required node of the matrix is a blank space
        :return: bool
        """
        pass

    def is_breakable(self, direction):
        """
        Method that checks if the required node of the matrix is a breakable one
        :return: bool
        """
        pass

    def is_unbreakable(self, direction):
        """
        Method that checks if the required node of the matrix is an unbreakable one
        :return: bool
        """
        pass

    def is_enemy(self, direction):
        """
        Method that checks if in the required node of the matrix is an enemy
        :return: bool
        """
        pass

    def expand_radius(self, direction):
        """
        Method that increases the correct radius depending on direction parameter
        :return: void
        """
        if direction == 'up':
            self.up_radius += 1
        elif direction == 'down':
            self.down_radius += 1
        elif direction == 'right':
            self.right_radius += 1
        elif direction == 'left':
            self.left_radius += 1

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

    def heal(self, player):
        """
        Method that increases the user o enemy live
        :return: void
        """
        if isinstance(player, Player.User):
            player.lives += 1  # one is OK or should be better more of them
        elif isinstance(player, Player.Enemy):
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
        self.kick_radius = 3  # how many node are necessary?

    def kick_bomb(self):
        # change bomb position in the matrix
        pass

    def __str__(self):
        """
        ASCII identifier for the shoe power up
        :return: "z"
        """
        return "z"
