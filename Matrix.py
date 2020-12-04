from Block import *
from Player import *
from PlayersList import *
import random

WHITE = (255, 255, 255)
ROWS = 12
COLUMNS = 14


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
            return Matrix()
        return Matrix.__instance

    def __init__(self):
        """Virtually private constructor"""
        if Matrix.__instance is not None:
            raise Exception("Private constructor, this is a Singleton class")
        else:
            Matrix.__instance = self
            self.matrix = []
            self.positions = []
            self.players = PlayersList.get_instance()
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
        self.positions = self.set_initial_positions()
        self.add_players(self.positions)
        self.add_random_unbreakables()
        bt = BackTracking(self.unbreakables)
        self.add_random_breakables()

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
        Method that changes 7% of the total of nodes in the matrix (ROWS x COLUMNS) to randomly distributed unbreakable blocks
        :return:
        """
        random_blocks = 0.07 * ROWS * COLUMNS
        blocks_counter = 0
        while blocks_counter < random_blocks:
            i = random.randint(0, ROWS - 1)
            j = random.randint(0, COLUMNS - 1)
            if isinstance(self.matrix[i][j], Blank) and not self.is_in_player_zone(i, j):
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

    def add_random_breakables(self):
        """
        Method that changes 25% of the total of nodes in the matrix (ROWS x COLUMNS) to randomly distributed unbreakable blocks
        :return:
        """
        random_blocks = 0.25 * ROWS * COLUMNS
        blocks_counter = 0
        while blocks_counter < random_blocks:
            i = random.randint(0, ROWS - 1)
            j = random.randint(0, COLUMNS - 1)
            if isinstance(self.matrix[i][j], Blank) and not self.is_in_player_zone(i, j):
                breakable = Breakable((i, j))
                self.matrix[i][j] = breakable
                blocks_counter += 1
                self.unbreakables += 1

    def is_in_player_zone(self, i, j):
        """
        Validation if index i,j is and adjacent node of the position of any player
        :param i:
        :param j:
        :return:
        """
        positions_list = self.positions
        for position in positions_list:
            if i == position[0]-1 and j == position[1]-1:
                return True
            elif i == position[0]-1 and j == position[1]:
                return True
            elif i == position[0]-1 and j == position[1]+1:
                return True
            elif i == position[0] and j == position[1]-1:
                return True
            elif i == position[0] and j == position[1]:
                return True
            elif i == position[0] and j == position[1]+1:
                return True
            elif i == position[0]+1 and j == position[1]-1:
                return True
            elif i == position[0]+1 and j == position[1]:
                return True
            elif i == position[0]+1 and j == position[1]+1:
                return True
        return False

    def add_players(self, positions):
        """Adds players to the matrix"""
        players = []

        def set_indexes():
            rand_indexes = []
            while len(rand_indexes) < 8:
                ind = random.randint(0, 7)
                if ind not in rand_indexes:
                    rand_indexes.append(ind)
            return rand_indexes

        indexes = set_indexes()

        index = indexes[0]
        self.enemy0 = Enemy(positions[index], self)
        players.append(self.enemy0)

        index = indexes[1]
        self.enemy1 = Enemy(positions[index], self)
        players.append(self.enemy1)

        index = indexes[2]
        self.enemy2 = Enemy(positions[index], self)
        players.append(self.enemy2)

        index = indexes[3]
        self.enemy3 = Enemy(positions[index], self)
        players.append(self.enemy3)

        index = indexes[4]
        self.enemy4 = Enemy(positions[index], self)
        players.append(self.enemy4)

        index = indexes[5]
        self.enemy5 = Enemy(positions[index], self)
        players.append(self.enemy5)

        index = indexes[6]
        self.enemy6 = Enemy(positions[index], self)
        players.append(self.enemy6)

        index = indexes[7]
        self.user = User(positions[index], self)
        players.append(self.user)

        for k in range(0, len(players)):  # assign players to the matrix
            player = players[k]
            i = player.get_x()
            j = player.get_y()
            self.matrix[i][j] = player

        self.players.players_list = []
        for i in range(0, len(players)-1):
            self.players.players_list.append(players[i])



    def set_initial_positions(self):
        """
        Defines the initial position of the 8 players. Returns a list with the coordinates or indexes where each player will be placed in the matrix
        :return: inital_positions
        """
        initial_positions = []
        for k in range(0, 4):
            i = int((ROWS - 1) * k / 3)
            if k % 2 == 0:
                j = 0
            else:
                j = int((COLUMNS - 1) / 2)
            initial_positions.append([i, j])
            j += int((COLUMNS - 1) / 2)
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
        """
        Recursive method that attempts to visit all nodes in matrix to check if the generated routes are correct.
        Returns false if there are unreachable nodes.
        :param i: int
        :param j: int
        :return: boolean
        """

        position = (i, j)
        if len(self.visited) == ROWS * COLUMNS - self.unbreakables:
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
