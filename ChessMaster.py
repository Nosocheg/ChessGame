from stockfish import Stockfish
from elements import *


class ChessMaster:
    def __init__(self):
        self.stockfish = Stockfish('stockfish.exe')
        self.color = WHITE
        self.result = 0

    def game_result(self, result):
        self.result = result

    def get_game_result(self):
        return self.result

    def make_move(self, move):
        self.stockfish.make_moves_from_current_position([move])

    def is_move_correct(self, move):
        return self.stockfish.is_move_correct(move)

    def positions(self):
        return self.stockfish.get_fen_position()

    def possible_moves(self, num_from):
        position = entry(num_from)

        moves = []
        for num_to in range(64):
            move = position + entry(num_to)
            if self.stockfish.is_move_correct(move) or \
                    self.stockfish.is_move_correct(move + 'q'):
                moves.append(num_to)

        return moves

    def make_computer_move(self):
        self.make_move(self.stockfish.get_best_move())

    def set_fen_position(self, start_positions):
        self.stockfish.set_fen_position(start_positions)

    def get_evaluation(self):
        return self.stockfish.get_evaluation()
