import pygame
import sys
import random
import os
from tile import Tile
from keyboard import Keyboard
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, LIGHT_BLUE, WHITE, BLACK, GRAY,
    DARK_GRAY, LIGHT_GRAY, GREEN, YELLOW, PURPLE, SCORE, TILE_SIZE,
    TILE_SPACING, GRID_X, GRID_Y
)

# Initialize fonts
import pygame
pygame.font.init()
TITLE_FONT = pygame.font.Font(None, 72)
KEYBOARD_FONT = pygame.font.Font(None, 40)
MESSAGE_FONT = pygame.font.Font(None, 48)
SMALL_FONT = pygame.font.Font(None, 28)

class Game:
    def __init__(self):
        global SCORE
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Wordle")
        self.clock = pygame.time.Clock()
        self.word_list = self.load_word_list()
        self.target_word = self.get_random_word(self.word_list)
        self.guesses = []
        self.current_guess = ''
        self.current_row = 0
        self.game_over = False
        self.won = False
        self.message = ''
        self.message_timer = 0
        self.keyboard = Keyboard()
        self.tiles = self._create_tiles()
        self.cursor_blink = False
        self.cursor_blink_timer = 0

    def load_word_list(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            word_list_path = os.path.join(script_dir, 'word_list.txt')
            with open(word_list_path, 'r') as f:
                words = [line.strip().upper() for line in f.readlines()]
            return words
        except FileNotFoundError:
            print("Warning: word_list.txt not found. Using default words.")
            return ['APPLE', 'WORLD', 'HELLO', 'PUZZL', 'CODE', 'PYTHON', 'WORD', 'GAME', 'SCREEN', 'COLOR']

    def get_random_word(self, word_list):
        return random.choice(word_list)

    def _create_tiles(self):
        tiles = []
        for row in range(6):
            for col in range(5):
                x = GRID_X + col * (TILE_SIZE + TILE_SPACING)
                y = GRID_Y + row * (TILE_SIZE + TILE_SPACING)
                tiles.append(Tile(x, y, row, col))
        return tiles

    def reset_game(self):
        global SCORE
        self.target_word = self.get_random_word(self.word_list)
        self.guesses = []
        self.current_guess = ''
        self.current_row = 0
        self.game_over = False
        self.won = False
        self.message = ''
        self.message_timer = 0
        self.keyboard = Keyboard()
        self.tiles = self._create_tiles()

    def handle_input(self, key):
        if self.game_over:
            return

        if key == 'BACK':
            if self.current_guess:
                self.current_guess = self.current_guess[:-1]
                if self.current_row < 6:
                    col = min(len(self.current_guess), 4)
                    tile_idx = self.current_row * 5 + col
                    if tile_idx < len(self.tiles):
                        self.tiles[tile_idx].letter = ''
        elif key == 'ENTER':
            if len(self.current_guess) == 5:
                self.submit_guess()
        elif key.isalpha() and len(self.current_guess) < 5:
            self.current_guess += key.upper()
            if self.current_row < 6:
                col = min(len(self.current_guess) - 1, 4)
                tile_idx = self.current_row * 5 + col
                if tile_idx < len(self.tiles):
                    self.tiles[tile_idx].letter = key.upper()

    def submit_guess(self):
        global SCORE
        if len(self.current_guess) != 5:
            self.message = 'Not enough letters'
            self.message_timer = 60
            return

        if self.current_guess not in self.word_list:
            self.message = 'Not in word list'
            self.message_timer = 60
            return

        self.guesses.append(self.current_guess)
        self._color_tiles()
        self._update_keyboard()

        if self.current_guess == self.target_word:
            self.won = True
            self.game_over = True
            SCORE += 1
            self.message = 'You Won!'
            self.message_timer = 120
        elif self.current_row >= 5:
            self.game_over = True
            self.message = f'Word: {self.target_word}'
            self.message_timer = 120
        else:
            self.current_row += 1

        self.current_guess = ''

    def _color_tiles(self):
        guess = self.current_guess
        target = self.target_word
        used_letters = [False] * 5

        for i, letter in enumerate(guess):
            if letter == target[i]:
                tile = self._get_tile(self.current_row, i)
                tile.state = 'correct'
                tile.color = GREEN
                used_letters[i] = True

        for i, letter in enumerate(guess):
            if not used_letters[i] and letter in target:
                for j, target_letter in enumerate(target):
                    if letter == target_letter and not used_letters[j]:
                        tile = self._get_tile(self.current_row, i)
                        tile.state = 'present'
                        tile.color = YELLOW
                        used_letters[j] = True
                        break
                else:
                    tile = self._get_tile(self.current_row, i)
                    tile.state = 'absent'
                    tile.color = DARK_GRAY

    def _update_keyboard(self):
        for i, letter in enumerate(self.current_guess):
            if self.target_word[i] == letter:
                self.keyboard.update_state(letter, 'correct')
            elif letter in self.target_word:
                self.keyboard.update_state(letter, 'present')
            else:
                self.keyboard.update_state(letter, 'absent')

    def _get_tile(self, row, col):
        return self.tiles[row * 5 + col]

    def draw(self):
        self.screen.fill(LIGHT_BLUE)

        title_surface = TITLE_FONT.render('WORDLE', True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, 40))
        self.screen.blit(title_surface, title_rect)

        glow_surface = pygame.Surface((title_surface.get_width() + 20, title_surface.get_height() + 20), pygame.SRCALPHA)
        glow_color = (PURPLE[0]*0.3, PURPLE[1]*0.3, PURPLE[2]*0.3, 100)
        pygame.draw.rect(glow_surface, glow_color, glow_surface.get_rect(), border_radius=10)
        self.screen.blit(glow_surface, (title_rect.x - 10, title_rect.y - 10))

        score_surface = SMALL_FONT.render(f'Score: {SCORE}', True, GRAY)
        self.screen.blit(score_surface, (50, SCREEN_HEIGHT - 40))

        attempts_surface = SMALL_FONT.render(f'Attempts: {self.current_row + 1}/6', True, GRAY)
        self.screen.blit(attempts_surface, (SCREEN_WIDTH - 120, SCREEN_HEIGHT - 40))

        for tile in self.tiles:
            tile.draw(self.screen, KEYBOARD_FONT)

        self.keyboard.draw(self.screen)

        if self.message:
            message_surface = MESSAGE_FONT.render(self.message, True, WHITE)
            message_rect = message_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            bg_rect = message_rect.inflate(40, 20)
            pygame.draw.rect(self.screen, LIGHT_BLUE, bg_rect, border_radius=10)
            pygame.draw.rect(self.screen, (0, 0, 0, 150), bg_rect, width=3, border_radius=10)
            self.screen.blit(message_surface, message_rect)

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.handle_input('ENTER')
            elif event.key == pygame.K_BACKSPACE:
                self.handle_input('BACK')
            elif event.key == pygame.K_a:
                self.handle_input('A')
            elif event.key == pygame.K_b:
                self.handle_input('B')
            elif event.key == pygame.K_c:
                self.handle_input('C')
            elif event.key == pygame.K_d:
                self.handle_input('D')
            elif event.key == pygame.K_e:
                self.handle_input('E')
            elif event.key == pygame.K_f:
                self.handle_input('F')
            elif event.key == pygame.K_g:
                self.handle_input('G')
            elif event.key == pygame.K_h:
                self.handle_input('H')
            elif event.key == pygame.K_i:
                self.handle_input('I')
            elif event.key == pygame.K_j:
                self.handle_input('J')
            elif event.key == pygame.K_k:
                self.handle_input('K')
            elif event.key == pygame.K_l:
                self.handle_input('L')
            elif event.key == pygame.K_m:
                self.handle_input('M')
            elif event.key == pygame.K_n:
                self.handle_input('N')
            elif event.key == pygame.K_o:
                self.handle_input('O')
            elif event.key == pygame.K_p:
                self.handle_input('P')
            elif event.key == pygame.K_q:
                self.handle_input('Q')
            elif event.key == pygame.K_r:
                self.handle_input('R')
            elif event.key == pygame.K_s:
                self.handle_input('S')
            elif event.key == pygame.K_t:
                self.handle_input('T')
            elif event.key == pygame.K_u:
                self.handle_input('U')
            elif event.key == pygame.K_v:
                self.handle_input('V')
            elif event.key == pygame.K_w:
                self.handle_input('W')
            elif event.key == pygame.K_x:
                self.handle_input('X')
            elif event.key == pygame.K_y:
                self.handle_input('Y')
            elif event.key == pygame.K_z:
                self.handle_input('Z')

        if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
            key_label = self.keyboard.check_click(event.pos)
            if key_label:
                if key_label == 'ENTER':
                    self.handle_input('ENTER')
                elif key_label == 'BACK':
                    self.handle_input('BACK')
                else:
                    self.handle_input(key_label)

        return True

    def update(self):
        global SCORE
        self.cursor_blink_timer += 1
        if self.cursor_blink_timer >= 30:
            self.cursor_blink = not self.cursor_blink
            self.cursor_blink_timer = 0

        for tile in self.tiles:
            tile.is_cursor = False

        if not self.game_over and self.current_row < 6:
            cursor_col = min(len(self.current_guess), 4)
            if cursor_col >= 5:
                cursor_col = 4
            start_idx = self.current_row * 5
            if start_idx + cursor_col < len(self.tiles):
                self.tiles[start_idx + cursor_col].is_cursor = self.cursor_blink

        if self.message_timer > 0:
            self.message_timer -= 1
            if self.message_timer == 0:
                self.message = ''
                if self.game_over:
                    # Wait for any key press to continue
                    waiting = True
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                waiting = False
                                break
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                    self.reset_game()
                    self.target_word = self.get_random_word(self.word_list)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                running = self.handle_event(event)

            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()
