import pygame
from elements import *

from Board import Board
from ChessMaster import ChessMaster
from Client import Client
import Button


class Menu:

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH_MENU, HEIGHT_MENU))
        pygame.display.set_caption('Меню')

        self.imageImg = pygame.image.load(image_dir + 'menu.png').convert()
        self.image = pygame.transform.scale(self.imageImg, (WIDTH_MENU, HEIGHT_MENU))

        message_image = pygame.image.load(image_dir + 'message_box.png').convert()
        self.message_image = pygame.transform.scale(message_image, (WIDTH_MENU * 0.8, HEIGHT_MENU * 0.8))
        self.message_image.set_colorkey(BLACK_COLOR)

        self.buttons = pygame.sprite.Group()

        start_y = 80
        dy = 100
        self.buttons.add(Button.Button(self.game, SINGLE_COMPUTER, 'Игра на одном компьютере', start_y))
        self.buttons.add(Button.Button(self.game, WITH_COMPUTER, 'Игра против компьютера', start_y + dy))
        self.buttons.add(Button.Button(self.game, INTERNET_GAME, 'Играть по Сети', start_y + 2 * dy))

        self.avatar = Button.Avatar(510, 300)
        self.buttons.add(self.avatar)
        self.running = False
        self.error = False
        self.stop_searching = False

    def game(self, mode):

        self.error = False
        self.stop_searching = False

        if mode in [WITH_COMPUTER, SINGLE_COMPUTER]:
            chess_master = ChessMaster()
        else:
            try:
                chess_master = Client(self)
            except ConnectionRefusedError:
                self.message_box('Сервер игры неактивен', 30)
                return

        if self.error:
            if not self.stop_searching:
                self.message_box('Сервер разорвал соединение', 25)
            self.error = False
            return

        board = Board(chess_master, mode)

        board.play()

        self.screen = pygame.display.set_mode((WIDTH_MENU, HEIGHT_MENU))
        if chess_master.get_game_result() == DISCONNECTED:
            if mode == INTERNET_GAME:
                self.message_box('Один из игроков разорвал соединение', 18)
            else:
                self.message_box('Вы вышли из игры', 25)
        else:
            if chess_master.get_game_result() == FIRST_PLAYER:
                color = WHITE
            else:
                color = BLACK
            if mode == INTERNET_GAME:
                if chess_master.color == color:
                    self.message_box('Вы победили', 30)
                else:
                    self.message_box('Вы проиграли', 30)
            elif mode == SINGLE_COMPUTER:
                if chess_master.color == color:
                    self.message_box('Белые победили', 30)
                else:
                    self.message_box('Чёрные победили', 30)
            elif mode == WITH_COMPUTER:
                if chess_master.color == color:
                    self.message_box('Вы победили', 30)
                else:
                    self.message_box('Компьютер победил', 30)

        if mode == INTERNET_GAME:
            chess_master.socket.close()

    def press(self, pos, buttons):
        for button in buttons:
            if button.rect.collidepoint(pos):
                button.pressed()
                self.screen = pygame.display.set_mode((WIDTH_MENU, HEIGHT_MENU))
                break

    def return_to_menu(self):
        self.stop_searching = True
        self.running = False

    def message_box(self, text, size):
        surf = pygame.Surface((WIDTH_MENU, HEIGHT_MENU))

        surf.fill(GREY)
        surf.set_alpha(200)

        buttons = pygame.sprite.Group()
        buttons.add(Button.Button(self.return_to_menu, None,
                                  'Назад', HEIGHT_MENU * 0.65, WIDTH_MENU * 0.5, WIDTH_MENU * 0.6, HEIGHT_MENU * 0.1))

        pictures = pygame.sprite.Group()
        pictures.add(Button.Picture(text, size, HEIGHT_MENU * 0.35, WIDTH_MENU * 0.5,
                                    WIDTH_MENU * 0.7, HEIGHT_MENU * 0.1))

        self.running = True
        while self.running:

            self.screen.fill(WHITE_COLOR)
            self.screen.blit(self.image, (0, 0))
            self.buttons.draw(self.screen)
            self.screen.blit(surf, (0, 0))
            self.screen.blit(self.message_image, (WIDTH_MENU * 0.1, HEIGHT_MENU * 0.1))

            buttons.draw(self.screen)
            pictures.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.stop_searching = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for button in buttons:
                            if button.rect.collidepoint(event.pos):
                                button.pressed()
                elif event.type == pygame.MOUSEMOTION:
                    Button.illuminate_buttons(event.pos, buttons)

            pygame.display.update()
            self.clock.tick(FPS)

        if text == 'Поиск соперника':
            return self.stop_searching

    def play(self):
        timer = 0
        running = True
        while running:
            self.screen.fill(WHITE_COLOR)
            self.screen.blit(self.image, (0, 0))
            self.buttons.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEMOTION:
                    Button.illuminate_buttons(event.pos, self.buttons)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if timer > 0.5:
                        if event.button == 1:
                            pos = event.pos
                            self.press(pos, self.buttons)
                        timer = 0

            pygame.display.update()
            timer += self.clock.tick(FPS) / 1000
