import Matrix
import pygame

class Player (pygame.sprite.Sprite):
    """
    Class for player objects.
    """
    lives = 8
    velocity = 5
    explosion_radius = 3
    evasion = 7

    def __init__(self, position, matrix):
        """
        Player constructor
        :param position: list
        :param matrix: Matrix
        """
        super().__init__()
        self.matrix = matrix.matrix
        self.position = position

    def get_x(self):
        return self.position[0]

    def get_y(self):
        return self.position[1]

    def move_right(self):
        """
        Method that moves the player to the right in the matrix
        """
        pos_i = self.get_x()
        pos_j = self.get_y()
        if pos_j < Matrix.COLUMNS-1:
            if isinstance(self.matrix[pos_i][pos_j+1], Matrix.Blank):
                self.matrix[pos_i][pos_j+1] = self
                self.matrix[pos_i][pos_j] = Matrix.Blank((pos_i, pos_j))
                self.position[1] += 1
                print("moving right")
            else:
                print("Impossible to move right")

    def move_left(self):
        """
        Method that moves the player to the left in the matrix
        """
        pos_i = self.get_x()
        pos_j = self.get_y()
        if pos_j > 0:
            if isinstance(self.matrix[pos_i][pos_j-1], Matrix.Blank):
                self.matrix[pos_i][pos_j - 1] = self
                self.matrix[pos_i][pos_j] = Matrix.Blank((pos_i, pos_j))
                self.position[1] -= 1
                print("moving left")
            else:
                print("Impossible to move left")

    def move_up(self):
        """
        Method that moves the player up in the matrix
        """
        pos_i = self.get_x()
        pos_j = self.get_y()
        if pos_i > 0:
            if isinstance(self.matrix[pos_i-1][pos_j], Matrix.Blank):
                self.matrix[pos_i-1][pos_j] = self
                self.matrix[pos_i][pos_j] = Matrix.Blank((pos_i, pos_j))
                self.position[0] -= 1
                print("moving up")
            else:
                print("Impossible to move up")

    def move_down(self):
        """
        Method that moves the player down in the matrix
        """
        pos_i = self.get_x()
        pos_j = self.get_y()
        if pos_i < Matrix.ROWS-1:
            if isinstance(self.matrix[pos_i+1][pos_j], Matrix.Blank):
                self.matrix[pos_i+1][pos_j] = self
                self.matrix[pos_i][pos_j] = Matrix.Blank((pos_i, pos_j))
                self.position[0] += 1
                print("moving down")
            else:
                print("Impossible to move down")



class User(Player):

    def __init__(self, position, matrix):
        super().__init__(position, matrix)

    def __str__(self):
        """
        ASCII identifier for the user's player
        :return: "u"
        """
        return "u"

    def update(self):
        """
        Method that reads the user movements from the keyboard
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.move_right()
        if keys[pygame.K_a]:
            self.move_left()
        if keys[pygame.K_w]:
            self.move_up()
        if keys[pygame.K_s]:
            self.move_down()


class Enemy(Player):
    def __init__(self, position, matrix):
        super().__init__(position, matrix)

    def __str__(self):
        """
        ASCII identifier for the enemies
        :return: "e"
        """
        return "e"

    def update(self):
        """
        Method that reads the enemy movements based on the genetic algorithm
        """
        pass
