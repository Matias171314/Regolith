"""Quick access to the first five inventory slots."""

import pygame

from config import COLOR_ACCENT, COLOR_GRID, COLOR_UI_TEXT


class Toolbar:
    """Displays and selects the first five inventory slots."""

    def __init__(self, y, width, height):
        self.rect = pygame.Rect(0, y, width, height)
        self.font = pygame.font.Font(None, 20)
        slot_width = 216
        gap = 8
        start_x = (width - 5 * (slot_width + gap) + gap) // 2
        self.slots = [
            pygame.Rect(
                start_x + i * (slot_width + gap), y + 10, slot_width, height - 20
            )
            for i in range(5)
        ]

    def get_clicked_slot(self, position):
        for index, slot in enumerate(self.slots):
            if slot.collidepoint(position):
                return index
        return None

    def draw(self, screen, inventory, selected_slot):
        pygame.draw.rect(screen, (22, 28, 36), self.rect)
        pygame.draw.line(screen, COLOR_GRID, self.rect.topleft, self.rect.topright)
        for index, slot in enumerate(self.slots):
            pygame.draw.rect(screen, (35, 49, 62), slot)
            border = COLOR_ACCENT if index == selected_slot else COLOR_GRID
            pygame.draw.rect(screen, border, slot, width=2)
            stack = inventory.slots[index]
            text = f"{index + 1}  Vacío"
            if stack is not None:
                module = stack.preview()
                icon = pygame.Rect(slot.x + 8, slot.y + 18, 20, 24)
                pygame.draw.rect(screen, module.color, icon)
                text = f"{index + 1} {module.name} x{stack.quantity}"
            label = self.font.render(text, True, COLOR_UI_TEXT)
            screen.blit(label, (slot.x + 34, slot.centery - label.get_height() // 2))
