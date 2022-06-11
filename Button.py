import pygame

from elements import *


class Button(pygame.sprite.Sprite):
    def __init__(self, code_to_run, mode, text, y, x=WIDTH_MENU // 2, width=300, height=80):
        pygame.sprite.Sprite.__init__(self)

        self.code_to_run = code_to_run
        self.mode = mode

        self.font = pygame.font.SysFont("Arial", 18)
        self.textSurf = self.font.render(text, True, BLACK_COLOR)

        self.imageImg = pygame.image.load(image_dir + 'button.png').convert_alpha()

        self.image = pygame.transform.scale(self.imageImg, (width, height))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.image.set_colorkey(WHITE_COLOR)

        w = self.textSurf.get_width()
        h = self.textSurf.get_height()

        self.image.blit(self.textSurf, [width / 2 - w / 2, height / 2 - h / 2])

    def pressed(self):
        if self.mode:
            self.code_to_run(mode=self.mode)
        else:
            self.code_to_run()


class Picture(pygame.sprite.Sprite):
    def __init__(self, text, size, y, x=WIDTH_MENU // 2, width=250, height=70):
        pygame.sprite.Sprite.__init__(self)

        self.font = pygame.font.SysFont("Alias", size)
        self.textSurf = self.font.render(text, 1, BLACK_COLOR)

        image = pygame.image.load(image_dir + 'text_frame.png').convert_alpha()
        self.image = pygame.transform.scale(image, (width, height))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        w = self.textSurf.get_width()
        h = self.textSurf.get_height()

        self.image.blit(self.textSurf, [width / 2 - w / 2, height / 2 - h / 2])


class Avatar(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        user_data = load_obj('data')
        if not user_data['avatar']:
            self.imageImg = pygame.image.load(image_dir + 'no_avatar.png').convert_alpha()
        else:
            self.imageImg = pygame.image.load('data/' + user_data['avatar']).convert_alpha()

        w, h = self.imageImg.get_size()
        width = w * 150 / h
        height = 150
        self.image = pygame.transform.scale(self.imageImg, (width, height))

        self.rect = self.image.get_rect()
        self.rect.center = (y, x)

    def pressed(self):
        pass


def illuminate_buttons(pos, buttons):
    for button in buttons:
        if button.rect.collidepoint(pos):
            button.image.set_alpha(255)
        else:
            button.image.set_alpha(200)
