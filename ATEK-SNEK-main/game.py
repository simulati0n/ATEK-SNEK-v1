import pygame
from snake import Snake
from food import Food
from score import Score
from sound import Sound
from levelManager import LevelManager
from factManager import FactManager
from database import Database
from ui import UI


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
        self.snake.wrap_edges(self.board_width, self.board_height)

        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            self.food.spawn(self.board_width, self.board_height, self.snake.body)
            self.score.update()
            self.sound.play_eat()

            if self.score.current_score % 5 == 0:
                self.show_fact()

        if self.snake.check_collision() or self.lives <= 0:
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
                    (0, 200, 0),  #tail color (green)
                    (x, y, self.grid_size, self.grid_size),
                    border_radius=self.grid_size // 4  #rounded corners for the tail
                )
            else:  #draw middle body segments as plain squares
                pygame.draw.rect(
                    self.screen,
                    (0, 200, 0),  #body color (green)
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


if __name__ == "__main__":
    game = Game()
    try:
        game.run()
    finally:
        game.quit()
