"""Information and recovery controls for an adjacent module."""

import pygame

from config import COLOR_ACCENT, COLOR_UI_TEXT


class ModulePanel:
    """Displays a nearby building and the controls for recovering it."""

    def __init__(self, width, height):
        self.module = None
        self.rect = pygame.Rect(0, 0, 580, 260)
        self.rect.center = (width // 2, height // 2)
        self.font = pygame.font.Font(None, 25)
        self.overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 150))

    def draw(self, screen):
        screen.blit(self.overlay, (0, 0))
        pygame.draw.rect(screen, (22, 28, 36), self.rect)
        pygame.draw.rect(screen, COLOR_ACCENT, self.rect, width=2)
        y = self.rect.y + 24
        screen.blit(
            self.font.render(self.module.name, True, COLOR_ACCENT),
            (self.rect.x + 24, y),
        )
        y += 42
        line = ""
        for word in self.module.description.split():
            candidate = f"{line} {word}".strip()
            if self.font.size(candidate)[0] > self.rect.width - 48:
                screen.blit(
                    self.font.render(line, True, COLOR_UI_TEXT), (self.rect.x + 24, y)
                )
                y += 26
                line = word
            else:
                line = candidate
        screen.blit(self.font.render(line, True, COLOR_UI_TEXT), (self.rect.x + 24, y))
        for text, offset in [
            ("R: recoger módulo al inventario", 76),
            ("E o Esc: cerrar", 42),
        ]:
            screen.blit(
                self.font.render(text, True, COLOR_UI_TEXT),
                (self.rect.x + 24, self.rect.bottom - offset),
            )
