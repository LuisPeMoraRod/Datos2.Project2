from Player import *


class PlayersList:
    """
    Class that stores every player (user o enemy) in a list. Implements a singleton pattern design
    """

    __instance = None

    @staticmethod
    def get_instance():
        """Static access method"""
        if PlayersList.__instance is None:
            return PlayersList()
        return PlayersList.__instance

    def __init__(self):
        """Virtually private constructor"""
        if PlayersList.__instance is not None:
            raise Exception("Private constructor, this is a Singleton class")
        else:
            PlayersList.__instance = self
            self.players_list = []
