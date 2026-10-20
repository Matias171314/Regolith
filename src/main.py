"""Main entry point for the Regolith game engine.

This module initializes the Pygame environment and encapsulates the core
game loop, handling events, logical updates, and rendering.
"""

import sys

import pygame

from config import (
    BOARD_HEIGHT,
    COLOR_BG,
    FPS,
    TILE_SIZE,
    TITLE,
    TOOLBAR_HEIGHT,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from core.grid import Grid
from entities.modules import (
    Greenhouse,
    Habitat,
    OxygenGenerator,
    SolarPanel,
    WaterTank,
)
from entities.player import Player
from ui.hud import HUD
from ui.inventory import InventoryPanel
from ui.module_panel import ModulePanel
from ui.toolbar import Toolbar


class RegolithGame:
    """Core game engine class managing the application lifecycle.

    Attributes:
        screen (pygame.Surface): The main display surface for rendering.
        clock (pygame.time.Clock): Internal clock to manage framerate.
        is_running (bool): Flag indicating if the main game loop is active.
    """

    def __init__(self):
        """Initializes Pygame, the display window, and internal clock."""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)

        self.clock = pygame.time.Clock()
        self.is_running = True
        self.grid = Grid(WINDOW_WIDTH, BOARD_HEIGHT, TILE_SIZE)
        self.toolbar = Toolbar(BOARD_HEIGHT, WINDOW_WIDTH, TOOLBAR_HEIGHT)
        self.player = Player(WINDOW_WIDTH / 2, BOARD_HEIGHT / 2)
        for module_class in (
            SolarPanel,
            OxygenGenerator,
            Habitat,
            WaterTank,
            Greenhouse,
        ):
            self.player.inventory.add(module_class, 3)
        self.hud = HUD()
        self.inventory_panel = InventoryPanel(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.entities = []
        self.selected_slot = 0
        self.build_mode = False
        self.module_panel = ModulePanel(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.message = "B: construir | E: interactuar | Tab: inventario"
        self.message_timer = 0
        self.font = pygame.font.Font(None, 24)

    def notify(self, text):
        self.message = text
        self.message_timer = 3

    def nearest_module(self):
        """Choose the closest building edge within 48 pixels of the player."""
        nearest = None
        best_distance = 48
        for entity in self.entities:
            dx = max(
                entity.rect.left - self.player.rect.right,
                self.player.rect.left - entity.rect.right,
                0,
            )
            dy = max(
                entity.rect.top - self.player.rect.bottom,
                self.player.rect.top - entity.rect.bottom,
                0,
            )
            distance = pygame.Vector2(dx, dy).length()
            if distance <= best_distance:
                nearest, best_distance = entity, distance
        return nearest

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.inventory_panel.is_open:
                        self.inventory_panel.is_open = False
                        self.inventory_panel.selected_slot = None
                    elif self.module_panel.module is not None:
                        self.module_panel.module = None
                    elif self.build_mode:
                        self.build_mode = False
                    else:
                        self.is_running = False
                    continue
                if self.module_panel.module is not None:
                    if event.key == pygame.K_e:
                        self.module_panel.module = None
                    elif event.key == pygame.K_r:
                        module = self.module_panel.module
                        if self.player.inventory.add(type(module)):
                            self.entities.remove(module)
                            self.module_panel.module = None
                            self.notify("Módulo recuperado.")
                        else:
                            self.notify("Inventario lleno. Libera una casilla.")
                    continue
                if event.key == pygame.K_TAB:
                    self.inventory_panel.is_open = not self.inventory_panel.is_open
                    self.inventory_panel.selected_slot = None
                    continue
                if self.inventory_panel.is_open:
                    continue
                if pygame.K_1 <= event.key <= pygame.K_5:
                    self.selected_slot = event.key - pygame.K_1
                elif event.key == pygame.K_b:
                    self.build_mode = not self.build_mode
                elif event.key == pygame.K_e:
                    self.module_panel.module = self.nearest_module()
                    if self.module_panel.module is None:
                        self.notify("Acércate a un módulo para interactuar.")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.inventory_panel.is_open:
                    self.inventory_panel.handle_click(event.pos, self.player.inventory)
                    continue
                if self.module_panel.module is not None:
                    continue
                if self.hud.rect.collidepoint(event.pos):
                    continue
                if self.toolbar.rect.collidepoint(event.pos):
                    selected = self.toolbar.get_clicked_slot(event.pos)
                    if selected is not None:
                        self.selected_slot = selected
                    continue
                if not self.build_mode:
                    continue
                stack = self.player.inventory.slots[self.selected_slot]
                if stack is None:
                    self.notify("No hay módulos en esta casilla.")
                    continue
                grid_x, grid_y = (value // TILE_SIZE for value in event.pos)
                if self.can_build_at(grid_x, grid_y):
                    self.entities.append(stack.module_class(grid_x, grid_y))
                    self.player.inventory.consume(self.selected_slot)
                else:
                    self.notify("No puedes construir en esa celda.")

    def update(self, dt):
        """Updates the mathematical state and logic of all game entities.

        This method should not contain any drawing code. It handles physical
        calculations, resource management, and state changes.
        """
        if self.inventory_panel.is_open or self.module_panel.module is not None:
            return
        self.message_timer = max(0, self.message_timer - dt)
        self.player.update(
            dt,
            pygame.Rect(0, 0, WINDOW_WIDTH, BOARD_HEIGHT),
            [entity.rect for entity in self.entities],
        )
        for entity in self.entities:
            entity.update()

    def is_cell_occupied(self, target_x, target_y):
        """Checks if a specific grid cell is already occupied by an entity.

        Iterates through the current entities list to prevent overlapping
        structures on the same coordinates.

        Args:
            target_x: The logical X coordinate on the grid.
            target_y: The logical Y coordinate on the grid.

        Returns:
            True if the cell contains an entity, False otherwise.
        """
        for entity in self.entities:
            if entity.grid_x == target_x and entity.grid_y == target_y:
                return True
        return False

    def can_build_at(self, grid_x, grid_y):
        """Checks bounds, buildings and the player's entire rectangle."""
        cell = pygame.Rect(grid_x * TILE_SIZE, grid_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        return (
            self.grid.is_valid_cell(grid_x, grid_y)
            and not self.is_cell_occupied(grid_x, grid_y)
            and not self.player.rect.colliderect(cell)
        )

    def draw_build_preview(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (
            not self.build_mode
            or self.inventory_panel.is_open
            or self.module_panel.module is not None
            or self.toolbar.rect.collidepoint(mouse_x, mouse_y)
            or self.hud.rect.collidepoint(mouse_x, mouse_y)
        ):
            return

        grid_x = mouse_x // TILE_SIZE
        grid_y = mouse_y // TILE_SIZE

        if self.player.inventory.slots[
            self.selected_slot
        ] is None or not self.can_build_at(grid_x, grid_y):
            preview_color = (220, 70, 70)
        else:
            preview_color = (70, 220, 120)

        preview_rect = pygame.Rect(
            grid_x * TILE_SIZE,
            grid_y * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE,
        )

        pygame.draw.rect(
            self.screen,
            preview_color,
            preview_rect,
            width=3,
        )

    def render(self):
        """Draws the current state of the game to the screen.

        Applies double buffering by clearing the screen, drawing all current
        elements, and then flipping the buffer to the display.
        """
        self.screen.fill(COLOR_BG)
        self.grid.draw(self.screen)

        for entity in self.entities:
            entity.draw(self.screen)

        self.draw_build_preview()
        self.player.draw(self.screen)
        self.toolbar.draw(self.screen, self.player.inventory, self.selected_slot)
        self.hud.draw(self.screen, self.player)
        nearby = self.nearest_module()
        if nearby is not None and not self.build_mode:
            pygame.draw.rect(self.screen, (0, 212, 255), nearby.rect, width=2)
        status = "CONSTRUCCIÓN" if self.build_mode else "EXPLORACIÓN"
        hint = f"{status} | B: cambiar | Tab: inventario"
        if nearby is not None:
            hint += " | E: interactuar"
        if self.message_timer > 0:
            hint = self.message
        text = self.font.render(hint, True, (230, 237, 243))
        pygame.draw.rect(
            self.screen,
            (22, 28, 36),
            (12, BOARD_HEIGHT - 34, text.get_width() + 16, 28),
        )
        self.screen.blit(text, (20, BOARD_HEIGHT - 30))
        if self.module_panel.module is not None:
            self.module_panel.draw(self.screen)
        if self.inventory_panel.is_open:
            self.inventory_panel.draw(self.screen, self.player.inventory)
        pygame.display.flip()

    def run(self):
        """Executes the main game loop.

        Continuously handles events, updates game logic, renders graphics,
        and enforces the configured frame rate until the game is stopped.
        """
        while self.is_running:
            dt = min(self.clock.tick(FPS) / 1000, 0.05)
            self.handle_events()
            self.update(dt)
            self.render()
        self.exit()

    def exit(self):
        """Safely shuts down Pygame and terminates the program."""
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = RegolithGame()
    game.run()
