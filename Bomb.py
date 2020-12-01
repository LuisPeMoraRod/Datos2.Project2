import pygame

# Constants
TIME_TO_DETONATE = 2200


class Bomb:
    """
    Class for the bombs objects
    """

    def __init__(self, position, matrix, bomb_radius):
        self.start_time = pygame.time.get_ticks()
        self.position = position
        self.matrix = matrix
        self.radius = bomb_radius

    def detonate(self):
        actual_time = pygame.time.get_ticks()
        if actual_time - self.start_time > TIME_TO_DETONATE:
            return True
        return False

    def __str__(self):
        """
        ASCII identifier for the bombs
        :return: "o"
        """
        return "o"
