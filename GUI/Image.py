import pygame


class Image:
    """This class is used to upload all the images that are needed in the GUI"""
    __instance = None

    @staticmethod
    def get_instance(block_size):
        if Image.__instance is None:
            return Image(block_size)
        return Image.__instance

    def __init__(self, block_size):
        if Image.__instance is not None:
            raise Exception("There's already an Image object instantiated!")

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

            self.e0_portrait = self.__load_image("images/enemy1.png", block_size*2)
            self.e1_portrait = self.__load_image("images/enemy3.png", block_size * 2)
            self.e2_portrait = self.__load_image("images/enemy2.png", block_size * 2)
            self.e3_portrait = self.__load_image("images/enemy4.png", block_size * 2)
            self.e4_portrait = self.__load_image("images/enemy6.png", block_size * 2)
            self.e5_portrait = self.__load_image("images/enemy5.png", block_size * 2)
            self.e6_portrait = self.__load_image("images/enemy7.png", block_size * 2)
            self.user_portrait = self.__load_image("images/user_portrait.png", block_size * 4)

            self.shoe_e_collected = self.__load_image("images/shoe.png", int(0.5*block_size))
            self.shield_e_collected  = self.__load_image("images/shield.png", int(0.5*block_size))
            self.cross_bomb_e_collected  = self.__load_image("images/cross_bomb.png", int(0.5*block_size))

            self.shoe_e_stat = self.__load_image("images/shoe2.png", int(0.5*block_size))
            self.shield_e_stat = self.__load_image("images/shield2.png", int(0.5*block_size))
            self.cross_bomb_e_stat = self.__load_image("images/cross_bomb2.png", int(0.5*block_size))

            self.shoe_u_collected = self.__load_image("images/shoe.png", int(block_size))
            self.shield_u_collected = self.__load_image("images/shield.png", int(block_size))
            self.cross_bomb_u_collected = self.__load_image("images/cross_bomb.png", int(block_size))

            self.shoe_u_stat = self.__load_image("images/shoe2.png", int(block_size))
            self.shield_u_stat = self.__load_image("images/shield2.png", int(block_size))
            self.cross_bomb_u_stat = self.__load_image("images/cross_bomb2.png", int(block_size))


            self.title = self.__load_titles("images/title.png", block_size, 0.4)
            self.enemy_title = self.__load_titles("images/enemy_title.png", block_size, 0.15)

    def __load_image(self, path, block_size):
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (block_size, block_size))
        return image

    def __load_titles(self, path, block_size, title_proportion):
        title_width = 30*block_size*title_proportion
        title = pygame.image.load(path)
        title = pygame.transform.scale(title, (int(title_width), int(title_width/7)))
        return title
