import pygame
from elements import *


class Cell(pygame.sprite.Sprite):
    def __init__(self, num):
        pygame.sprite.Sprite.__init__(self)

        self.num = num

        self.img = pygame.image.load(image_dir + 'frame.png').convert_alpha()
        self.image = pygame.transform.scale(self.img, (CELL_SIZE, CELL_SIZE))
        self.image.set_colorkey(WHITE_COLOR)
        self.image.set_alpha(0)

        self.rect = self.image.get_rect(topleft=(OFFSET_X + num % 8 * CELL_SIZE,
                                                 OFFSET_Y + num // 8 * CELL_SIZE))
        self.figure = None

    def set_figure(self, figure):
        figure.rect = self.rect.copy()
        figure.cell = self
        if self.figure and self.figure.cell:
            self.figure.cell = None
        self.figure = figure
