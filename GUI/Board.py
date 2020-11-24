from Matrix import *

# constants
LIGHT_GREEN = (120, 187, 82)
DARK_GREEN = (113, 177, 76)
DARK_GREY = (61, 64, 75)
LIGHT_GREY = (145, 147, 156)
BROWN = (169, 109, 69)
BLOCK_SIZE = 50
ROWS = 12
COLUMNS = 18


class Board:
    __instance = None
    matrix = Matrix.get_instance()
    board_matrix = matrix.get_matrix()

    @staticmethod
    def get_instace():
        if Board.__instance is None:
            return Board()
        return Board.__instance

    def __init__(self):
        if Board.__instance is not None:
            raise Exception("A board has already been created!")
        else:
            Board.__instance = self

    def draw_base(self, SCREEN):
        pos_x = 5
        pos_y = 2

        for x in range(pos_x, COLUMNS + pos_x):
            for y in range(pos_y, ROWS + pos_y):
                if x%2 == 0:
                    if y%2 == 0:
                        color = LIGHT_GREEN
                    else:
                        color = DARK_GREEN
                else:
                    if y % 2 == 0:
                        color = DARK_GREEN
                    else:
                        color = LIGHT_GREEN
                rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(SCREEN, color, rect)

    def draw_board(self, SCREEN):
        x = 5
        y = 2
        for i in self.board_matrix:
            for j in i:
                if not isinstance(j, Blank):
                    if isinstance(j, Unbreakable):
                        rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                        pygame.draw.rect(SCREEN, LIGHT_GREY, rect)
                    elif isinstance(j, Breakable):
                        rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                        pygame.draw.rect(SCREEN, BROWN, rect)
                y = y+1
            x = x+1
            y = 2
