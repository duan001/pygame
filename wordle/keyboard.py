import pygame
from config import GRID_Y, GRID_ROWS, TILE_SIZE, TILE_SPACING, SCREEN_WIDTH, KEY_HEIGHT, KEY_SPACING, LIGHT_GRAY, GRAY, GREEN, YELLOW, DARK_GRAY, WHITE

class Keyboard:
    def __init__(self):
        self.keys = []
        self.key_layout = [
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['^E', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '^B']
        ]
        self.key_states = {}
        self._create_keys()

    def _create_keys(self):
        start_y = GRID_Y + GRID_ROWS * (TILE_SIZE + TILE_SPACING) + 30
        total_width = 10 * (TILE_SIZE + KEY_SPACING) + (TILE_SIZE * 1.5 - TILE_SIZE)
        start_x = (SCREEN_WIDTH - total_width) // 2 + 25

        for row_idx, row in enumerate(self.key_layout):
            current_x = start_x
            row_y = start_y + row_idx * (KEY_HEIGHT + KEY_SPACING)

            for key in row:
                key_width = TILE_SIZE * 1.5 if key in ['ENTER', 'BACK'] else TILE_SIZE
                key_rect = pygame.Rect(current_x, row_y, key_width, KEY_HEIGHT)

                self.keys.append({
                    'label': key,
                    'rect': key_rect,
                    'state': 'default'
                })

                if key not in ['ENTER', 'BACK']:
                    self.key_states[key] = 'default'

                current_x += key_width + KEY_SPACING

    def update_state(self, letter, new_state):
        if letter not in ['ENTER', 'BACK']:
            old_state = self.key_states.get(letter, 'default')
            if new_state == 'correct':
                self.key_states[letter] = 'correct'
            elif new_state == 'present' and old_state != 'correct':
                self.key_states[letter] = 'present'
            elif new_state == 'absent' and old_state not in ['correct', 'present']:
                self.key_states[letter] = 'absent'

    def draw(self, screen):
        for key in self.keys:
            if key['label'] in ['ENTER', 'BACK']:
                color = LIGHT_GRAY
            else:
                state = self.key_states.get(key['label'], 'default')
                if state == 'correct':
                    color = GREEN
                elif state == 'present':
                    color = YELLOW
                elif state == 'absent':
                    color = DARK_GRAY
                else:
                    color = LIGHT_GRAY

            rect = key['rect']
            pygame.draw.rect(screen, color, rect, border_radius=5)
            pygame.draw.rect(screen, GRAY, rect, width=2, border_radius=5)

            label_surface = pygame.font.Font(None, 40).render(key['label'], True, WHITE)
            label_rect = label_surface.get_rect(center=(rect.centerx, rect.centery))
            screen.blit(label_surface, label_rect)

    def check_click(self, pos):
        for key in self.keys:
            if key['rect'].collidepoint(pos):
                return key['label']
        return None
