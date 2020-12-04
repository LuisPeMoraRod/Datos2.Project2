import random
from Player import *

# Constants
CHROMOSOME_LENGTH = 100
AMOUNT_OF_ACTIONS = 4
AMOUNT_OF_MUTATIONS = 3


def define_chromosome():
    """
    Chromosomes list, each number represents an action
    0 -> chance to hide
    1 -> chance to search a power up
    2 -> change to search an enemy
    3 -> chance to leave a bomb
    """
    genes_list = []
    for i in range(0, CHROMOSOME_LENGTH):
        random_gene = random.randint(1, AMOUNT_OF_ACTIONS)  # doesn't include hiding action. This will be added later depending on the defined initial stat
        genes_list.append(random_gene)
    return genes_list


class GeneticAlgorithm:
    """
    Class that controls the genetic algorithm
    """

    def __init__(self, enemy):
        evasion_prob = enemy.evasion * 10
        self.chromosome = define_chromosome()
        self.chromosome = self.set_hide_probability(self.chromosome, evasion_prob)

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


    def combine(self, genes_list):
        """
        This method allows the crossover of the object of this class with
        the strongest one (measured before with the fitness function)
        The crossover range is completely randomly chosen
        """
        begin_crossover = random.randint(0, CHROMOSOME_LENGTH//2)
        end_crossover = random.randint(CHROMOSOME_LENGTH//2, CHROMOSOME_LENGTH)
        for i in range(begin_crossover, end_crossover):
            cross = random.randint(0, 2)
            if cross:
                self.chromosome[i] = genes_list[i]

    def mutate(self):
        """
        Method that mutates three of the genes of every chromosome
        This mutation is completely random
        """
        for i in range(0, AMOUNT_OF_MUTATIONS):
            chosen_gene = random.randint(0, CHROMOSOME_LENGTH-1)
            new_action = random.randint(0, AMOUNT_OF_ACTIONS)
            self.chromosome[chosen_gene] = new_action
