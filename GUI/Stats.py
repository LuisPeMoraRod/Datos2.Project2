from GUI.Image import *


class Stats:
    __instance = None

    @staticmethod
    def get_instance(block_size):
        if Stats.__instance is None:
            return Stats(block_size)
        return Stats.__instance

    def __init__(self, image):
        if Stats.__instance is not None:
            raise Exception("There's already a Stats object instantiated!")

        else:
            Stats.__instance = self
