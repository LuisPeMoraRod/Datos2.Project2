ORANGE = (230, 126, 34)


class Fire:
    """
    Class for fire
    """

    def __init__(self, position):
        self.position = position
        self.color = ORANGE
        self.on_fire = 0

    def __str__(self):
        """
        ASCII identifier for breakable block
        :return: "F"
        """
        return "F"

    def check_fire_state(self):
        if self.on_fire > 200:
            return True
        self.on_fire += 1
        return False
