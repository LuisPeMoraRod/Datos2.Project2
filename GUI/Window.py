import pygame
from GUI.Board import *
import pyautogui

screen_width, screen_height = pyautogui.size()

class MainWindow:
    __instance = None
    __bg_image = pygame.image.load("images/background.jpg")
    __done = False
    __WIDTH = screen_width
    __HEIGHT = int(screen_height*0.9)

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
        screen = pygame.display.set_mode((self.__WIDTH, self.__HEIGHT))
        pygame.display.set_caption('BomberTEC')
        board = Board.get_instance(self.__WIDTH, self.__HEIGHT)
        board.enemies.update()
        # board.matrix.enemy0.update()

        while not self.__done:
            screen.blit(self.__bg_image, (0, 0))
            board.draw_base(screen)
            board.draw_board(screen)
            board.draw_stats(screen)
            board.draw_titles(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            board.users.update()
            # Random power up creation
            actual_time = pygame.time.get_ticks()
            board.create_power_up(actual_time)
            pygame.display.flip()
