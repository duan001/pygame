import pygame
from config import TILE_SIZE, GRAY, GREEN, YELLOW, DARK_GRAY, LIGHT_GRAY, BLACK, WHITE, BLUE

class Tile:
    def __init__(self, x, y, row, col):
        self.x = x
        self.y = y
        self.row = row
        self.col = col
        self.letter = ''
        self.state = 'default'
        self.color = WHITE
        self.is_cursor = False

    def draw(self, screen, font):
        if self.state == 'correct':
            color = GREEN
        elif self.state == 'present':
            color = YELLOW
        elif self.state == 'absent':
            color = DARK_GRAY
        elif self.state == 'current':
            color = LIGHT_GRAY
        else:
            color = WHITE

        rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, color, rect, border_radius=8)
        pygame.draw.rect(screen, GRAY, rect, width=3, border_radius=8)

        if self.letter:
            letter_surface = font.render(self.letter, True, BLACK)
            letter_rect = letter_surface.get_rect(center=(self.x + TILE_SIZE//2, self.y + TILE_SIZE//2))
            screen.blit(letter_surface, letter_rect)
        else:
            if self.is_cursor:
                cursor_surface = font.render('?', True, BLUE)
                cursor_rect = cursor_surface.get_rect(center=(self.x + TILE_SIZE//2, self.y + TILE_SIZE//2))
                screen.blit(cursor_surface, cursor_rect)
