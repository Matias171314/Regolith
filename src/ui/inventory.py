"""Inventory view with slot swapping, including the five quick-access slots."""

import pygame

from config import COLOR_ACCENT, COLOR_GRID, COLOR_UI_TEXT


class InventoryPanel:
    """Draws inventory slots and handles swapping their contents."""

    def __init__(self, width, height):
        self.is_open = False
        self.selected_slot = None
        self.rect = pygame.Rect(0, 0, 660, 380)
        self.rect.center = (width // 2, height // 2)
        self.font = pygame.font.Font(None, 20)
        self.overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 150))
        self.slots = [
            pygame.Rect(
                self.rect.x + 24 + (i % 5) * 124,
                self.rect.y + 76 + (i // 5) * 80,
                116,
                70,
            )
            for i in range(15)
        ]

    def handle_click(self, position, inventory):
        for index, slot in enumerate(self.slots):
            if slot.collidepoint(position):
                if self.selected_slot is None:
                    self.selected_slot = index
                else:
                    source = self.selected_slot
                    inventory.slots[source], inventory.slots[index] = (
                        inventory.slots[index],
                        inventory.slots[source],
                    )
                    self.selected_slot = None
                return
        self.selected_slot = None

    def draw(self, screen, inventory):
        screen.blit(self.overlay, (0, 0))
        pygame.draw.rect(screen, (22, 28, 36), self.rect)
        pygame.draw.rect(screen, COLOR_ACCENT, self.rect, width=2)
        for text, y in [
            ("Inventario · primera fila: acceso rápido 1–5", 20),
            ("Haz clic en dos casillas para intercambiarlas.", 44),
            ("Tab o Esc: cerrar", self.rect.height - 30),
        ]:
            screen.blit(
                self.font.render(text, True, COLOR_UI_TEXT),
                (self.rect.x + 24, self.rect.y + y),
            )
        for index, slot in enumerate(self.slots):
            pygame.draw.rect(screen, (35, 49, 62), slot)
            color = COLOR_ACCENT if index == self.selected_slot else COLOR_GRID
            pygame.draw.rect(screen, color, slot, width=2)
            stack = inventory.slots[index]
            if stack is not None:
                module = stack.preview()
                pygame.draw.rect(screen, module.color, (slot.x + 8, slot.y + 8, 18, 18))
                quantity = self.font.render(f"x{stack.quantity}", True, COLOR_UI_TEXT)
                screen.blit(quantity, (slot.x + 34, slot.y + 8))
                words = module.name.split()
                for line, word in enumerate(words):
                    label = self.font.render(word, True, COLOR_UI_TEXT)
                    screen.blit(label, (slot.x + 8, slot.y + 30 + line * 17))
