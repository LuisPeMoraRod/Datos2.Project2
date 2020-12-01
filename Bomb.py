class Bomb:
    """
    Class for the bombs objects
    """

    def __init__(self, position, matrix, bomb_radius):
        self.active_time = 0
        self.position = position
        self.matrix = matrix
        self.radius = bomb_radius

    def detonate(self):
        if self.active_time > 500:
            return True
        self.active_time += 1
        return False

    def __str__(self):
        """
        ASCII identifier for the bombs
        :return: "o"
        """
        return "o"
