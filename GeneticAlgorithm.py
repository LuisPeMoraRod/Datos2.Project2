import random

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
        random_gene = random.randint(0, AMOUNT_OF_ACTIONS)
        genes_list.append(random_gene)
    return genes_list


class GeneticAlgorithm:
    """
    Class that controls the genetic algorithm
    """

    def __init__(self):
        self.chromosome = define_chromosome()

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
