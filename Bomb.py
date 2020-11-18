class Bomb:
    """
    Class for the bombs objects
    """

    def __init__(self, position, matrix):
        self.position = position
        self.matrix = matrix

    def __str__(self):
        """
        ASCII identifier for the bombs
        :return: "o"
        """
        return "o"
