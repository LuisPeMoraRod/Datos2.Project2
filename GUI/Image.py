import pygame


class Image:
    __instance = None

    @staticmethod
    def get_instance(block_size):
        if Image.__instance is None:
            return Image(block_size)
        return Image.__instance

    def __init__(self, block_size):
        if Image.__instance is not None:
            raise Exception("There's already an Image class instantiated!")

        else:
            Image.__instance = self
            self.light_grass = self.__load_image("images/light_grass.png", block_size + 1)
            self.dark_grass = self.__load_image("images/dark_grass.png", block_size + 1)
            self.breakable_block = self.__load_image("images/breakable.png", block_size + 1)
            self.unbreakable_block = self.__load_image("images/unbreakable.png", block_size + 1)
            self.fire = self.__load_image("images/fire.png", block_size + 1)
            self.border = self.__load_image("images/border.png", block_size + 1)
            self.healing = self.__load_image("images/healing.png", block_size + 1)
            self.shoe = self.__load_image("images/shoe.png", block_size + 1)
            self.shield = self.__load_image("images/shield.png", block_size + 1)
            self.cross_bomb = self.__load_image("images/cross_bomb.png", block_size + 1)
            self.bomb = self.__load_image("images/bomb.png", block_size + 1)

            self.enemy0 = self.__load_image("images/Enemy1/PNG/Wraith_02/PNG Sequences/Walking/Wraith_02_Moving Forward_000.png", block_size + 2)
            self.enemy1 = self.__load_image(
                "images/Enemy2/PNG/Minotaur_02/PNG Sequences/Walking/Minotaur_02_Walking_000.png", block_size + 2)
            self.enemy2 = self.__load_image(
                "images/Enemy2/PNG/Minotaur_01/PNG Sequences/Walking/Minotaur_01_Walking_000.png", block_size + 2)
            self.enemy3 = self.__load_image(
                "images/Enemy2/PNG/Minotaur_03/PNG Sequences/Walking/Minotaur_03_Walking_000.png", block_size + 2)
            self.enemy4 = self.__load_image(
                "images/Enemy3/PNG/Satyr_01/PNG Sequences/Walking/Satyr_01_Walking_000.png", block_size + 2)
            self.enemy5 = self.__load_image(
                "images/Enemy3/PNG/Satyr_02/PNG Sequences/Walking/Satyr_02_Walking_000.png", block_size + 2)
            self.enemy6 = self.__load_image(
                "images/Enemy3/PNG/Satyr_03/PNG Sequences/Walking/Satyr_03_Walking_000.png", block_size + 2)

            self.user = self.__load_image("images/user.png", block_size + 1)

    def __load_image(self, path, block_size):
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (block_size, block_size))
        return image
