import socket
import threading as th
import sys
from stockfish import Stockfish

from elements import *


class Player:
    def __init__(self, connection, client_address, name):
        self.connection = connection
        self.client_address = client_address
        self.name = name
        self.color = WHITE


class Server:
    def __init__(self):
        port = 10030
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        print(host_ip)

        addr = (host_ip, port)

        self.host = None

        self.current_player = 0

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.socket.bind(addr)
        self.socket.listen(10)

        thread = th.Thread(target=self.listen, daemon=True)
        thread.start()

        while True:
            data = input('\n>')
            if data == 'exit':
                self.socket.close()
                sys.exit()

    def listen(self):
        print('Запуск сервера...')
        while True:
            connection, client_address = self.socket.accept()

            name = connection.recv(1024).decode()

            player = Player(connection, client_address, name)

            print('Присоединился игрок', name)

            my_thread = th.Thread(target=self.try_join, args=(player,))
            my_thread.start()

    def recv(self, player):
        return player.connection.recv(1024).decode()

    def send(self, player, data):
        player.connection.sendall(data.encode())

    def try_join(self, player):

        if self.host:
            host = self.host
            host.color = WHITE
            player.color = BLACK
            self.host = None
            self.send(player, 'game')
            self.send(host, 'game')
            my_thread = th.Thread(target=self.game, args=(host, player))
            my_thread.start()
        else:
            self.host = player
            self.send(player, 'wait')
            data = self.recv(player)
            if data == 'stopped':
                self.host = None

    def game(self, pl_left, pl_right):
        stockfish = Stockfish('stockfish.exe')
        stockfish.turn = WHITE
        stockfish.finish = 0

        self.send(pl_left, 'white')
        self.send(pl_right, 'black')

        th_left = th.Thread(target=self.get_requests, args=(pl_left, stockfish))
        th_left.start()
        th_right = th.Thread(target=self.get_requests, args=(pl_right, stockfish))
        th_right.start()

    def get_requests(self, player, stockfish):

        while True:

            data = self.recv(player)
            if not data:
                break
            cmd, *answer = data.split('|')

            if cmd == 'move':
                move = answer[0]
                stockfish.make_moves_from_current_position([move])
                stockfish.turn *= -1
                self.send(player, 'good')
            elif cmd == 'correct':
                move = answer[0]
                if stockfish.is_move_correct(move):
                    self.send(player, 'correct')
                else:
                    self.send(player, 'incorrect')
            elif cmd == 'positions':
                self.send(player, stockfish.get_fen_position())
            elif cmd == 'possible':
                position = answer[0]
                moves = []
                for num_to in range(64):
                    move = position + chr(ord('a') + num_to % 8) + str(8 - num_to // 8)
                    if stockfish.is_move_correct(move) or \
                            stockfish.is_move_correct(move + 'q'):
                        moves.append(num_to)
                self.send(player, ' '.join(map(str, moves)))

            elif cmd == 'set':
                start_positions = answer[0]
                stockfish.set_fen_position(start_positions)
                self.send(player, 'good')
            elif cmd == 'evaluation':
                d = stockfish.get_evaluation()
                self.send(player, d['type'] + ' ' + str(d['value']))
            elif cmd == 'finish':
                stockfish.finish = int(answer[0])
            elif cmd == 'get_game_result':
                self.send(player, str(stockfish.finish))
