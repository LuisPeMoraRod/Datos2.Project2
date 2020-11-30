from Block import *
import Player
import Matrix
from PowerUp import PowerUp
from Bomb import *


class Route:

    def __init__(self, i_start, j_start, i_objective, j_objective):
        """
        Constructor method
        :param i_start:
        :param j_start:
        :param i_objective:
        :param j_objective:
        """
        self.frontier = []
        self.visited = []
        self.costs = []

        self.start = self.Node(i_start, j_start)
        self.frontier.append(self.start)
        self.add_node(self.start, None, 0)

        self.i_objective = i_objective
        self.j_objective = j_objective

        self.matrix = Matrix.Matrix.get_instance().get_matrix()

        self.find_objective()
        print(str(self))

    def __str__(self):
        route = self.get_route(self.i_objective, self.j_objective, [])
        commands = self.set_commands_list(route)
        route_str = ""
        for element in commands:
            route_str += element+"\n"
        return route_str

    def get_neighbors(self, node):
        """
        Gets list with the neighbors of node
        :param node:
        :return:
        """
        neighbors = []
        i = node.i
        j = node.j

        try:
            if j - 1 >= 0:
                if not isinstance(self.matrix[i][j-1], Unbreakable):
                    neighbor = self.Node(i, j-1)
                    neighbors.append(neighbor)
        except:
            pass

        try:
            if i - 1 >= 0:
                if not isinstance(self.matrix[i-1][j], Unbreakable):
                    neighbor = self.Node(i-1, j)
                    neighbors.append(neighbor)
        except:
            pass

        try:
            if not isinstance(self.matrix[i][j+1], Unbreakable):
                neighbor = self.Node(i, j+1)
                neighbors.append(neighbor)
        except:
            pass

        try:
            if not isinstance(self.matrix[i+1][j], Unbreakable):
                neighbor = self.Node(i+1, j)
                neighbors.append(neighbor)
        except:
            pass
        return neighbors

    def get_cost(self, next_node):
        """
        sets weight of moving to next_node depending on its class
        :param next_node:
        :return:
        """
        i = next_node.i
        j = next_node.j
        position = self.matrix[i][j]
        if isinstance(position, Breakable) or isinstance(position, Bomb):
            return 5
        elif isinstance(position, Player.Player):
            return 6
        elif isinstance(position, Matrix.Blank):
            return 1


    def find_objective(self):
        """
        Creates route to objective using A* algorithm
        :return:
        """
        while not len(self.frontier) == 0:
            current = self.frontier.pop(0)
            self.visited.append(current)

            if current.i == self.i_objective and current.j == self.j_objective:
                print("found it")
                break

            for neighbor in self.get_neighbors(current):
                new_cost = self.cost_so_far(current) + self.get_cost(neighbor) + self.heuristic(neighbor.i, neighbor.j, self.i_objective, self.j_objective)
                if not self.is_in_visited(neighbor) or self.is_lower(neighbor, new_cost):
                    self.visited.append(neighbor)
                    manhattan = self.heuristic(neighbor.i, neighbor.j, self.i_objective, self.j_objective)
                    self.frontier.append(neighbor)
                    self.add_node(neighbor, current, new_cost)

    def is_in_visited(self, node):
        """
        Checks if node is in self.visited list
        :param node:
        :return:
        """
        for element in self.visited:
            if node.i == element.i and node.j == element.j:
                return True
        return False

    def is_lower(self, node, cost):
        """
        Checks if cost to node is lower than current cost
        :param node:
        :param cost:
        :return:
        """
        for element in self.costs:
            if node.i == element[0].i and node.j == element[0].j:
                if cost < element[2]:
                    return True
        return False

    def add_node(self, node, comes_from, cost):
        """
        Adds new node to the list with the costs and previous for every node
        :param node:
        :param comes_from:
        :param cost:
        :return:
        """
        for element in self.costs:
            if element[0].i == node.i and element[0].j == node.j:
                element[1] = comes_from
                element[2] = cost
                return
        new_element = [node, comes_from, cost]
        self.costs.append(new_element)

    def cost_so_far(self, node):
        """
        Returns current cost so far to specific node
        :param node:
        :return:
        """
        for element in self.costs:
            if element[0].i == node.i and element[0].j == node.j:
                current_cost = element[2]
                return current_cost

    def get_route(self, i, j, route):
        """
        Generates list with route to follow including costs: element[0] = actual, element[1] = previous, element[2] = cost
        :param i:
        :param j:
        :param route:
        :return:
        """
        if i == self.start.i and j == self.start.j:
            return route
        for element in self.costs:
            if element[0].i == i and element[0].j == j:
                route.insert(0, (element[0].i, element[0].j))
                return self.get_route(element[1].i, element[1].j, route)

    def set_commands_list(self, route):
        """
        Generates list with commands to get to the objective
        :param i:
        :param j:
        :param route:
        :return:
        """
        commands = []
        if len(route) > 0:
            if route[0][0] - self.start.i > 0:
                commands.append("down")
            if route[0][0] - self.start.i < 0:
                commands.append("up")
            if route[0][1] - self.start.j > 0:
                commands.append("right")
            if route[0][1] - self.start.j < 0:
                commands.append("left")
            for i in range(0, len(route)-1):
                if route[i+1][0] - route[i][0] > 0:
                    commands.append("down")
                if route[i+1][0] - route[i][0] < 0:
                    commands.append("up")
                if route[i+1][1] - route[i][1] > 0:
                    commands.append("right")
                if route[i+1][1] - route[i][1] < 0:
                    commands.append("left")
        return commands

    def heuristic(self, i1, j1, i2, j2):
        """
        Calculates Manhattan distance between two points
        :param i1:
        :param j1:
        :param i2:
        :param j2:
        :return:
        """
        return abs(i1 - i2) + abs(j1 - j2)

    def add_to_frontier(self, node, priority):
        """
        Adds node to frontier list considering heuristic priority
        :param node:
        :param priority:
        :return:
        """
        frontier_length = len(self.frontier)
        if frontier_length == 0:
            self.frontier.append([node, priority])
        else:
            for i in range(0, frontier_length):
                if priority <= self.frontier[i][1]:
                    self.frontier.insert(0, [node, priority])
                else:
                    self.frontier.append([node, priority])


    def get_commands(self):
        route = self.get_route(self.i_objective, self.j_objective, [])
        commands = self.set_commands_list(route)
        return commands



    class Node:
        def __init__(self, i, j):
            self.i = i
            self.j = j

        def get_type(self):
            return None

        def __str__(self):
            indexes = str(self.i)+" "+str(self.j)
            return indexes
