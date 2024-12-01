import pygame

class Snake:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.body = [[100, 100], [80, 100], [60, 100]]  #snake body
        self.direction = "RIGHT"
        self.head_image = pygame.image.load("ATEK-SNEK-main/snakeHead.png")  #head image
        self.head_image = pygame.transform.scale(self.head_image, (grid_size, grid_size))  #scale to grid size

    def move(self):
        """Move the snake by adding a new head position and removing the last segment."""
        head = self.body[0].copy()

        if self.direction == "UP":
            head[1] -= self.grid_size
        elif self.direction == "DOWN":
            head[1] += self.grid_size
        elif self.direction == "LEFT":
            head[0] -= self.grid_size
        elif self.direction == "RIGHT":
            head[0] += self.grid_size

        self.body.insert(0, head)  #add the new head
        self.body.pop()  #remove the tail unless growing

    def grow(self):
        """Grow the snake by duplicating the last segment."""
        self.body.append(self.body[-1])  #add a new segment at the tail

    def check_collision(self):
        """Check if the snake has collided with itself."""
        head = self.body[0]
        return head in self.body[1:]

    def wrap_edges(self, screen_width, screen_height):
        """Allow the snake to wrap around the edges of the game board."""
        head = self.body[0]
        if head[0] < 0:
            head[0] = screen_width - self.grid_size
        elif head[0] >= screen_width:
            head[0] = 0
        if head[1] < 0:
            head[1] = screen_height - self.grid_size
        elif head[1] >= screen_height:
            head[1] = 0
