import tkinter as tk
import random

GAME_WIDTH = 500
GAME_HEIGHT = 500
SNAKE_SIZE = 20
SPEED = 100
BACKGROUND_COLOR = "#000000"
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(self.root, width=GAME_WIDTH, height=GAME_HEIGHT, bg=BACKGROUND_COLOR)
        self.canvas.pack()

        self.score = 0
        self.snake = [(100, 100), (80, 100), (60, 100)] 
        self.food_position = self.create_food()
        self.direction = 'Right'
        self.running = True

        self.root.bind("<Up>", self.turn_up)
        self.root.bind("<Down>", self.turn_down)
        self.root.bind("<Left>", self.turn_left)
        self.root.bind("<Right>", self.turn_right)

        self.update_snake()
        self.move_snake()
    
    def create_food(self):
        x = random.randint(0, (GAME_WIDTH // SNAKE_SIZE) - 1) * SNAKE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SNAKE_SIZE) - 1) * SNAKE_SIZE
        self.canvas.create_oval(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill=FOOD_COLOR, tag="food")
        return x, y

    def turn_up(self, event):
        if self.direction != 'Down':
            self.direction = 'Up'

    def turn_down(self, event):
        if self.direction != 'Up':
            self.direction = 'Down'

    def turn_left(self, event):
        if self.direction != 'Right':
            self.direction = 'Left'

    def turn_right(self, event):
        if self.direction != 'Left':
            self.direction = 'Right'

    def update_snake(self):
        self.canvas.delete("snake")
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + SNAKE_SIZE, segment[1] + SNAKE_SIZE, fill=SNAKE_COLOR, tag="snake")

    def move_snake(self):
        if not self.running:
            return

        x, y = self.snake[0]
        if self.direction == 'Up':
            y -= SNAKE_SIZE
        elif self.direction == 'Down':
            y += SNAKE_SIZE
        elif self.direction == 'Left':
            x -= SNAKE_SIZE
        elif self.direction == 'Right':
            x += SNAKE_SIZE

        new_head = (x, y)

        if (x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT or new_head in self.snake):
            self.game_over()
            return

        self.snake = [new_head] + self.snake[:-1]

        if new_head == self.food_position:
            self.snake.append(self.snake[-1])
            self.score += 1
            self.canvas.delete("food")
            self.food_position = self.create_food()

        self.update_snake()
        self.root.after(SPEED, self.move_snake)

    def game_over(self):
        self.running = False
        self.canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2, fill="white", font="Arial 20", text=f"Game Over! Score: {self.score}")

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
