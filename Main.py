import sys
from pygame.locals import *
from Matrix import *

# Constants
FPS = 2

matrix0 = Matrix.get_instance()
print(matrix0)

# Load pygame window and clock
pygame.init()
SCREEN = pygame.display.set_mode((500, 480))
pygame.display.set_caption('BomberTEC')
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

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    # Sprites update
    players.update()
    print('\n')
    print(matrix0)
