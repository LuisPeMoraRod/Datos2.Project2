from Block import *
from Player import *
import random
ROWS = 20
COLUMNS = 20
WHITE = (255, 255, 255)


class Matrix:
    """
    Class that creates the matrix on which the main algorithms and the game board works. Implements Singleton creational pattern design
    """
    __instance = None
    user = enemy0 = enemy1 = enemy2 = enemy3 = enemy4 = enemy5 = enemy6 = None
    unbreakables = 0

    @staticmethod
    def get_instance():
        """Static access method"""
        if Matrix.__instance is None:
            Matrix()
        return Matrix.__instance

    def __init__(self):
        """Virtually private constructor"""
        if Matrix.__instance is not None:
            raise Exception("Private constructor, this is a Singleton class")
        else:
            Matrix.__instance = self
            self.matrix = []
            self.generate_matrix()

    def __str__(self):
        """
        Returns matrix parsed as a string
        :return: str_matrix
        """
        str_matrix = ""
        for i in range(0, len(self.matrix)):
            for j in range(0, len(self.matrix[i])):
                str_matrix += str(self.matrix[i][j]) + '\t'
            str_matrix += "\n"
        return str_matrix

    def get_matrix(self):
        return self.matrix

    def generate_matrix(self):
        self.add_unbreakables()
        positions = self.set_initial_positions()
        self.add_players(positions)
        self.add_random_unbreakables()
        bt = BackTracking(self.unbreakables)
        print(bt.is_safe())


    def add_unbreakables(self):
        """
        Method that distributes unbreakable blocks in a special pattern over the matrix
        :return: void
        """
        for i in range(0, ROWS):
            row = []
            self.matrix.append(row)
            for j in range(0, COLUMNS):
                if i % 2 == 0:  # even rows have blank spaces only
                    blank_space = Blank((i, j))
                    self.matrix[i].append(blank_space)
                else:
                    if j % 2 == 0:  # even columns have blank spaces
                        blank_space = Blank((i, j))
                        self.matrix[i].append(blank_space)
                    else:  # odd columns in odd rows have the unbreakable blocks
                        unbreakable = Unbreakable((i, j))
                        self.matrix[i].append(unbreakable)
                        self.unbreakables += 1

    def add_random_unbreakables(self):
        """
        Method that adds 10% of randomly distributed unbreakable blocks of the total of spaces in the matrix (ROWS x COLUMNS)
        :return:
        """
        random_blocks = 0.05*ROWS*COLUMNS
        blocks_counter = 0
        while blocks_counter < random_blocks:
            i = random.randint(0, ROWS-1)
            j = random.randint(0, COLUMNS-1)
            if isinstance(self.matrix[i][j], Blank):
                unbreakable = Unbreakable((i, j))
                self.matrix[i][j] = unbreakable
                blocks_counter += 1
                self.unbreakables += 1
                bt = BackTracking(self.unbreakables)
                if not bt.is_safe():
                    blocks_counter -= 1
                    self.unbreakables -= 1
                    blank_space = Blank((i, j))
                    self.matrix[i][j] = blank_space

    def add_players(self, positions):
        """Adds players to the matrix"""
        players = []

        self.enemy0 = Enemy(positions[0])
        players.append(self.enemy0)

        self.enemy1 = Enemy(positions[1])
        players.append(self.enemy1)

        self.enemy2 = Enemy(positions[2])
        players.append(self.enemy2)

        self.enemy3 = Enemy(positions[3])
        players.append(self.enemy3)

        self.enemy4 = Enemy(positions[4])
        players.append(self.enemy4)

        self.enemy5 = Enemy(positions[5])
        players.append(self.enemy5)

        self.enemy6 = Enemy(positions[6])
        players.append(self.enemy6)

        self.user = User(positions[7])
        players.append(self.user)

        for k in range(0, len(players)):  # assign players to the matrix
            player = players[k]
            i = player.get_x()
            j = player.get_y()
            self.matrix[i][j] = player


    def set_initial_positions(self):
        """
        Defines the initial position of the 8 players. Returns a list with the coordinates or indexes where each player will be placed in the matrix
        :return: inital_positions
        """
        initial_positions = []
        for k in range(0, 4):
            i = int((ROWS-1) * k/3)
            if k % 2 == 0:
                j = 0
            else:
                j = int((COLUMNS-1)/2)
            initial_positions.append([i, j])
            j += int((COLUMNS-1)/2)
            initial_positions.append([i, j])
        return initial_positions


class Blank:
    """
    Class for empty spaces in matrix. Represent the spaces where any player can move.
    """

    def __init__(self, position):
        self.position = position
        self.color = WHITE

    def __str__(self):
        """
        ASCII identifier for empty spaces
        :return: "-"
        """
        return " "


class BackTracking:
    """
    Class that executes backtracking algorithm to check if all blank spaces are reachable
    """
    def __init__(self, unbreakables):
        self.matrix = Matrix.get_instance()
        self.visited = []
        self.unbreakables = unbreakables

    def is_safe(self):
        return self.is_safe_aux(0, 0)

    def is_safe_aux(self, i, j):
        position = (i, j)
        if len(self.visited) == ROWS*COLUMNS-self.unbreakables:
            return True
        if i == ROWS or j == COLUMNS:
            return False
        if i < 0 or j < 0:
            return False
        array = self.matrix.get_matrix()
        if (isinstance(array[i][j], Blank) or isinstance(array[i][j], Player)) and (position not in self.visited):
            self.visited.append(position)
            if self.is_safe_aux(i, j + 1):
                return True
            elif self.is_safe_aux(i + 1, j):
                return True
            elif self.is_safe_aux(i, j - 1):
                return True
            elif self.is_safe_aux(i - 1, j):
                return True
        return False
