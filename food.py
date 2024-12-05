import random
import pygame

class Food:
    def __init__(self, screen_width, screen_height, grid_size):
        self.image = pygame.image.load("egg.png")
        self.image = pygame.transform.scale(self.image, (grid_size, grid_size))
        self.grid_size = grid_size
        self.position = [0, 0]
        self.spawn(screen_width, screen_height, [])

    def spawn(self, screen_width, screen_height, snake_body):
        while True:
            self.position = [
                random.randint(0, (screen_width - self.grid_size) // self.grid_size) * self.grid_size,
                random.randint(0, (screen_height - self.grid_size) // self.grid_size) * self.grid_size,
            ]
            if self.position not in snake_body:
                break
