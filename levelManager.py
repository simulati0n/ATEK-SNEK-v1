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
