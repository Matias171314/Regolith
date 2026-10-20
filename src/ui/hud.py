"""Player status display."""

import pygame

from config import COLOR_UI_TEXT


class HUD:
    def __init__(self):
        self.rect = pygame.Rect(12, 12, 228, 132)
        self.font = pygame.font.Font(None, 23)

    def draw(self, screen, player):
        pygame.draw.rect(screen, (22, 28, 36), self.rect)
        stats = [
            ("Salud", player.health, (220, 80, 80)),
            ("Energía", player.energy, (230, 180, 60)),
            ("Oxígeno", player.oxygen, (60, 190, 220)),
        ]
        for i, (name, value, color) in enumerate(stats):
            y = self.rect.y + 10 + i * 32
            label = self.font.render(f"{name}: {value}/100", True, COLOR_UI_TEXT)
            screen.blit(label, (self.rect.x + 12, y))
            bar = pygame.Rect(self.rect.x + 12, y + 19, 204, 6)
            pygame.draw.rect(screen, (48, 54, 61), bar)
            fill = bar.copy()
            fill.width = round(bar.width * max(0, min(value, 100)) / 100)
            pygame.draw.rect(screen, color, fill)
        hint = self.font.render("Tab: inventario", True, COLOR_UI_TEXT)
        screen.blit(hint, (self.rect.x + 12, self.rect.bottom - 23))
