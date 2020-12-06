import pygame
from PlayersList import *
from Route import *


class Bomb:
    """
    Class for the bombs objects
    """
    # Static Constants
    TIME_TO_DETONATE = 2200

    def __init__(self, position, matrix, bomb_radius, player):
        self.start_time = pygame.time.get_ticks()
        self.position = position
        self.matrix = matrix
        self.radius = bomb_radius
        self.player = player
        self.players_list = PlayersList.get_instance()
        dist_to_user = self.distance_to_user()
        self.set_nearest_bomb(dist_to_user)

    def detonate(self):
        actual_time = pygame.time.get_ticks()
        if actual_time - self.start_time > Bomb.TIME_TO_DETONATE:
            return True
        return False

    def __str__(self):
        """
        ASCII identifier for the bombs
        :return: "o"
        """
        return "o"

    def distance_to_user(self):
        """
        Gets distance from bomb to User using A* algorithm
        :return:
        """
        user = self.players_list.players_list[-1]
        i_bomb = self.position[0]
        j_bomb = self.position[1]
        i_objective = user.get_x()
        j_objective = user.get_y()
        a_star = Route(i_bomb, j_bomb, i_objective, j_objective)
        route = a_star.get_commands()
        distance = len(route)
        return distance

    def set_nearest_bomb(self, distance):
        """
        Sets distance of nearest_bomb of the enemy who put the bomb
        :param distance:
        :return:
        """
        if distance < self.player.nearest_bomb:
            self.player.nearest_bomb = distance
