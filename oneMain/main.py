import pygame
import sqlite3
import random
import requests
import io
import asyncio

#-------------------------------------------------------------------------------------------[database class]
class Database:
    def __init__(self, db_name="snake_game.db"):
       #initialize the database connection
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        #create tables for the database
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS high_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                score INTEGER NOT NULL
            )
        """)
        self.connection.commit()

    def add_score(self, player_name, score):
        #add a new score to the high_scores table
        self.cursor.execute("""
            INSERT INTO high_scores (player_name, score)
            VALUES (?, ?)
        """, (player_name, score))
        self.connection.commit()

    def get_high_scores(self, limit=10):
        #retrieve the top high scores
        self.cursor.execute("""
            SELECT player_name, score
            FROM high_scores
            ORDER BY score DESC
            LIMIT ?
        """, (limit,))
        return self.cursor.fetchall()

    def close(self):
        #close the database connection
        self.connection.close()

        import random

#-------------------------------------------------------------------------------------------[fact manager class]
class FactManager:
    def __init__(self):
        #facts about coding language; python
        self.facts = [
    ("Python is named after a comedy group, not the snake.", True),
    ("In Python, you use `print()` to display text on the screen.", True),
    ("Python uses braces `{}` to define code blocks.", False),
    ("You can write comments in Python using the `#` symbol.", True),
    ("In Python, strings are enclosed in quotes.", True),
    ("Python is a programming language invented in 1991.", True),
    ("Python is a compiled programming language.", False),
    ("Python can be used to create video games.", True),
    ("Indentation is not important in Python.", False),
    ("Python can be used to control robots.", True),
    ("You can create websites using Python.", True),
    ("The keyword `def` is used to define a function in Python.", True),
    ("In Python, `if` statements allow you to make decisions.", True),
    ("Python can only be used on Windows computers.", False),
    ("Python has built-in libraries for math and science.", True),
    ("The `for` loop is used to repeat actions in Python.", True),
    ("Python does not support variables.", False),
    ("Python is a popular language for beginners.", True),
    ("You need a special computer to run Python code.", False),
    ("Python uses `.py` as the file extension.", True),
    ("You can create animations with Python.", True),
    ("Python code runs in web browsers by default.", False),
    ("The `input()` function allows users to enter data.", True),
    ("You can import libraries in Python using the `import` keyword.", True),
    ("Python uses the `while` loop for repeated tasks until a condition is false.", True),
    ("Python can only handle small numbers.", False),
    ("Python supports both integers and decimals.", True),
    ("In Python, you can store multiple items in a `list`.", True),
    ("Python's creator is named Guido van Rossum.", True),
    ("The `else` statement is used for alternative actions in Python.", True),
    ("Python's syntax is designed to be easy to read.", True),
    ("The `int` data type is used for text in Python.", False),
    ("Python's official mascot is a python snake.", False),
    ("Python has a function to find the length of a string called `len()`.", True),
    ("Python uses the `=` symbol for comparison.", False),
    ("Python can only run on new computers.", False),
    ("Python is an open-source language.", True),
    ("You can use Python to send emails.", True),
    ("Python does not have built-in support for numbers.", False),
    ("Python can connect to databases.", True),
    ("Python files must always start with the line `#!/usr/bin/python`.", False),
    ("The `str` data type represents text in Python.", True),
    ("Python can be used to build mobile apps.", True),
    ("Python can only handle 2D graphics, not 3D.", False),
    ("You can store data in Python using `dictionaries`.", True),
    ("Python supports functions and classes.", True),
    ("Python code always ends with `.py`.", False),
    ("You can use Python to create music.", True),
    ("Python is only used by professional programmers.", False),
    ("Python can work with large amounts of data.", True),
]
        #facts about snakes
        self.facts += [
    ("Pythons are some of the largest snakes in the world.", True),
    ("Pythons are venomous snakes.", False),
    ("Pythons kill their prey by constriction.", True),
    ("Pythons can eat prey as large as a deer.", True),
    ("All pythons are found in Africa.", False),
    ("Pythons lay eggs.", True),
    ("The reticulated python is the longest snake species.", True),
    ("Pythons have fangs like venomous snakes.", False),
    ("Pythons are non-venomous snakes.", True),
    ("Pythons can live for more than 20 years in captivity.", True),
    ("Pythons use heat-sensing pits to locate prey.", True),
    ("Pythons can grow up to 30 feet in length.", True),
    ("Pythons swallow their prey whole.", True),
    ("Pythons can chew their food.", False),
    ("Pythons have scales that help them move.", True),
    ("Pythons are cold-blooded animals.", True),
    ("Pythons live in the Arctic region.", False),
    ("Pythons have flexible jaws to eat large prey.", True),
    ("Pythons do not have eyelids.", True),
    ("Pythons shed their skin regularly.", True),
    ("Pythons can breathe while swallowing prey.", True),
    ("Pythons are active hunters at night.", True),
    ("Pythons have teeth that face backward.", True),
    ("Pythons have external ears.", False),
    ("Pythons can weigh over 200 pounds.", True),
    ("Pythons can live in trees.", True),
    ("Pythons are only found in Asia.", False),
    ("Pythons have a forked tongue for smelling.", True),
    ("Pythons can go months without eating.", True),
    ("Pythons are amphibians.", False),
    ("Pythons are good swimmers.", True),
    ("Pythons are faster than most animals they hunt.", False),
    ("Pythons can live in deserts.", False),
    ("Pythons use camouflage to hide from predators.", True),
    ("Pythons can digest bones of their prey.", True),
    ("Pythons do not have tails.", False),
    ("Pythons can regrow lost body parts.", False),
    ("Pythons use their muscles to squeeze prey.", True),
    ("Pythons can climb vertical surfaces like trees.", True),
    ("Pythons can communicate with each other using sounds.", False),
    ("Pythons do not have a sense of taste.", True),
    ("Pythons can live in water and on land.", True),
    ("Pythons are solitary animals.", True),
    ("Pythons can survive in urban areas.", True),
    ("Pythons only eat meat.", True),
    ("Pythons can see in complete darkness.", True),
    ("Pythons are faster on land than in water.", False),
    ("Pythons can grow new teeth if they lose one.", True),
    ("Pythons cannot hear but sense vibrations.", True),
    ("Pythons are not found in the wild in Europe.", True),
]
    def get_random_fact(self):
        return random.choice(self.facts)

#-------------------------------------------------------------------------------------------[food class]
class Food:
    def __init__(self, screen_width, screen_height, grid_size):
            self.image_url = "https://raw.githubusercontent.com/stackandheap2/snake-game-wasm/refs/heads/main/egg.png"
            self.image = self.load_image_from_url(self.image_url, grid_size)
            self.grid_size = grid_size
            self.position = [0, 0]
            self.spawn(screen_width, screen_height, [])

    def load_image_from_url(self, url, grid_size):
        response = requests.get(url)
        if response.status_code == 200:
            image_bytes = io.BytesIO(response.content)
            image = pygame.image.load(image_bytes)
            return pygame.transform.scale(image, (grid_size, grid_size))
        else:
            raise Exception(f"Failed to load image from URL: {url}")

    def spawn(self, screen_width, screen_height, snake_body):
        while True:
            self.position = [
                random.randint(0, (screen_width - self.grid_size) // self.grid_size) * self.grid_size,
                random.randint(0, (screen_height - self.grid_size) // self.grid_size) * self.grid_size,
            ]
            if self.position not in snake_body:
                break

#-------------------------------------------------------------------------------------------[leve manager class]
class LevelManager:
    def __init__(self):
        self.level = 1
        self.base_speed = 10  #base speed for the snake
        self.speed_increment = 2  #speed increment per level

    def increase_level(self, snake):
        #increase the game level and adjust the snake's speed
        self.level += 1
        snake.speed += self.speed_increment

    def get_speed(self):
        #return the current game speed based on the level
        return self.base_speed + (self.level - 1) * self.speed_increment

#-------------------------------------------------------------------------------------------[score class]
class Score:
    def __init__(self, file_name="highscore.txt"):
        self.current_score = 0
        self.file_name = file_name
        self.high_score = self._load_high_score()

    def _load_high_score(self):
        try:
            with open(self.file_name, "r") as file:
                return int(file.read().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def _save_high_score(self):
        with open(self.file_name, "w") as file:
            file.write(str(self.high_score))

    def update(self):
        self.current_score += 1
        if self.current_score > self.high_score:
            self.high_score = self.current_score
            self._save_high_score()

    def reset(self):
        self.current_score = 0

#-------------------------------------------------------------------------------------------[snake class]
class Snake:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.head_image_url = "https://raw.githubusercontent.com/stackandheap2/snake-game-wasm/refs/heads/main/snakeHead.png"
        self.head_image = self.load_image_from_url(self.head_image_url, grid_size)  # Load image from URL
        self.body = [[100, 100], [80, 100], [60, 100]]  # Snake body
        self.direction = "RIGHT"

    def load_image_from_url(self, url, grid_size):
        response = requests.get(url)
        if response.status_code == 200:
            image_bytes = io.BytesIO(response.content)
            image = pygame.image.load(image_bytes)
            return pygame.transform.scale(image, (grid_size, grid_size))
        else:
            raise Exception(f"Failed to load image from URL: {url}")

    def move(self):
        head = self.body[0].copy()
        if self.direction == "UP":
            head[1] -= self.grid_size
        elif self.direction == "DOWN":
            head[1] += self.grid_size
        elif self.direction == "LEFT":
            head[0] -= self.grid_size
        elif self.direction == "RIGHT":
            head[0] += self.grid_size
        self.body.insert(0, head)
        self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])

    def check_collision(self):
        return self.body[0] in self.body[1:]

    def wrap_edges(self, screen_width, screen_height):
        head = self.body[0]
        if head[0] < 0:
            head[0] = screen_width - self.grid_size
        elif head[0] >= screen_width:
            head[0] = 0
        if head[1] < 0:
            head[1] = screen_height - self.grid_size
        elif head[1] >= screen_height:
            head[1] = 0

#-------------------------------------------------------------------------------------------[sound class]
class Sound:
    def __init__(self):
        self.sounds = {
            "eat": "https://github.com/stackandheap2/snake-game-wasm/raw/refs/heads/main/eat.mp3",
            "level_up": "https://github.com/stackandheap2/snake-game-wasm/raw/refs/heads/main/level_up.mp3",
            "game_over": "https://github.com/stackandheap2/snake-game-wasm/raw/refs/heads/main/game_over.mp3",
        }
        self.initialized = False

    def initialize(self):
        pygame.mixer.init()
        self.initialized = True

    def load_sound_from_url(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            sound_bytes = io.BytesIO(response.content)
            return sound_bytes
        else:
            raise Exception(f"Failed to load sound from URL: {url}")

    def play_sound(self, sound_name):
        if not self.initialized:
            return
        if sound_name in self.sounds:
            sound_url = self.sounds[sound_name]
            try:
                sound_data = self.load_sound_from_url(sound_url)
                pygame.mixer.music.load(sound_data)
                pygame.mixer.music.play()
            except Exception as e:
                print(f"Error playing sound {sound_name}: {e}")

    def play_eat(self):
        # Play the sound for eating food
        self.play_sound("eat")

    def play_level_up(self):
        # Play the sound for leveling up
        self.play_sound("level_up")

    def play_game_over(self):
        # Play the sound for game over
        self.play_sound("game_over")

#-------------------------------------------------------------------------------------------[ui class]

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.button_font = pygame.font.Font(None, 48)
        self.text_color = (255, 255, 255)  # White text color
        self.button_color = (0, 128, 255, 128)  # Semi-transparent blue
        self.button_border_color = (255, 255, 255)  # White border color

    def draw_button(self, x, y, width, height, text):
        button_rect = pygame.Rect(x, y, width, height)

        # Draw semi-transparent button
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(surface, self.button_color, (0, 0, width, height), border_radius=10)
        self.screen.blit(surface, (x, y))

        # Draw button border
        pygame.draw.rect(self.screen, self.button_border_color, button_rect, 2, border_radius=10)

        # Draw button text
        text_surface = self.button_font.render(text, True, self.text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)

        return button_rect

    def draw_text_wrapped(self, text, rect, color=(255, 255, 255)):
        words = text.split(' ')
        lines = []
        line = ""

        for word in words:
            test_line = line + word + " "
            if self.font.size(test_line)[0] <= rect.width:
                line = test_line
            else:
                lines.append(line)
                line = word + " "
        lines.append(line)

        y = rect.y
        for line in lines:
            text_surface = self.font.render(line, True, color)
            self.screen.blit(text_surface, (rect.x, y))
            y += self.font.size(line)[1]

    def draw_fact_popup(self, fact):
        popup_width, popup_height = 600, 300
        popup_x = (self.screen.get_width() - popup_width) // 2
        popup_y = (self.screen.get_height() - popup_height) // 2

        # Draw popup background
        pygame.draw.rect(self.screen, (0, 0, 0, 180), (popup_x, popup_y, popup_width, popup_height), border_radius=20)
        pygame.draw.rect(self.screen, (255, 255, 255), (popup_x, popup_y, popup_width, popup_height), 3, border_radius=20)

        # Display the fact text
        fact_rect = pygame.Rect(popup_x + 20, popup_y + 20, popup_width - 40, popup_height - 140)
        self.draw_text_wrapped(fact, fact_rect)

        # Display the prompt above the buttons
        prompt_text = "Type T for True, F for False"
        prompt_surface = self.font.render(prompt_text, True, (255, 255, 255))
        prompt_rect = prompt_surface.get_rect(center=(popup_x + popup_width // 2, popup_y + popup_height - 110))
        self.screen.blit(prompt_surface, prompt_rect)

        true_button = self.draw_button(popup_x + 50, popup_y + popup_height - 70, 200, 50, "True")
        false_button = self.draw_button(popup_x + popup_width - 250, popup_y + popup_height - 70, 200, 50, "False")


        return true_button, false_button

    

    def draw_game_over_popup(self, score):
        popup_width, popup_height = 400, 300
        popup_x = (self.screen.get_width() - popup_width) // 2
        popup_y = (self.screen.get_height() - popup_height) // 2

        pygame.draw.rect(self.screen, (0, 0, 0, 180), (popup_x, popup_y, popup_width, popup_height), border_radius=20)
        pygame.draw.rect(self.screen, (255, 255, 255), (popup_x, popup_y, popup_width, popup_height), 3, border_radius=20)

        self.draw_text("Game Over!", popup_x + 120, popup_y + 30, (255, 0, 0))
        self.draw_text(f"Your Score: {score}", popup_x + 100, popup_y + 100, self.text_color)

        play_again_button = self.draw_button(popup_x + 40, popup_y + popup_height - 100, 140, 50, "Play Again")
        quit_button = self.draw_button(popup_x + popup_width - 180, popup_y + popup_height - 100, 140, 50, "Quit")

        return play_again_button, quit_button

    def draw_text(self, text, x, y, color=(255, 255, 255)):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))


#-------------------------------------------------------------------------------------------[game class]
class Game:
    def __init__(self):
        pygame.init()
        self.grid_size = 20
        self.board_width = 600
        self.board_height = 400
        self.score_height = 70
        self.screen_width = self.board_width
        self.screen_height = self.board_height + self.score_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Snake Game")

        self.clock = pygame.time.Clock()
        self.running = True

        self.snake = Snake(self.grid_size)
        self.food = Food(self.board_width, self.board_height, self.grid_size)
        self.score = Score()
        self.sound = Sound()
        self.level_manager = LevelManager()
        self.fact_manager = FactManager()
        self.ui = UI(self.screen)
        self.lives = 3

        self.db = Database()

    def run(self):
        while self.running:
            self.handle_events()
            self.update_game_state()
            self.render()
            self.clock.tick(self.level_manager.get_speed())

    def draw_background(self):
        for row in range(0, self.board_height, self.grid_size):
            for col in range(0, self.board_width, self.grid_size):
                if (row // self.grid_size + col // self.grid_size) % 2 == 0:
                    color = (255, 255, 255)
                else:
                    color = (0, 0, 0)
                pygame.draw.rect(self.screen, color, (col, row + self.score_height, self.grid_size, self.grid_size))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.direction != "DOWN":
                    self.snake.direction = "UP"
                elif event.key == pygame.K_DOWN and self.snake.direction != "UP":
                    self.snake.direction = "DOWN"
                elif event.key == pygame.K_LEFT and self.snake.direction != "RIGHT":
                    self.snake.direction = "LEFT"
                elif event.key == pygame.K_RIGHT and self.snake.direction != "LEFT":
                    self.snake.direction = "RIGHT"

    def update_game_state(self):
        self.snake.move()

        # Check for collisions with the edges of the screen
        head_x, head_y = self.snake.body[0]
        if head_x < 0 or head_x >= self.board_width or head_y < 0 or head_y >= self.board_height:
            self.lives = 0  # Set lives to 0 to trigger game over
            self.game_over()
            return

        # Check for collisions with food
        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            self.food.spawn(self.board_width, self.board_height, self.snake.body)
            self.score.update()
            self.sound.play_eat()

            if self.score.current_score % 5 == 0:
                self.show_fact()

        # Check for collisions with itself
        if self.snake.check_collision():
            self.lives = 0  # Set lives to 0 to trigger game over
            self.game_over()

    def render(self):
        self.screen.fill((50, 50, 50))  #dark gray background
        score_text = f"Score: {self.score.current_score} | High Score: {self.score.high_score} | Lives: {self.lives}"
        self.ui.draw_text(score_text, 10, 10)

        #draw the game board
        self.draw_background()

        #draw the snake
        for i, segment in enumerate(self.snake.body):
            x, y = segment[0], segment[1] + self.score_height

            if i == 0:  #draw the head
                head_image_rotated = self.get_rotated_image(self.snake.head_image, self.snake.direction)
                self.screen.blit(head_image_rotated, (x, y))
            elif i == len(self.snake.body) - 1:  #draw the tail with rounded corners
                pygame.draw.rect(
                    self.screen,
                    (71, 105, 45),  #tail color (green)
                    (x, y, self.grid_size, self.grid_size),
                    border_radius=self.grid_size // 4  #rounded corners for the tail
                )
            else:  #draw middle body segments as plain squares
                pygame.draw.rect(
                    self.screen,
                    (71, 105, 45),  #body color (green)
                    (x, y, self.grid_size, self.grid_size)
                )

        #draw the food
        self.screen.blit(self.food.image, (self.food.position[0], self.food.position[1] + self.score_height))

        pygame.display.flip()

    def get_rotated_image(self, image, direction):
        #rotate the image based on the snake's direction
        if direction == "UP":
            return pygame.transform.rotate(image, 90)
        elif direction == "DOWN":
            return pygame.transform.rotate(image, -90)
        elif direction == "LEFT":
            return pygame.transform.rotate(image, 180)
        elif direction == "RIGHT":
            return image

    def show_fact(self):
        #display a random fact and ask 'True or False'
        fact, is_true = self.fact_manager.get_random_fact()
        self.ui.draw_fact_popup(fact)
        pygame.display.flip()

        start_time = pygame.time.get_ticks()
        answered = False

        while not answered:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:  #user pressed 'True'
                        answered = True
                        if is_true:  #correct answer
                            self.sound.play_level_up()  #play level up sound
                        else:
                            self.lives -= 1  #wrong answer, lose a life
                    elif event.key == pygame.K_f:  #user pressed 'False'
                        answered = True
                        if not is_true:  #correct answer
                            self.sound.play_level_up()  #play level up sound
                        else:
                            self.lives -= 1  #wrong answer, lose a life

        #exit if 10 seconds pass without an answer
        if pygame.time.get_ticks() - start_time > 10000:  #10 seconds
            self.lives -= 1
            return


            if pygame.time.get_ticks() - start_time > 10000:
                self.lives -= 1
                return

    def game_over(self):
        """Handle game over logic with database integration."""
        # Play game over sound
        self.sound.play_game_over()
        pygame.time.delay(2000)

        # Ask for the player's name
        player_name = ""
        asking_name = True

        # Display prompt to get player name
        while asking_name:
            self.screen.fill((50, 50, 50))  # Dark background
            self.ui.draw_text("Game Over!", self.screen_width // 2 - 100, 50, (255, 0, 0))
            self.ui.draw_text("Enter your name:", self.screen_width // 2 - 120, 150, (255, 255, 255))
            self.ui.draw_text(player_name, self.screen_width // 2 - 100, 200, (255, 255, 255))
            self.ui.draw_text("Press ENTER to submit", self.screen_width // 2 - 150, 250, (255, 255, 255))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if player_name.strip():  # Ensure the player name isn't empty
                            asking_name = False
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode

        # Save the player's score to the database
        self.db.add_score(player_name, self.score.current_score)

        # Retrieve and display high scores
        high_scores = self.db.get_high_scores()
        self.screen.fill((50, 50, 50))  # Dark background
        self.ui.draw_text("High Scores", self.screen_width // 2 - 100, 50, (255, 255, 255))

        for rank, (name, score) in enumerate(high_scores, start=1):
            score_text = f"{rank}. {name}: {score}"
            self.ui.draw_text(score_text, self.screen_width // 2 - 150, 100 + rank * 40, (255, 255, 255))

        self.ui.draw_text("Press SPACE to play again or ESC to quit", self.screen_width // 2 - 200, 400, (255, 255, 255))
        pygame.display.flip()

        # Wait for user input to restart or quit
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting_for_input = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # Play again
                        self.reset_game()
                        waiting_for_input = False
                    elif event.key == pygame.K_ESCAPE:  # Quit
                        self.running = False
                        waiting_for_input = False


    def reset_game(self):
        self.snake = Snake(self.grid_size)
        self.food = Food(self.board_width, self.board_height, self.grid_size)
        self.score.reset()
        self.lives = 3
        self.level_manager = LevelManager()

    def quit(self):
        self.db.close()
        pygame.quit()



#-------------------------------------------------------------------------------------------[main class]
async def main():
    game = Game()
    await game.run()

if __name__ == "__main__":
    asyncio.run(main())
