import pygame

class Sound:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            "eat": "ATEK-SNEK-main/eat.mp3",
            "level_up": "ATEK-SNEK-main/level_up.mp3",
            "game_over": "ATEK-SNEK-main/game_over.mp3",
        }

    def play_sound(self, sound_name):
        #play a sound based on the name
        if sound_name in self.sounds:
            pygame.mixer.music.load(self.sounds[sound_name])
            pygame.mixer.music.play()

    def play_eat(self):
        #play the sound for eating food
        self.play_sound("eat")

    def play_level_up(self):
        #play the sound for leveling up
        self.play_sound("level_up")

    def play_game_over(self):
        #play the sound for game over
        self.play_sound("game_over")
