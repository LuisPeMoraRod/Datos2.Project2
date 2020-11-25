import sys
from pygame.locals import *
from Matrix import *
from GUI.Window import *

# Constants
FPS = 2

MainWindow.get_instance()

clock = pygame.time.Clock()

# Sprites group
players = pygame.sprite.Group()
players.add(matrix0.user)
players.add(matrix0.enemy0)
players.add(matrix0.enemy1)
players.add(matrix0.enemy2)
players.add(matrix0.enemy3)
players.add(matrix0.enemy4)
players.add(matrix0.enemy5)
players.add(matrix0.enemy6)


