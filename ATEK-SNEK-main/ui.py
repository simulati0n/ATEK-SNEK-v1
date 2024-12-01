import pygame

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)

    def draw_text_wrapped(self, text, rect, color=(255, 255, 255)):
        #draw text inside a rectangle, wrapping it if necessary
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
        #display a fact popup with True/False instructions
        popup_width, popup_height = 600, 250  #adjust popup size for larger text
        popup_x = (self.screen.get_width() - popup_width) // 2
        popup_y = (self.screen.get_height() - popup_height) // 2

        #draw popup background
        pygame.draw.rect(self.screen, (50, 50, 50), (popup_x, popup_y, popup_width, popup_height))
        pygame.draw.rect(self.screen, (200, 200, 200), (popup_x, popup_y, popup_width, popup_height), 2)

        #display the fact text and wrap it
        fact_rect = pygame.Rect(popup_x + 20, popup_y + 20, popup_width - 40, popup_height - 80)
        self.draw_text_wrapped(fact, fact_rect)

        #draw instructions
        instructions_text = "Press T for True, F for False"
        instructions_surface = self.font.render(instructions_text, True, (255, 255, 255))
        self.screen.blit(instructions_surface, (popup_x + 150, popup_y + popup_height - 50))

    def draw_text(self, text, x, y, color=(255, 255, 255)):
        #draw text on the screen at a given position
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_game_over_popup(self, score):
        #display a popup with 'Play Again' and 'Quit' buttons
        popup_width, popup_height = 300, 200
        popup_x = (self.screen.get_width() - popup_width) // 2
        popup_y = (self.screen.get_height() - popup_height) // 2
        button_width, button_height = 100, 40
        button_padding = 20

        #draw popup background
        pygame.draw.rect(self.screen, (50, 50, 50), (popup_x, popup_y, popup_width, popup_height))
        pygame.draw.rect(self.screen, (200, 200, 200), (popup_x, popup_y, popup_width, popup_height), 2)

        #display game over text and score
        self.draw_text("Game Over!", popup_x + 80, popup_y + 20)
        self.draw_text(f"Score: {score}", popup_x + 100, popup_y + 60)

        #draw buttons
        play_again_rect = pygame.Rect(popup_x + button_padding, popup_y + 120, button_width, button_height)
        quit_rect = pygame.Rect(popup_x + popup_width - button_width - button_padding, popup_y + 120, button_width, button_height)

        pygame.draw.rect(self.screen, (0, 255, 0), play_again_rect)  #green for Play Again
        pygame.draw.rect(self.screen, (255, 0, 0), quit_rect)  #red for Quit

        self.draw_text("Play Again", play_again_rect.x + 10, play_again_rect.y + 10, (0, 0, 0))
        self.draw_text("Quit", quit_rect.x + 30, quit_rect.y + 10, (0, 0, 0))

        return play_again_rect, quit_rect
