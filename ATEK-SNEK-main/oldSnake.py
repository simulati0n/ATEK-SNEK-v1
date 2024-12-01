import pygame

class Snake:
    def __init__(self, screen_width, screen_height, cell_size):

        self.cell_size = cell_size
        self.body = [[5, 5], [4, 5], [3, 5]]
        self.direction = "RIGHT"
        self.new_direction = "RIGHT" 
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.growing = False

    def move(self):
        head_x, head_y = self.body[0]

        if self.direction == "UP":
            head_y -= 1
        elif self.direction == "DOWN":
            head_y += 1
        elif self.direction == "LEFT":
            head_x -= 1
        elif self.direction == "RIGHT":
            head_x += 1
            
    def getBody(self):
        return self.body
