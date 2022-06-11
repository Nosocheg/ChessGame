import pygame
from elements import *


class Figure(pygame.sprite.Sprite):

    def __init__(self, image_name, color):
        pygame.sprite.Sprite.__init__(self)

        image = pygame.image.load(image_dir + image_name).convert()
        self.image = pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE))
        self.image.set_colorkey(GREY)

        self.color = color
        self.cell = None
        self.rect = None

    def remove(self):
        if self.cell:
            self.cell.figure = None
        self.cell = None
        self.rect = None
