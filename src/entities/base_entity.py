"""Core entity module for the Regolith simulation.

This module defines the abstract base class for all physical objects
that exist on the lunar grid.
"""

import pygame

from config import TILE_SIZE


class BaseEntity:
    """Abstract base class representing an object on the grid.

    Attributes:
        grid_x (int): The X coordinate on the logical grid.
        grid_y (int): The Y coordinate on the logical grid.
        color (tuple): RGB color representing the entity (placeholder for graphics).
        name (str): Identifier for the entity.
    """

    def __init__(self, grid_x: int, grid_y: int, color: tuple, name: str = "Entity"):
        """Initializes the entity with its grid position and visual properties.

        Args:
            grid_x: The logical column index on the grid.
            grid_y: The logical row index on the grid.
            color: A tuple representing the RGB color of the entity.
            name: A string identifier for the entity.
        """
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.color = color
        self.name = name

    @property
    def rect(self):
        """The full cell occupied by this entity, in pixels."""
        return pygame.Rect(
            self.grid_x * TILE_SIZE, self.grid_y * TILE_SIZE, TILE_SIZE, TILE_SIZE
        )

    def update(self):
        """Updates the entity's logical state.

        To be overridden by subclasses. For example, a solar panel subclass
        would generate power here every frame.
        """

    def draw(self, screen: pygame.Surface):
        """Renders the entity onto the grid.

        Converts logical grid coordinates to pixel coordinates and draws
        a placeholder rectangle representing the entity.

        Args:
            screen: The Pygame surface to draw on.
        """
        pygame.draw.rect(screen, self.color, self.rect.inflate(-4, -4))
