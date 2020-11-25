BROWN = (130, 91, 91)
GRAY = (158, 155, 155)


class Block:

    """
    Parent class of BreakableBlock and UnbreakableBlock subclasses
    """

    def __init__(self, position):

        self.position = position


class Breakable(Block):

    """
    Class for breakable blocks
    """

    def __init__(self, position):

        self.position = position
        self.color = BROWN

    def __str__(self):

        """
        ASCII identifier for breakable block
        :return: "#"
        """

        return "#"


class Unbreakable(Block):

    """
    Class for unbreakable blocks
    """

    def __init__(self, position):

        self.position = position
        self.color = GRAY

    def __str__(self):

        """
        ASCII identifier for unbreakable block
        :return: "X"
        """

        return "X"
