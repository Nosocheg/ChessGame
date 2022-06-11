import socket
import threading as th

from elements import *


class Client:
    def __init__(self, menu):

        self.menu = menu

        port = 10030
        host_ip = '192.168.56.1'
        addr = (host_ip, port)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(addr)

        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        user_data = load_obj('data')

        name = user_data['name']

        self.send(name)

        ready_msg = self.recv()

        self.menu.error = False

        if ready_msg == 'wait':
            thread = th.Thread(target=self.wait_opponent, daemon=True)
            thread.start()
            stopped = self.menu.message_box('Поиск соперника', 30)
            if stopped:
                self.send('stopped')
                self.menu.error = True
                self.socket.close()
                return
            else:
                self.send('good')

        if self.menu.error:
            self.socket.close()
            return

        self.color = WHITE if self.recv() == 'white' else BLACK

    def game_result(self, result):
        self.send('finish|' + str(result))

    def get_game_result(self):
        self.send('get_game_result')
        data = int(self.recv())
        return data

    def wait_opponent(self):
        try:
            opponent_found = self.recv()
        except ConnectionResetError:
            self.menu.running = False
            self.menu.error = True
        except ConnectionAbortedError:
            pass

        self.menu.running = False

    def send(self, data):
        self.socket.send(data.encode())

    def recv(self):
        return self.socket.recv(1024).decode()

    def close(self):
        self.socket.close()

    def make_move(self, move):
        self.send('move|' + move)
        data = self.recv()

    def is_move_correct(self, move):
        self.send('correct|' + move)
        data = self.recv()

        return data == 'correct'

    def positions(self):
        self.send('positions')
        return self.recv()

    def possible_moves(self, num_from):
        self.send('possible|' + entry(num_from))
        data = self.recv()
        return list(map(int, data.split()))

    def make_computer_move(self):
        pass

    def set_fen_position(self, start_positions):
        self.send('set|' + start_positions)
        data = self.recv()

    def get_evaluation(self):
        self.send('evaluation')
        data = self.recv()
        tp, value = data.split()
        d = {'type': tp, 'value': int(value)}
        return d
