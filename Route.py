from Block import *
from Player import *
from Matrix import *
from PowerUp import *


class Route:
    route = []
    adjacent_nodes = []
    visited = []
    non_visited = []

    def __init__(self, player, i, j):
        self.player = player
        self.i = i
        self.j = j
        self.matrix = Matrix.get_instance().get_matrix()
        self.route = self.set_route()

    def __str__(self):
        route = ""
        for node in self.route:
            route += str(node[0])+" "+str(node[1])+" "+str(node[2])+" "+str(node[3])+"\n"
        return route

    def set_route(self):
        route = []
        for i in range(0, len(self.matrix)):
            for j in range(0, len(self.matrix[i])):
                if not isinstance(self.matrix[i][j], Unbreakable):
                    node = [i, j, 100000000, None]
                    route.append(node)
        return route

    def update_adjacents_nodes(self, i, j):
        """
        method that appends position of adjacent nodes to list
        :return:
        """
        self.create_adj_node(i, j - 1, i, j)
        self.create_adj_node(i - 1, j, i, j)
        self.create_adj_node(i, j + 1, i, j)
        self.create_adj_node(i + 1, j, i, j)

    def create_adj_node(self, i, j, prev_i, prev_j):
        node = self.matrix[i,j]
        if not isinstance(node, Unbreakable):
            node = self.Node(node, i, j, prev_i, prev_j)
            self.adjacent_nodes.append(node)

    class Node:
        def __init__(self, node_type, i, j, prev_i, prev_j):
            self.weight = self.get_weight(node_type)
            self.i = i
            self.j = j
            self.prev_i = prev_i
            self.prev_j = prev_j

        def get_weight(self, node_type):
            if isinstance(node_type, Breakable) or isinstance(node_type, Bomb) or isinstance(node_type, Player):
                return 5
            elif isinstance(node_type, Blank) or isinstance(node_type, PowerUp):
                return 1
