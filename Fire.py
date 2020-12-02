import pygame

# Constants
EXPLOSION_TIME = 1000
ORANGE = (230, 126, 34)


class Fire:
    """
    Class for fire
    """

    def __init__(self, position):
        self.position = position
        self.color = ORANGE
        self.start_fire = pygame.time.get_ticks()

    def __str__(self):
        """
        ASCII identifier for breakable block
        :return: "F"
        """
        return "F"

    def check_fire_state(self):
        actual_time = pygame.time.get_ticks()
        if actual_time-self.start_fire > EXPLOSION_TIME:
            return True
        return False
