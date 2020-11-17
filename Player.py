class Player:
    """
    Class for player objects.
    """
    lives = 8
    velocity = 5
    explosion_radius = 3
    evasion = 7

    def __init__(self, position):
        self.position = position

    def get_x(self):
        return self.position[0]

    def get_y(self):
        return self.position[1]


class User(Player):

    def __init__(self, position):
        self.position = position

    def __str__(self):
        """
        ASCII identifier for the user's player
        :return: "u"
        """
        return "u"


class Enemy(Player):
    def __init__(self, position):
        self.position = position

    def __str__(self):
        """
        ASCII identifier for the enemies
        :return: "e"
        """
        return "e"
