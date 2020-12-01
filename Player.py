import Matrix
import pygame
import Bomb
import Block
import random
import GeneticAlgorithm
import Route
import threading
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
        self.bomb_radius = 0

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
            return "Out of bounds"
        if isinstance(self.matrix[pos_i - 1][pos_j], Matrix.Blank):
            self.matrix[pos_i - 1][pos_j] = self
            if self.new_bomb:
                self.leave_bomb()
            else:
                self.matrix[pos_i][pos_j] = Matrix.Blank((pos_i, pos_j))
            self.position[0] -= 1
            return "Moved"
        elif isinstance(self.matrix[pos_i - 1][pos_j], Block.Breakable):
            return "Breakable"

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

    def set_bomb_radius(self, bomb_radius):
        self.bomb_radius = bomb_radius

    def leave_bomb(self):
        """
        Method that allows the player to leave a bomb where he is
        """
        pos_i = self.get_x()
        pos_j = self.get_y()
        self.matrix[pos_i][pos_j] = Bomb.Bomb((pos_i, pos_j), self.matrix, self.bomb_radius)
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
        self.explosion_radius = 4
        self.set_bomb_radius(self.explosion_radius)

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
        self.set_bomb_radius(self.explosion_radius)

        # Genetics
        self.genetics = GeneticAlgorithm.GeneticAlgorithm()
        threading.Thread.__init__(self)

    def run(self):
        self.choose_next_action()

    def choose_next_action(self):
        random_number = random.randint(0, GeneticAlgorithm.CHROMOSOME_LENGTH-1)
        random_action = self.genetics.chromosome[random_number]
        if random_action == 0:
            # Hide action
            self.hide_enemy()
            pass
        elif random_action == 1:
            # Search power up
            self.search_a_power_up()
        elif random_action == 2:
            # Search an enemy
            self.search_an_enemy()
        elif random_action == 3:
            # Leave a bomb
            self.leave_enemy_bomb()

    def is_position_save(self, p_type, p_number):
        if p_type == "row":
            for row in range(0, Matrix.COLUMNS-1):
                if self.matrix[p_number][row] == "o":
                    return False
        elif p_type == "column":
            for column in range(0, Matrix.ROWS-1):
                if self.matrix[column][p_number] == "o":
                    return False
        return True

    def hide_enemy(self):
        pos_i = self.get_x()
        pos_j = self.get_y()
        save_movement = []
        if pos_i % 2 == 0 and pos_j % 2 == 0:  # Even row and even column:

            if not (self.is_position_save("row", pos_i) and self.is_position_save("column", pos_j)):
                possible_movements = ["RRU", "RRD", "UUR", "UUL", "DDR", "DDL", "LLU", "LLD"]
                save_movement = self.enemy_bomb_case(pos_i, pos_j, possible_movements)
            elif not self.is_position_save("column", pos_j):
                possible_movements = ["R", "L"]
                save_movement = self.enemy_bomb_case(pos_i, pos_j, possible_movements)
            elif not self.is_position_save("row", pos_i):
                possible_movements = ["U", "D"]
                save_movement = self.enemy_bomb_case(pos_i, pos_j, possible_movements)
            else:
                return

        elif pos_i % 2 == 1 and pos_j % 2 == 0:  # Odd row and even column

            if not self.is_position_save("column", pos_j):
                possible_movements = ["UR", "UL", "DR", "DL"]
                save_movement = self.enemy_bomb_case(pos_i, pos_j, possible_movements)

        elif pos_i % 2 == 0 and pos_j % 2 == 1:  # Even row and odd column

            if not self.is_position_save("column", pos_j):
                possible_movements = ["RU", "RD", "LU", "LD"]
                save_movement = self.enemy_bomb_case(pos_i, pos_j, possible_movements)

        if save_movement != []:
            print(save_movement)
            self.move_enemy_aux(save_movement)
        else:
            print("The actual position is a save one")

    def leave_enemy_bomb(self):
        pos_i = self.get_x()
        pos_j = self.get_y()
        save_movement = []

        # The movement depends on the position of the enemy
        if pos_i % 2 == 0 and pos_j % 2 == 0:  # Even row and even column
            possible_movements = ["RRU", "RRD", "UUR", "UUL", "DDR", "DDL", "LLU", "LLD"]
            save_movement = self.enemy_bomb_case(pos_i, pos_j, possible_movements)

        elif pos_i % 2 == 1 and pos_j % 2 == 0:  # Odd row and even column
            possible_movements = ["UR", "UL", "DR", "DL"]
            save_movement = self.enemy_bomb_case(pos_i, pos_j, possible_movements)

        elif pos_i % 2 == 0 and pos_j % 2 == 1:  # Even row and odd column
            possible_movements = ["RU", "RD", "LU", "LD"]
            save_movement = self.enemy_bomb_case(pos_i, pos_j, possible_movements)

        if save_movement != []:
            self.new_bomb = True
            self.move_enemy_aux(save_movement)
        else:
            print("Impossible to leave a bomb")

    def enemy_bomb_case(self, p_pos_i, p_pos_j, p_possible_movements):
        possible_movements = p_possible_movements
        result_route = []
        for movement in possible_movements:
            pos_i = p_pos_i
            pos_j = p_pos_j
            result_route_aux = []
            for letter in movement:
                if letter == "R":
                    if not pos_j+1 < Matrix.COLUMNS:
                        result_route_aux.clear()
                        break
                    if isinstance(self.matrix[pos_i][pos_j+1], Matrix.Blank):
                        pos_j += 1
                        result_route_aux.append("right")
                    else:
                        result_route_aux.clear()
                        break
                elif letter == "U":
                    if not pos_i - 1 >= 0:
                        result_route_aux.clear()
                        break
                    if isinstance(self.matrix[pos_i-1][pos_j], Matrix.Blank):
                        pos_i -= 1
                        result_route_aux.append("up")
                    else:
                        result_route_aux.clear()
                        break
                elif letter == "D":
                    if not pos_i+1 < Matrix.ROWS:
                        result_route_aux.clear()
                        break
                    if isinstance(self.matrix[pos_i+1][pos_j], Matrix.Blank):
                        pos_i += 1
                        result_route_aux.append("down")
                    else:
                        result_route_aux.clear()
                        break
                elif letter == "L":
                    if not pos_j-1 >= 0:
                        result_route_aux.clear()
                        break
                    if isinstance(self.matrix[pos_i][pos_j-1], Matrix.Blank):
                        pos_j -= 1
                        result_route_aux.append("left")
                    else:
                        result_route_aux.clear()
                        break
            if result_route_aux != []:
                result_route = result_route_aux
        return result_route

    def search_a_power_up(self):
        closest_power_up_position = self.find_closest_object("chsz") # chsz are all the possible power ups
        if closest_power_up_position == []:
            print("No hay power ups")
            return
        enemy_i = self.get_x()
        enemy_j = self.get_y()
        target_i = closest_power_up_position[0]
        target_j = closest_power_up_position[1]
        a_star_route = Route.Route(enemy_i, enemy_j, target_i, target_j)
        self.move_enemy_aux(a_star_route.get_commands())

    def search_an_enemy(self):
        closest_enemy_position = self.find_closest_object("eu")  # "eu" means enemy or user
        if closest_enemy_position == []:
            self.choose_next_action()
        enemy_i = self.get_x()
        enemy_j = self.get_y()
        target_i = closest_enemy_position[0]
        target_j = closest_enemy_position[1]
        a_star_route = Route.Route(enemy_i, enemy_j, target_i, target_j)
        self.move_enemy_aux(a_star_route.get_commands())

    def move_enemy_aux(self, movement_list):
        for movement in movement_list:
            time.sleep(1)
            message = ""
            if movement == "up":
                message = self.move_up()
            elif movement == "down":
                message = self.move_down()
            elif movement == "right":
                message = self.move_right()
            elif movement == "left":
                message = self.move_left()

            if message == "Breakable":
                # Add a bomb and hide
                self.leave_enemy_bomb()
                """
                Pending:
                -> after leaving the bomb wait for it to explode
                and then return to the actual position to continue the A*
                -> analise the cases when the enemy hits another enemy or the user
                """
                break

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
            return []

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
