# Game constants and configuration

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 780

# Colors
LIGHT_BLUE = (135, 206, 235)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (131, 131, 131)
DARK_GRAY = (58, 58, 58)
LIGHT_GRAY = (189, 189, 189)
GREEN = (54, 161, 93)
YELLOW = (177, 170, 61)
RED = (199, 65, 65)
PURPLE = (150, 100, 200)
BLUE = (67, 144, 237)

# Game settings
GRID_ROWS = 6
GRID_COLS = 5
TILE_SIZE = 55
TILE_SPACING = 6
KEYBOARD_ROWS = 3
KEY_HEIGHT = 60
KEY_SPACING = 4

# Grid position
GRID_X = (SCREEN_WIDTH - (GRID_COLS * (TILE_SIZE + TILE_SPACING) + TILE_SPACING)) // 2
GRID_Y = 150

# Font settings (will be initialized later)
TITLE_FONT = None
KEYBOARD_FONT = None
MESSAGE_FONT = None
SMALL_FONT = None

# Score
SCORE = 0

def init_fonts():
    """Initialize fonts after pygame is ready"""
    import pygame
    pygame.font.init()
    global TITLE_FONT, KEYBOARD_FONT, MESSAGE_FONT, SMALL_FONT
    TITLE_FONT = pygame.font.Font(None, 72)
    KEYBOARD_FONT = pygame.font.Font(None, 40)
    MESSAGE_FONT = pygame.font.Font(None, 48)
    SMALL_FONT = pygame.font.Font(None, 28)
    return TITLE_FONT, KEYBOARD_FONT, MESSAGE_FONT, SMALL_FONT
