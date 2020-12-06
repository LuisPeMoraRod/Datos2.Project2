# Internal project imports
import Matrix
import Bomb
import Block
import GeneticAlgorithm
import Route
import Fire
import PowerUp

# External project imports
import pygame
import random
import threading
import time
import sys

# Stack management
sys.setrecursionlimit(10**6)
# Constants
TIME_BETWEEN_MOVEMENTS = 150
TIME_BETWEEN_BOMBS = 1000
HIDING_TIME = 0.5
POWER_UP_SEARCH_TIME = 0.2
LIVES = 3


class Player (pygame.sprite.Sprite):
    """
    Class for player objects.
    Parent class of User and Enemy
    """

    def __init__(self, position, matrix):
        """
        Player constructor
        :param position: list -> initial position of the player
        :param matrix: Matrix -> matrix where the player moves
        """
        super().__init__()
        # Position attributes
        self.matrix = matrix.matrix
        self.position = position
        # Bomb control attribute
        self.new_bomb = False
        # Movement attributes
        self.last_movement_time = pygame.time.get_ticks()
        self.last_bomb_time = pygame.time.get_ticks()
        self.is_movement_denied = False
        # Power ups attributes
        self.has_cross_bomb = False
        self.has_shoe = False
        self.has_shield = False
        # Player stats
        self.explosion_radius = 0
        self.lives = 0

        self.kills = 0  # number of kills achieved
        self.nearest_bomb = 10000000  # distance of nearest bomb to User

    def get_x(self):
        """:return: current row"""
        return self.position[0]

    def get_y(self):
        """:return: current column"""
        return self.position[1]

    def moving_aux(self, actual_pos, next_pos):
        """
        Auxiliary method for the move_right, move_left, move_up and
        move_down methods
        :param: next_object -> the object located in the position
        where the player is moving
        :param: actual_pos <Tuple> -> contains the player coordinates before the movement
        :param: next_pos <Tuple> -> contains the player coordinates after the movement
        :return: string -> action that the player most follow, the possible
        actions are:
        1) Moved -> the player moves and does nothing else
        2) Breakable -> indicates that the next object is a breakable block
        3) Abort movement -> indicates the player to stop moving
        """
        # Activate  a power up if it follows the movement
        if isinstance(self.matrix[next_pos[0]][next_pos[1]], PowerUp.PowerUp):
            self.matrix[next_pos[0]][next_pos[1]].activate(self)
        # Do the normal movement when the next position is Blank
        if isinstance(self.matrix[next_pos[0]][next_pos[1]], Matrix.Blank):
            self.matrix[next_pos[0]][next_pos[1]] = self
            if self.new_bomb:
                self.leave_bomb()
            else:
                self.matrix[actual_pos[0]][actual_pos[1]] = Matrix.Blank(actual_pos)
            self.position = next_pos
            return "Moved"
        # Inform if the next position is a Breakbale Block
        elif isinstance(self.matrix[next_pos[0]][next_pos[1]], Block.Breakable):
            return "Breakable"
        # Every other object will kill the movement
        else:
            if isinstance(self.matrix[next_pos[0]][next_pos[1]], Bomb.Bomb) and self.has_shoe:
                self.kick_bomb(next_pos)
            return "Abort movement"

    def move_right(self):
        """
        Method that moves the player to the right in the matrix
        :brief: If moving to the right is possible the player does it
        :return: An string indicating if the player moved
        """
        if self.is_movement_denied:  # When a bomb hits the player
            return ""
        pos_i = self.get_x()
        pos_j = self.get_y()
        if not pos_j < Matrix.COLUMNS-1:
            return "Out of bounds"
        return self.moving_aux((pos_i, pos_j), (pos_i, pos_j+1))

    def move_left(self):
        """
        Method that moves the player to the left in the matrix
        :brief: If moving to the left is possible the player does it
        :return: An string indicating if the player moved
        """
        if self.is_movement_denied:  # When a bomb hits the player
            return ""
        pos_i = self.get_x()
        pos_j = self.get_y()
        if not pos_j > 0:
            return "Out of bounds"
        return self.moving_aux((pos_i, pos_j), (pos_i, pos_j-1))

    def move_up(self):
        """
        Method that moves the player up in the matrix
        :brief: If moving up is possible the player does it
        :return: An string indicating if the player moved
        """
        if self.is_movement_denied:  # When a bomb hits the player
            return ""
        pos_i = self.get_x()
        pos_j = self.get_y()
        if not pos_i > 0:
            return "Out of bounds"
        return self.moving_aux((pos_i, pos_j), (pos_i-1, pos_j))

    def move_down(self):
        """
        Method that moves the player down in the matrix
        :brief: If moving down is possible the player does it
        :return: An string indicating if the player moved
        """
        if self.is_movement_denied:  # When a bomb hits the player
            return ""
        pos_i = self.get_x()
        pos_j = self.get_y()
        if not pos_i < Matrix.ROWS - 1:
            return "Out of bounds"
        return self.moving_aux((pos_i, pos_j), (pos_i+1, pos_j))

    def leave_bomb(self):
        """
        Method that allows the player to leave a bomb where he is
        """
        pos_i = self.get_x()
        pos_j = self.get_y()
        bomb_radius = self.explosion_radius
        if self.has_cross_bomb:
            bomb_radius = max(Matrix.COLUMNS, Matrix.ROWS)
            self.has_cross_bomb = False
        self.matrix[pos_i][pos_j] = Bomb.Bomb((pos_i, pos_j), self.matrix, bomb_radius, self)
        self.new_bomb = False

    def kick_bomb(self, position):
        """
        Auxiliary method for the Shoe power up, changes
        the position of the "kicked" bomb
        """
        pos_i = position[0]
        pos_j = position[1]
        self.matrix[pos_i][pos_j] = Matrix.Blank((pos_i, pos_j))
        new_position_found = False
        # Searches until it founds a Black position to add the bomb
        while not new_position_found:
            pos_i = random.randint(0, Matrix.ROWS - 1)
            pos_j = random.randint(0, Matrix.COLUMNS - 1)
            if isinstance(self.matrix[pos_i][pos_j], Matrix.Blank):
                new_position_found = True
        self.matrix[pos_i][pos_j] = Bomb.Bomb((pos_i, pos_j), self.matrix, self.explosion_radius, self)
        self.has_shoe = False

    def lose_live(self,  action):
        """
        Method that makes the player lose a live
        kills the player if he reaches 0 lives
        """
        if action == "Test":
            if self.lives == 1:
                return None
            return self
        elif action == "Kill":
            if not self.has_shield and self.lives > 0:
                self.lives -= 1
            if self.lives <= 0:
                self.kill()  # Method from the pygame.Sprite class
                return None
            return self


