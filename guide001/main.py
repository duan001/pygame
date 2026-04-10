import pygame
import sys
from src.player import Player

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My First Pygame")

# Clock for controlling framerate
clock = pygame.time.Clock()
FPS = 60

# Main game loop
running = True
player = Player(200, 200)
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    # Update game logic here
    keys = pygame.key.get_pressed()
    player.move(keys)

    # Draw everything
    screen.fill((0, 0, 0))  # Black background
    player.draw(screen)
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()