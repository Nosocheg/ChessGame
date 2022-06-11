import pickle

FPS = 30

WIDTH = 800
HEIGHT = 600
SIZE = 500
CELL_SIZE = SIZE / 9.05
OFFSET_X = 43
OFFSET_Y = 114

WIDTH_MENU = 400
HEIGHT_MENU = 600

WITH_COMPUTER = 1
SINGLE_COMPUTER = 2
INTERNET_GAME = 3

FIRST_PLAYER = 1
SECOND_PLAYER = 2
DRAW = 3
DISCONNECTED = 4

WHITE = 1
BLACK = -1

WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
GREY = (195, 195, 195)
GREEN = (0, 255, 0)

image_dir = 'images/'


def entry(num):
    return chr(ord('a') + num % 8) + str(8 - num // 8)


def save_obj(obj, name):
    with open('data/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open('data/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
