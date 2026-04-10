# Pygame Programming - Step-by-Step Guide

## Overview
This guide will walk you through creating your first Pygame project, from setup to a complete playable game.

---

## Step 1: Project Setup

### 1.1 Create Project Structure
```bash
cd ~/project03
mkdir pygame-basics
cd pygame-basics
```

### 1.2 Install Pygame
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install pygame
```

### 1.3 Project Folder Structure
```
pygame-basics/
├── main.py
├── assets/
│   ├── images/
│   ├── sounds/
│   └── fonts/
├── src/
│   ├── player.py
│   ├── enemy.py
│   └── game.py
└── README.md
```

---

## Step 2: Your First Pygame Program

### 2.1 Create `main.py`
```python
import pygame
import sys

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
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update game logic here
    
    # Draw everything
    screen.fill((0, 0, 0))  # Black background
    
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
```

### 2.2 Run It
```bash
python main.py
```

---

## Step 3: Understanding Pygame Basics

### 3.1 The Pygame Module Structure
- **pygame.display** - Window management
- **pygame.time** - Clock and timing
- **pygame.event** - Keyboard, mouse input
- **pygame.draw** - Drawing shapes
- **pygame.image** - Loading images
- **pygame.sprite** - Sprite management
- **pygame.font** - Text rendering

### 3.2 Game Loop Structure
```python
while running:
    # 1. Event handling (input)
    # 2. Update game state (logic)
    # 3. Render graphics (draw)
    # 4. Control framerate
```

---

## Step 4: Adding Interactive Elements

### 4.1 Keyboard Input
```python
# Track key states
keys = pygame.key.get_pressed()

if keys[pygame.K_LEFT]:
    player.x -= 5
if keys[pygame.K_RIGHT]:
    player.x += 5
if keys[pygame.K_SPACE]:
    jump()
```

### 4.2 Mouse Input
```python
# Get mouse position
mouse_x, mouse_y = pygame.mouse.get_pos()

# Check for mouse clicks
if pygame.mouse.get_pressed()[0]:  # Left click
    print("Clicked at:", mouse_x, mouse_y)
```

---

## Step 5: Drawing Shapes and Sprites

### 5.1 Drawing Shapes
```python
# Draw a rectangle
pygame.draw.rect(screen, (255, 0, 0), (x, y, width, height))

# Draw a circle
pygame.draw.circle(screen, (0, 255, 0), (center_x, center_y), radius)

# Draw a line
pygame.draw.line(screen, (0, 0, 255), (x1, y1), (x2, y2), width)
```

### 5.2 Loading and Displaying Images
```python
# Load image
player_image = pygame.image.load('assets/images/player.png')

# Resize if needed
player_image = pygame.transform.scale(player_image, (50, 50))

# Blit (draw) to screen
screen.blit(player_image, (x, y))
```

---

## Step 6: Organizing with Classes

### 6.1 Create `src/player.py`
```python
import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.color = (0, 150, 255)
        self.speed = 5
        
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < 800 - self.width:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < 600 - self.height:
            self.y += self.speed
            
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
```

### 6.2 Update `main.py`
```python
import pygame
import sys
from src.player import Player

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Player Movement Demo")
clock = pygame.time.Clock()

player = Player(375, 275)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    player.move(keys)
    
    screen.fill((30, 30, 30))
    player.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
```

---

## Step 7: Adding Game Objects

### 7.1 Create `src/game.py` - Game Manager
```python
import pygame
from src.player import Player
from src.enemy import Enemy

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Game Demo")
        self.clock = pygame.time.Clock()
        self.player = Player(375, 275)
        self.enemies = []
        self.font = pygame.font.Font(None, 36)
        
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.enemies.append(Enemy(700, 300))
            
            keys = pygame.key.get_pressed()
            self.player.move(keys)
            
            # Update enemies
            for enemy in self.enemies[:]:
                enemy.move()
                if enemy.x < -50:
                    self.enemies.remove(enemy)
            
            # Check collisions
            for enemy in self.enemies:
                if self.player.x < enemy.x + enemy.width and \
                   self.player.x + self.player.width > enemy.x and \
                   self.player.y < enemy.y + enemy.height and \
                   self.player.y + self.player.height > enemy.y:
                    print("Collision!")
            
            # Draw
            self.screen.fill((0, 0, 0))
            self.player.draw(self.screen)
            for enemy in self.enemies:
                enemy.draw(self.screen)
            
            # Draw score
            score_text = self.font.render(f"Enemies: {len(self.enemies)}", True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
```

### 7.2 Create `src/enemy.py`
```python
import pygame

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.color = (255, 0, 0)
        self.speed = 3
        
    def move(self):
        self.x -= self.speed
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
```

### 7.3 Updated `main.py`
```python
from src.game import Game

game = Game()
game.run()
```

---

## Step 8: Advanced Features

### 8.1 Sound Effects
```python
# Load sound
jump_sound = pygame.mixer.Sound('assets/sounds/jump.wav')

# Play sound
jump_sound.play()

# Or with volume control
jump_sound.set_volume(0.5)
```

### 8.2 Sprites and Groups
```python
# Create sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Use sprites instead of manual management
player = PlayerSprite(375, 275)
all_sprites.add(player)
```

---

## Step 9: Next Steps & Practice Projects

### Practice Projects (in order):
1. **Moving Square** - Basic movement with keyboard
2. **Pong Clone** - Two paddles, bouncing ball
3. **Space Invaders** - Shooter with enemies
4. **Platformer** - Jumping, platforms, gravity
5. **Top-Down Shooter** - Mouse aiming, enemies

### Resources:
- **Official Docs:** https://www.pygame.org/docs/
- **Pygame Cheat Sheet:** https://opentechguides.com/how-to/article/python/1/pygame-cheat-sheet.html
- **GameDev Tutorials:** https://opentechguides.com/python-pygame.html

---

## Tips for Success

1. **Start small** - Build incrementally
2. **Test often** - Run frequently to catch bugs
3. **Comment your code** - Explain why, not what
4. **Use debug prints** - `print()` is your friend
5. **Read the docs** - pygame has excellent documentation
6. **Copy and modify** - Start from examples, learn by doing

---

**Happy coding! 🎮**
