import random
from Player import *
from PlayersList import *

# Constants
CHROMOSOME_LENGTH = 100
AMOUNT_OF_ACTIONS = 4
AMOUNT_OF_MUTATIONS = 15
CROSSOVER_TIME = 20000


class Genes:
    """
    Class that controls the genetic algorithm
    """

    def __init__(self, enemy):
        evasion_prob = enemy.evasion * 10
        self.chromosome = self.define_chromosome()
        self.chromosome = self.set_hide_probability(self.chromosome, evasion_prob)

    def define_chromosome(self):
        """
        Chromosomes list, each number represents an action
        0 -> chance to hide
        1 -> chance to search a power up
        2 -> change to search an enemy
        3 -> chance to leave a bomb
        """
        genes_list = []
        for i in range(0, CHROMOSOME_LENGTH):
            random_gene = random.randint(1,
                                         AMOUNT_OF_ACTIONS)  # doesn't include hiding action. This will be added later depending on the defined initial stat
            genes_list.append(random_gene)
        return genes_list

    def set_hide_probability(self, chromosome, probability):
        indexes = self.hide_indexes(probability)
        for index in indexes:
            chromosome[index] = 0
        return chromosome

    def hide_indexes(self, probability):
        """
        Define the indexes of the chromosomes list which will be changed to hiding action
        :param probability:
        :return:
        """
        cont = 0
        indexes = []
        while cont < probability:
            random_index = random.randint(0, CHROMOSOME_LENGTH - 1)
            if random_index not in indexes:
                indexes.append(random_index)
                cont += 1
        return indexes


class GeneticAlgorithm:
    """
    Class in charge of executing genetic algorithm
    """

    def __init__(self):
        self.players = PlayersList.get_instance()
        self.players_list = self.players.players_list
        self.last_crossover = 0
        self.user = None

    def set_user(self, user):
        self.user = user

    def combine(self, genes_list, enemy):
        """
        This method allows the crossover of the object of this class with
        the strongest one (measured before with the fitness function)
        The crossover range is completely randomly chosen
        """

        begin_crossover = random.randint(0, CHROMOSOME_LENGTH // 2)
        end_crossover = random.randint(CHROMOSOME_LENGTH // 2, CHROMOSOME_LENGTH)
        for i in range(begin_crossover, end_crossover):
            cross = random.randint(0, 2)
            if cross:
                enemy.genetics.chromosome[i] = genes_list[i]

    def mutate(self, enemy):
        """
        Method that mutates 15 of the genes of every chromosome
        This mutation is completely random
        """
        for i in range(0, AMOUNT_OF_MUTATIONS):
            chosen_gene = random.randint(0, CHROMOSOME_LENGTH - 1)
            new_action = random.randint(0, AMOUNT_OF_ACTIONS)
            enemy.genetics.chromosome[chosen_gene] = new_action

    def fitness_kills(self):
        """
        Method that selects the mvp since the last crossover depending who made the most amount of kills
        :return:
        """
        mvp = self.players_list[0]
        best_score = mvp.kills
        for i in range(0, len(self.players_list) - 1):
            if self.players_list[i].kills > best_score:
                best_score = self.players_list[i].kills
                mvp = self.players_list[i]
        return mvp

    def fitness_nearest_bomb(self):
        """
        Method that selects the mvp considering the enemy who put the nearest bomb to the User
        :return:
        """
        mvp = self.players_list[0]
        best_score = mvp.nearest_bomb
        for i in range(0, len(self.players_list) - 1):
            if self.players_list[i].nearest_bomb < best_score:
                best_score = self.players_list[i].nearest_bomb
                mvp = self.players_list[i]
        return mvp

    def crossover(self, current_time):
        """
        Executes crossover. Selects 2 best players: the one with most kills since the last crossover and the one who put
        :param current_time:
        :return:
        """
        if current_time - self.last_crossover > CROSSOVER_TIME:
            self.last_crossover = current_time
            mvp1 = self.fitness_kills()
            genes1 = mvp1.genetics.chromosome

            is_user_alive = True
            user = self.players_list[-1]
            if user.lose_live("Test") is not None:
                is_user_alive = False

            if is_user_alive:
                mvp2 = self.fitness_nearest_bomb()
                genes2 = mvp2.genetics.chromosome

            for i in range(0, len(self.players_list) - 1):
                self.combine(genes1, self.players_list[i])
                self.players_list[i].kills = 0
                if is_user_alive:
                    self.combine(genes2, self.players_list[i])
                self.mutate(self.players_list[i])
