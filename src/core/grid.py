"""Grid system for logical placement and rendering.

This module defines the Grid class, which handles the mapping between
logical coordinates and screen pixels, and renders the visual grid.
"""

import pygame

from config import COLOR_GRID


class Grid:
    """Manages the 2D spatial grid for the simulation.

    Attributes:
        width (int): Total width of the screen in pixels.
        height (int): Total height of the screen in pixels.
        tile_size (int): Size of each square tile in pixels.
    """

    def __init__(self, width: int, height: int, tile_size: int):
        """Initializes the grid dimensions.

        Args:
            width: The width of the screen in pixels.
            height: The height of the screen in pixels.
            tile_size: The pixel size of a single grid cell.
        """
        self.width = width
        self.height = height
        self.tile_size = tile_size

    def is_valid_cell(self, grid_x: int, grid_y: int) -> bool:
        """Returns whether the cell fits entirely inside the grid."""
        columns = self.width // self.tile_size
        rows = self.height // self.tile_size

        return 0 <= grid_x < columns and 0 <= grid_y < rows

    def draw(self, screen: pygame.Surface):
        """Draws the grid lines onto the provided surface.

        Args:
            screen: The Pygame surface where the grid will be rendered.
        """
        # Draw vertical lines
        for x in range(0, self.width, self.tile_size):
            pygame.draw.line(screen, COLOR_GRID, (x, 0), (x, self.height))

        # Draw horizontal lines
        for y in range(0, self.height, self.tile_size):
            pygame.draw.line(screen, COLOR_GRID, (0, y), (self.width, y))
