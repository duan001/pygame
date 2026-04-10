import pygame
import sys
from tile import Tile
from keyboard import Keyboard
from game import Game, SCORE
from config import TILE_SIZE

pygame.init()

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()
