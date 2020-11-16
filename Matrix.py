from Block import *
ROWS = 40
COLUMNS = 50
WHITE = (255, 255, 255)


class Matrix:
    """
    Class that creates the matrix on which the main algorithms and the game board works
    """

    def __init__(self):
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

    def generate_matrix(self):
        self.add_unbreakables()

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
                    else:
                        unbreakable = Unbreakable((i, j))
                        self.matrix[i].append(unbreakable)


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
        return "-"

