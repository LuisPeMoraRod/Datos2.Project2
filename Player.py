import Matrix
import pygame
import Bomb
import random
import GeneticAlgorithm
import Route
import threading
import _thread
import time

# Constants
TIME_BETWEEN_MOVEMENTS = 150


class Player (pygame.sprite.Sprite):
    """
    Class for player objects.
    """

    def __init__(self, position, matrix):
        """
        Player constructor
        :param position: list
        :param matrix: Matrix
        """
        super().__init__()
        # Position attributes
        self.matrix = matrix.matrix
        self.position = position
        # Bomb control attribute
        self.new_bomb = False
        # Movement attributes
        self.last_movement_time = pygame.time.get_ticks()
        # Power ups attributes
        self.has_cross_bomb = False
        self.has_shoe = False
        self.has_shield = False

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
        if not pos_j < Matrix.COLUMNS - 1:
            return ""
        if isinstance(self.matrix[pos_i][pos_j + 1], Matrix.Blank):
            self.matrix[pos_i][pos_j + 1] = self
            if self.new_bomb:
                self.leave_bomb()
            else:
                self.matrix[pos_i][pos_j] = Matrix.Blank((pos_i, pos_j))
            self.position[1] += 1

    def move_left(self):
        """
        Method that moves the player to the left in the matrix
        """
        pos_i = self.get_x()
        pos_j = self.get_y()
        if not pos_j > 0:
            return ""
        if isinstance(self.matrix[pos_i][pos_j - 1], Matrix.Blank):
            self.matrix[pos_i][pos_j - 1] = self
            if self.new_bomb:
                self.leave_bomb()
            else:
                self.matrix[pos_i][pos_j] = Matrix.Blank((pos_i, pos_j))
            self.position[1] -= 1

    def move_up(self):
        """
        Method that moves the player up in the matrix
        """
        pos_i = self.get_x()
        pos_j = self.get_y()
        if not pos_i > 0:
            return ""
        if isinstance(self.matrix[pos_i - 1][pos_j], Matrix.Blank):
            self.matrix[pos_i - 1][pos_j] = self
            if self.new_bomb:
                self.leave_bomb()
            else:
                self.matrix[pos_i][pos_j] = Matrix.Blank((pos_i, pos_j))
            self.position[0] -= 1

    def move_down(self):
        """
        Method that moves the player down in the matrix
        """
        pos_i = self.get_x()
        pos_j = self.get_y()
        if not pos_i < Matrix.ROWS - 1:
            return ""
        if isinstance(self.matrix[pos_i + 1][pos_j], Matrix.Blank):
            self.matrix[pos_i + 1][pos_j] = self
            if self.new_bomb:
                self.leave_bomb()
            else:
                self.matrix[pos_i][pos_j] = Matrix.Blank((pos_i, pos_j))
            self.position[0] += 1

    def leave_bomb(self):
        """
        Method that allows the player to leave a bomb where he is
        """
        pos_i = self.get_x()
        pos_j = self.get_y()
        self.matrix[pos_i][pos_j] = Bomb.Bomb((pos_i, pos_j), self.matrix)
        self.new_bomb = False


class User(Player):
    """
    Class of the user object
    Inherits from the player class
    """

    def __init__(self, position, matrix):
        super().__init__(position, matrix)
        # User stats
        self.lives = 3
        self.velocity = TIME_BETWEEN_MOVEMENTS
        self.explosion_radius = 2

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
        # Leave bomb control
        if keys[pygame.K_o]:
            self.new_bomb = True
        # Movement control
        actual_time = pygame.time.get_ticks()
        if actual_time - self.last_movement_time < self.velocity:
            return
        if keys[pygame.K_d]:
            self.move_right()
        if keys[pygame.K_a]:
            self.move_left()
        if keys[pygame.K_w]:
            self.move_up()
        if keys[pygame.K_s]:
            self.move_down()
        self.last_movement_time = actual_time


class Enemy(Player, threading.Thread):
    """
    Class of the enemy objects
    Inherits from the player class
    """

    def __init__(self, position, matrix):
        super().__init__(position, matrix)

        def define_stats():
            lives = random.randrange(3, 6)
            velocity = random.randrange(5, 7)
            explosion_radius = random.randrange(1, 4)
            evasion = 14 - lives - velocity - explosion_radius
            stats = [lives, velocity, explosion_radius, evasion]
            return stats

        enemy_stats = define_stats()
        self.lives = enemy_stats[0]
        self.velocity = enemy_stats[1]*100
        self.explosion_radius = enemy_stats[2]
        self.evasion = enemy_stats[3]

        # Genetics
        self.genetics = GeneticAlgorithm.GeneticAlgorithm()
        threading.Thread.__init__(self)

    def run(self):
        self.choose_next_action()

    def choose_next_action(self):
        random_number = random.randint(0, GeneticAlgorithm.CHROMOSOME_LENGTH-1)
        random_action = self.genetics.chromosome[random_number]
        random_action = 2
        if random_action == 0:
            # Hide action
            pass
        elif random_action == 1:
            # Search power up
            pass
        elif random_action == 2:
            # Search an enemy
            self.search_an_enemy()
        elif random_action == 3:
            # Leave a bomb
            pass

    def search_an_enemy(self):
        closest_enemy_position = self.find_closest_object("eu")  # "eu" means enemy or user
        print("The closest object for: " + "[" + str(self.get_x()) + "," + str(self.get_y()) + "] is: ")
        print(closest_enemy_position)
        enemy_i = self.get_x()
        print(enemy_i)
        enemy_j = self.get_y()
        print(enemy_j)
        target_i = closest_enemy_position[0]
        print(target_i)
        target_j = closest_enemy_position[1]
        print(target_j)
        a_star_route = Route.Route(enemy_i, enemy_j, target_i, target_j)
        print(a_star_route.get_commands())
        self.move_enemy_aux(a_star_route.get_commands())

    def move_enemy_aux(self, movement_list):
        for movement in movement_list:
            time.sleep(1)
            if movement == "up":
                print("Moving up")
                self.move_up()
                pass
            elif movement == "down":
                print("Moving down")
                self.move_down()
                pass
            elif movement == "right":
                print("Moving right")
                self.move_right()
                pass
            elif movement == "left":
                print("Moving left")
                self.move_left()
                pass

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
        #self.enemy_thread = threading.Thread(target=self.choose_next_action())
        #self.enemy_thread.start()
        #_thread.start_new_thread(self.choose_next_action(), ())
        #self.choose_next_action()
        self.start()

    def find_closest_object(self, object_str):
        """
        Method that approximates the closest object to the enemy
        :param: object_str is the string that represents the object we want to search
        :return: position (i,j) of the closest object
        """
        # Making the list of the objects
        object_pos_list = []
        for i in range(0, Matrix.ROWS):
            for j in range(0, Matrix.COLUMNS):
                if not (self.matrix[i][j].__str__() in object_str):
                    continue
                if i != self.get_x() or j != self.get_y():
                    new_position = [i, j]
                    object_pos_list.append(new_position)

        # Return None if there's no option
        if len(object_pos_list) == 0:
            return

        # Finding the closest object from the list
        min_distance = 10000
        min_position = object_pos_list[0]
        for position in object_pos_list:
            i_distance = abs(self.get_x() - position[0])
            j_distance = abs(self.get_y() - position[1])
            manhattan_distance = i_distance + j_distance
            if manhattan_distance < min_distance:
                min_position = position
                min_distance = manhattan_distance
        return min_position