class User(Player):
    """
    Class of the user object
    Inherits from the player class
    """

    def __init__(self, position, matrix):
        """
        User constructor, defines the main attributes
        :param position: list -> initial position of the player
        :param matrix: Matrix -> matrix where the player moves
        """
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
        if self.is_movement_denied:
            return
        keys = pygame.key.get_pressed()
        # Leave bomb control

        if keys[pygame.K_o]:
            actual_time_bomb = pygame.time.get_ticks()
            if actual_time_bomb - self.last_bomb_time < TIME_BETWEEN_BOMBS:
                return
            self.last_bomb_time = actual_time_bomb
            self.new_bomb = True
        # Movement control
        actual_time_move = pygame.time.get_ticks()
        if actual_time_move - self.last_movement_time < self.velocity:
            return
        if keys[pygame.K_d]:
            self.move_right()
        if keys[pygame.K_a]:
            self.move_left()
        if keys[pygame.K_w]:
            self.move_up()
        if keys[pygame.K_s]:
            self.move_down()
        self.last_movement_time = actual_time_move


class Enemy(Player, threading.Thread):
    """
    Class of the enemy objects
    Inherits from the player class and the Thread class
    """

    def __init__(self, position, matrix):
        """
        Enemy constructor, defines the main attributes
        :param position: list -> initial position of the player
        :param matrix: Matrix -> matrix where the player moves
        """
        super().__init__(position, matrix)

        def define_stats():  # Randomly define the stats
            lives = LIVES
            evasion = random.randrange(2, 4)
            explosion_radius = random.randrange(2, 4)
            velocity = 14 - evasion - explosion_radius
            stats = [lives, velocity, explosion_radius, evasion]
            return stats

        enemy_stats = define_stats()
        self.lives = enemy_stats[0]
        self.velocity = enemy_stats[1]*100
        self.explosion_radius = enemy_stats[2]
        self.evasion = enemy_stats[3]

        # Genetics
        self.genetics = GeneticAlgorithm.Genes(self)
        threading.Thread.__init__(self)

    def run(self):
        """
        Override from the Thread class
        :brief: allows the enemy to begin his thread
        the enemy thread ends when the player dies
        """
        self.choose_next_action()

    def choose_next_action(self):
        """
        Execute a new action from the genetic algorithm
        This function calls itself until the player dies
        the recursion allows the enemy to never stop playing
        """
        # Stop the movement if the player has no lives left
        if self.lives <= 0:
            return
        random_number = random.randint(0, GeneticAlgorithm.CHROMOSOME_LENGTH-2)
        random_action = self.genetics.chromosome[random_number]
        if random_action == 0:
            # Hide action
            self.hide_enemy()
            time.sleep(HIDING_TIME)
        elif random_action == 1:
            # Search power up
            self.search_a_power_up()
            time.sleep(POWER_UP_SEARCH_TIME)
        elif random_action == 2:
            # Search an enemy
            self.search_an_enemy()
        elif random_action == 3:
            # Leave a bomb
            self.leave_enemy_bomb
        self.choose_next_action()

    def is_position_save(self, p_type, p_number):
        """
        Auxiliary method for the hide_enemy() method
        :param p_type: defines the unpinned type (row or column)
        :param p_number: defines the pinned row or column
        :return: True if there is no in the current column or row
        """
        if p_type == "row":
            # Checks if theres a bomb in the current row
            for row in range(0, Matrix.COLUMNS-1):
                if self.matrix[p_number][row] == "o":
                    return False
        elif p_type == "column":
            # Checks if theres a bomb in the current column
            for column in range(0, Matrix.ROWS-1):
                if self.matrix[column][p_number] == "o":
                    return False
        return True

    def hide_enemy(self):
        """
        Action that hides the enemy
        :brief: if the enemy position is threatened by a possible
        cross bomb, the enemy changes his row or column
        """
        pos_i = self.get_x()
        pos_j = self.get_y()
        save_movement = []
        if pos_i % 2 == 0 and pos_j % 2 == 0:  # Even row and even column:

            # The movement depends in if the row, column or both are threatened
            if not (self.is_position_save("row", pos_i) and self.is_position_save("column", pos_j)):
                possible_movements = ["RRU", "RRD", "UUR", "UUL", "DDR", "DDL", "LLU", "LLD"]
                save_movement = self.possible_movement_cases(pos_i, pos_j, possible_movements)
            elif not self.is_position_save("column", pos_j):
                possible_movements = ["R", "L"]
                save_movement = self.possible_movement_cases(pos_i, pos_j, possible_movements)
            elif not self.is_position_save("row", pos_i):
                possible_movements = ["U", "D"]
                save_movement = self.possible_movement_cases(pos_i, pos_j, possible_movements)
            else:
                return

        elif pos_i % 2 == 1 and pos_j % 2 == 0:  # Odd row and even column
            if not self.is_position_save("column", pos_j):
                possible_movements = ["UR", "UL", "DR", "DL"]
                save_movement = self.possible_movement_cases(pos_i, pos_j, possible_movements)

        elif pos_i % 2 == 0 and pos_j % 2 == 1:  # Even row and odd column
            if not self.is_position_save("column", pos_j):
                possible_movements = ["RU", "RD", "LU", "LD"]
                save_movement = self.possible_movement_cases(pos_i, pos_j, possible_movements)

        if save_movement != []:  # Empty list means that the actual position is safe
            self.move_enemy_aux(save_movement)

    @property
    def leave_enemy_bomb(self):
        """
        Action that leaves an enemy bomb
        :brief: checks if it is safe to leave a bomb, if it is then
        the enemy leaves the bomb and moves to the save position
        """
        pos_i = self.get_x()
        pos_j = self.get_y()
        save_movement = []

        # The movement depends on the position of the enemy
        if pos_i % 2 == 0 and pos_j % 2 == 0:  # Even row and even column
            first_aux_movement = self.define_auxiliary_movements("row")
            second_aux_movement = self.define_auxiliary_movements("column")
            possible_movements = ["RRU", "RRD", "UUR", "UUL", "DDR", "DDL", "LLU", "LLD"]
            possible_movements += first_aux_movement + second_aux_movement
            save_movement = self.possible_movement_cases(pos_i, pos_j, possible_movements)

        elif pos_i % 2 == 1 and pos_j % 2 == 0:  # Odd row and even column
            aux_movement = self.define_auxiliary_movements("column")
            possible_movements = ["UR", "UL", "DR", "DL"] + aux_movement
            save_movement = self.possible_movement_cases(pos_i, pos_j, possible_movements)

        elif pos_i % 2 == 0 and pos_j % 2 == 1:  # Even row and odd column
            aux_movement = self.define_auxiliary_movements("row")

            possible_movements = ["RU", "RD", "LU", "LD"] + aux_movement
            save_movement = self.possible_movement_cases(pos_i, pos_j, possible_movements)

        if save_movement != []:  # Empty list means that leaving a bomb is not save
            self.new_bomb = True
            self.move_enemy_aux(save_movement)
            time.sleep(Fire.EXPLOSION_TIME / 1000)

        return save_movement

    def define_auxiliary_movements(self, p_type):
        """
        Defines the auxiliary movements that the enemy
        con do to avoid the bombs when adding one
        :return: a list with the auxiliary movements
        """
        auxiliary_movements = []
        first_movement = ""
        second_movement = ""
        if self.has_cross_bomb:
            return auxiliary_movements
        for count in range(0, self.explosion_radius+1):
            if p_type == "row":
                first_movement += 'R'
                second_movement += 'L'
            elif p_type == "column":
                first_movement += 'U'
                second_movement += 'D'
        auxiliary_movements.append(first_movement)
        auxiliary_movements.append(second_movement)
        return auxiliary_movements

    def possible_movement_cases(self, p_pos_i, p_pos_j, p_possible_movements):
        """
        Auxiliary method for the leave_enemy_bomb()
        :brief: determines which of the possible movements is possible
        :return: result_route -> list of the movements
        """
        possible_movements = p_possible_movements
        result_route = []
        # Checks every of the possible movements
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
        """
        Action that searches the closest power up
        :brief: given the closest power up the method
        uses the A* algorithm to move towards it
        """
        closest_power_up_position = self.find_closest_object("+h@s")  # chsz are all the possible power ups
        if closest_power_up_position == []:
            return
        enemy_i = self.get_x()
        enemy_j = self.get_y()
        target_i = closest_power_up_position[0]
        target_j = closest_power_up_position[1]
        a_star_route = Route.Route(enemy_i, enemy_j, target_i, target_j)
        self.move_enemy_aux(a_star_route.get_commands())

    def search_an_enemy(self):
        """
        Action that searches the closest player
        :brief: given the closest player (enemy or user)
        the method uses A* algorithm to move towards it
        """
        closest_enemy_position = self.find_closest_object("eu")  # "eu" means enemy or user
        if closest_enemy_position == []:
            self.choose_next_action()
        enemy_i = self.get_x()
        enemy_j = self.get_y()
        target_i = closest_enemy_position[0]
        target_j = closest_enemy_position[1]
        if isinstance(self, Enemy):
            a_star_route = Route.Route(enemy_i, enemy_j, target_i, target_j)
            self.move_enemy_aux(a_star_route.get_commands())

    def move_enemy_aux(self, movement_list):
        """
        Auxiliary method for moving based on the A* result
        """
        for movement in movement_list:
            if self.lives <= 0:
                return
            if self.is_movement_denied:
                break
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
                movement_list = self.leave_enemy_bomb
                if movement_list == []:
                    break
                return_route = self.get_back_to_position(movement_list) + [movement]
                self.move_enemy_aux(return_route)
            elif message == "Abort movement":
                break

    def get_back_to_position(self, movement_list):
        return_route = []
        for movement in movement_list:
            if movement == "right":
                return_route.append("left")
            elif movement == "left":
                return_route.append("right")
            elif movement == "up":
                return_route.append("down")
            elif movement == "down":
                return_route.append("up")
        return_route.reverse()
        return return_route

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
