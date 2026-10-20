"""Player character with continuous movement in pixel coordinates."""

import math

import pygame

from core.inventory import Inventory


class Player:
    """A simple astronaut controlled with WASD or the arrow keys."""

    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.health = 100
        self.energy = 100
        self.oxygen = 100
        self.inventory = Inventory()
        self.speed = 220  # Pixels per second.
        self.rect = pygame.Rect(0, 0, 32, 32)
        self.rect.center = (round(x), round(y))

    def update(self, dt, bounds, obstacles):
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(
            int(keys[pygame.K_d] or keys[pygame.K_RIGHT])
            - int(keys[pygame.K_a] or keys[pygame.K_LEFT]),
            int(keys[pygame.K_s] or keys[pygame.K_DOWN])
            - int(keys[pygame.K_w] or keys[pygame.K_UP]),
        )
        # Keep the same speed when moving diagonally.
        if direction.length_squared() > 0:
            direction = direction.normalize()
        movement = direction * self.speed * dt
        # Small steps prevent crossing an entire obstacle in one update.
        steps = max(1, math.ceil(max(abs(movement.x), abs(movement.y)) / 16))
        for _ in range(steps):
            self.move_axis(movement.x / steps, "x", bounds, obstacles)
            self.move_axis(movement.y / steps, "y", bounds, obstacles)

    def move_axis(self, distance, axis, bounds, obstacles):
        """Moves along one axis so the player can slide along walls."""
        if distance == 0:
            return
        if axis == "x":
            self.position.x += distance
            self.rect.centerx = round(self.position.x)
        else:
            self.position.y += distance
            self.rect.centery = round(self.position.y)

        for obstacle in obstacles:
            if self.rect.colliderect(obstacle):
                if axis == "x":
                    if distance > 0:
                        self.rect.right = obstacle.left
                    else:
                        self.rect.left = obstacle.right
                else:
                    if distance > 0:
                        self.rect.bottom = obstacle.top
                    else:
                        self.rect.top = obstacle.bottom

        self.rect.clamp_ip(bounds)
        if axis == "x":
            if self.rect.centerx != round(self.position.x):
                self.position.x = self.rect.centerx
        else:
            if self.rect.centery != round(self.position.y):
                self.position.y = self.rect.centery

    def draw(self, screen):
        pygame.draw.rect(screen, (230, 237, 243), self.rect)
