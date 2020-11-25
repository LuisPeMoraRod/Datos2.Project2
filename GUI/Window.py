import sys

import pygame
from pygame.locals import *
from GUI.Board import *


HEIGHT = 750
WIDTH = 1400


class MainWindow:
    __instance = None
    __bg_image = pygame.image.load("images/background.png")
    __done = False

    @staticmethod
    def get_instance():
        if MainWindow.__instance is None:
            MainWindow()
        return MainWindow.__instance

    def __init__(self):

        if MainWindow.__instance is not None:
            raise Exception("There's already a Window running!")

        else:
            MainWindow.__instance = self
            self.__create_window()

    def __create_window(self):

        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
        pygame.display.set_caption('BomberTEC')
        board = Board.get_instace()

        # Frame quantity
        frame = 0
        FPS = 2
        clock = pygame.time.Clock()

        while not self.__done:
            # clock.tick(FPS)
            screen.blit(self.__bg_image, (0, 0))
            board.draw_base(screen)
            board.draw_board(screen)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            board.players.update()

            # Random power up creation
            board.create_power_up(frame)

            frame += 1

            pygame.display.flip()
