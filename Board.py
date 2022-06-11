import pygame
import Button

from elements import *

from Cell import Cell
from Figure import Figure


class Board:
    def __init__(self, chess_master, mode):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Шахматы')

        self.imageImg = pygame.image.load(image_dir + 'board.png').convert()
        self.image = pygame.transform.scale(self.imageImg, (WIDTH, HEIGHT))

        self.figures = {
            'r': [Figure('black_rook.png', BLACK) for _ in range(2)],
            'R': [Figure('white_rook.png', WHITE) for _ in range(2)],
            'n': [Figure('black_knight.png', BLACK) for _ in range(2)],
            'N': [Figure('white_knight.png', WHITE) for _ in range(2)],
            'b': [Figure('black_bishop.png', BLACK) for _ in range(2)],
            'B': [Figure('white_bishop.png', WHITE) for _ in range(2)],
            'q': [Figure('black_queen.png', BLACK)],
            'Q': [Figure('white_queen.png', WHITE)],
            'k': [Figure('black_king.png', BLACK)],
            'K': [Figure('white_king.png', WHITE)],
            'p': [Figure('black_pawn.png', BLACK) for _ in range(8)],
            'P': [Figure('white_pawn.png', WHITE) for _ in range(8)],
        }

        self.white_figures = pygame.sprite.Group()
        for c in 'RNBQKP':
            self.white_figures.add(*self.figures[c])

        self.black_figures = pygame.sprite.Group()
        for c in 'rnbqkp':
            self.black_figures.add(*self.figures[c])

        self.cells = pygame.sprite.Group()
        self.list_cells = []

        for num in range(64):
            cell = Cell(num)
            self.cells.add(cell)
            self.list_cells.append(cell)

        self.turn = WHITE

        # start_positions = 'k7/7R/8/8/8/8/8/KR6 w - 39 39'
        start_positions = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        self.set_positions(start_positions)

        self.touched = None
        self.cell_from = None
        self.chess_master = chess_master
        self.chess_master.set_fen_position(start_positions)

        self.mode = mode
        self.possible_moves = []
        self.game_result = None
        self.running = True

        self.pictures = pygame.sprite.Group()

        if mode == SINGLE_COMPUTER:
            text = 'Совместная игра'
        else:
            text = 'Вы играете за белых' if self.chess_master.color == WHITE else 'Вы играете за чёрных'

        self.pictures.add(Button.Picture(text, 30, HEIGHT * 0.1, WIDTH * 0.8, WIDTH_MENU * 0.7, HEIGHT_MENU * 0.1))

    def return_menu(self):
        self.running = False

    def set_positions(self, positions):

        for figures in [self.black_figures, self.white_figures]:
            for figure in figures:
                figure.remove()

        num = 0
        i = 0
        while num < 64:
            c = positions[i]
            if c in self.figures:
                figures = self.figures[c]

                j = 0
                while figures[j].cell:
                    j += 1
                figure = figures[j]

                self.list_cells[num].set_figure(figure)
                num += 1
            elif c.isdigit():
                num += int(c)
            i += 1

        self.turn = WHITE if positions[i + 1] == 'w' else BLACK

    def check_frames(self, pos):
        for cell in self.cells:
            if cell.rect.collidepoint(pos):
                cell.image.set_alpha(255)
            else:
                cell.image.set_alpha(0)

    def show_possible_moves(self):
        for move in self.possible_moves:
            cell = self.list_cells[move]
            backlight = pygame.Surface(cell.rect.size).convert_alpha()
            backlight.fill(GREEN)
            backlight.set_alpha(100)
            self.screen.blit(backlight, cell.rect.topleft)

    def touch(self, pos):
        if not self.touched:
            figures = self.white_figures if self.turn == WHITE else self.black_figures
            for figure in figures:
                if figure.rect and figure.rect.collidepoint(pos):
                    self.touched = figure
                    self.cell_from = figure.cell
                    figure.cell = None
                    self.cell_from.figure = None

                    self.possible_moves = self.chess_master.possible_moves(self.cell_from.num)
                    break

    def move_touched(self, pos):
        if self.touched:
            self.touched.rect.center = pos

    def check_mate(self):
        evaluation = self.chess_master.get_evaluation()
        if evaluation['type'] == 'mate' and evaluation['value'] == 0:
            if self.turn == WHITE:
                self.chess_master.game_result(SECOND_PLAYER)
            else:
                self.chess_master.game_result(FIRST_PLAYER)
        elif evaluation['type'] == 'cp' and evaluation['value'] == 0 and False:
            self.chess_master.game_result(DRAW)

    def put_touched(self, pos):
        turn_from = entry(self.cell_from.num)

        move = ''
        cell_to = None
        for cell in self.cells:
            if cell.rect.collidepoint(pos):
                cell_to = cell
                move = turn_from + entry(cell_to.num)
                break

        if cell_to:
            correct = False
            if self.chess_master.is_move_correct(move):
                self.chess_master.make_move(move)
                correct = True
            if self.chess_master.is_move_correct(move + 'q'):
                self.chess_master.make_move(move + 'q')

                if self.turn == BLACK:
                    queen = Figure('black_queen.png', BLACK)
                    self.black_figures.add(queen)
                    self.figures['q'].append(queen)
                else:
                    queen = Figure('white_queen.png', WHITE)
                    self.white_figures.add(queen)
                    self.figures['Q'].append(queen)
                correct = True

            self.set_positions(self.chess_master.positions())
            self.check_mate()

            if correct and not self.game_result:
                if self.mode == WITH_COMPUTER:
                    self.make_computer_move()
                    self.set_positions(self.chess_master.positions())
                    self.check_mate()

        self.cell_from = None
        self.touched = None

        return False

    def make_computer_move(self):
        self.chess_master.make_computer_move()

    def play(self):
        timer = 0
        pict = None
        while self.running:
            self.screen.fill(WHITE_COLOR)
            self.screen.blit(self.image, (0, 0))

            if timer > 1 or timer == 0:
                if pict in self.pictures:
                    self.pictures.remove(pict)
                text = 'Ход белых' if self.turn == WHITE else 'Ход чёрных'
                pict = Button.Picture(text, 30, HEIGHT * 0.2, WIDTH * 0.8, WIDTH_MENU * 0.6, HEIGHT_MENU * 0.1)
                self.pictures.add(pict)
                timer = 0

            self.pictures.draw(self.screen)

            self.cells.draw(self.screen)
            for figures in [self.black_figures, self.white_figures]:
                alive = pygame.sprite.Group([figure for figure in figures if figure.rect])
                alive.draw(self.screen)
            self.show_possible_moves()

            if self.chess_master.get_game_result() not in [0, DISCONNECTED]:
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.chess_master.game_result(DISCONNECTED)
                    break

                if self.chess_master.color == self.turn or self.mode == SINGLE_COMPUTER:
                    if event.type == pygame.MOUSEMOTION:
                        pos = event.pos
                        self.check_frames(pos)
                        self.move_touched(pos)

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = event.pos
                        if event.button == 1:
                            self.touch(pos)

                    elif event.type == pygame.MOUSEBUTTONUP:
                        pos = event.pos
                        if event.button == 1:
                            if self.touched:
                                self.put_touched(pos)
                            self.possible_moves = []
                else:
                    self.set_positions(self.chess_master.positions())

            pygame.display.update()
            timer += self.clock.tick(FPS) / 1000

            if self.chess_master.get_game_result() == DISCONNECTED:
                self.running = False
