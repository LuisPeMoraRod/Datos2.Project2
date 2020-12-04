import random
from Player import *
from PlayersList import *

# Constants
CHROMOSOME_LENGTH = 100
AMOUNT_OF_ACTIONS = 4
AMOUNT_OF_MUTATIONS = 3
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

    def mutate(self):
        """
        Method that mutates three of the genes of every chromosome
        This mutation is completely random
        """
        for i in range(0, AMOUNT_OF_MUTATIONS):
            chosen_gene = random.randint(0, CHROMOSOME_LENGTH - 1)
            new_action = random.randint(0, AMOUNT_OF_ACTIONS)
            self.chromosome[chosen_gene] = new_action

    def fitness(self):
        """
        Method that selects the mvp since the last crossover depending on two factors: most amount of kills and nearest bomb to User player
        :return:
        """
        mvp = self.players_list[0]
        best_score = mvp.kills
        for player in self.players_list:
            if player.kills > best_score:
                best_score = player.kills
                mvp = player
        return mvp

    def crossover(self, current_time):
        if current_time - self.last_crossover > CROSSOVER_TIME:
            mvp = self.fitness()
            self.last_crossover = current_time
            print("MVP: " + str(mvp) + ", kills: "+str(mvp.kills))
            genes = mvp.genetics.chromosome

            for player in self.players_list:
                self.combine(genes, player)
                player.kills = 0






