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
            self.light_grass = self.__load_image("images/light_grass.png", block_size)
            self.dark_grass = self.__load_image("images/dark_grass.png", block_size)
            self.breakable_block = self.__load_image("images/breakable.png", block_size)
            self.unbreakable_block = self.__load_image("images/unbreakable.png", block_size)


    def __load_image(self, path, block_size):
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (block_size, block_size))
        return image
