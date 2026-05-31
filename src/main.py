"""Main entry point for the Regolith game engine.

This module initializes the Pygame environment and encapsulates the core
game loop, handling events, logical updates, and rendering.
"""
import pygame
import sys
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, TITLE, COLOR_BG, TILE_SIZE, COLOR_ACCENT
from core.grid import Grid
from entities.modules import SolarPanel, OxygenGenerator

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
        self.grid = Grid(WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE)
        self.entities = []
        self.current_build_mode = "SolarPanel"

    def handle_events(self):
        """Processes input events from the user and the system.

        Listens for window closing events and keyboard inputs (e.g., ESC
        to quit the game).
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False
                if event.key == pygame.K_1:
                    self.current_build_mode = "SolarPanel"
                if event.key == pygame.K_2:
                    self.current_build_mode = "OxygenGenerator"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x = mouse_x // TILE_SIZE
                grid_y = mouse_y // TILE_SIZE
                if not self.is_cell_occupied(grid_x, grid_y):
                    if self.current_build_mode == "SolarPanel":
                        self.entities.append(SolarPanel(grid_x, grid_y))
                    if self.current_build_mode == "OxygenGenerator":
                        self.entities.append(OxygenGenerator(grid_x, grid_y))
                else:
                    print("Construction failed: Cell is already occupied.")

    def update(self):
        """Updates the mathematical state and logic of all game entities.
        
        This method should not contain any drawing code. It handles physical
        calculations, resource management, and state changes.
        """
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

    def render(self):
        """Draws the current state of the game to the screen.

        Applies double buffering by clearing the screen, drawing all current
        elements, and then flipping the buffer to the display.
        """
        self.screen.fill(COLOR_BG)
        self.grid.draw(self.screen)
        for entity in self.entities:
            entity.draw(self.screen)
        pygame.display.flip()

    def run(self):
        """Executes the main game loop.

        Continuously handles events, updates game logic, renders graphics,
        and enforces the configured frame rate until the game is stopped.
        """
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        self.exit()

    def exit(self):
        """Safely shuts down Pygame and terminates the program."""
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = RegolithGame()
    game.run()
