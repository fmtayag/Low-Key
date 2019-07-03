from datetime import date
from game_variables import *
from game_fonts import *
import pygame

## Classes
class Label():
    ## Instantiate the class
    def __init__(self, file_name, size, text, color, x_pos, y_pos):

        self.file_name = file_name
        self.size = size
        self.text = text
        self.color = color
        self.is_depressed = False

        self.font = load_font(self.file_name, self.size)
        self.rendered_font = self.font.render(self.text, 1, self.color)
        self.rect = self.rendered_font.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos

    ## Greys out the text when hovered on by mouse, whitens it when not
    def depress(self, mouse_pos):

        if self.rect.collidepoint(mouse_pos):

            self.color = GREY
            self.rendered_font = self.font.render(self.text, 1, self.color)
            self.is_depressed = True

        else:

            self.color = WHITE
            self.rendered_font = self.font.render(self.text, 1, self.color)
            self.is_depressed = False

    ## Special Effect: Makes the label go down!
    def go_down(self):

        self.rect.y += 5

## Objects
label_title = Label("Raleway-Regular.ttf", 64, "Keyboard Smasher", WHITE, 30, 50)
label_creator = Label("Raleway-Regular.ttf", 32, "by Etherflux", WHITE, 30, 125)
label_play = Label("Raleway-Regular.ttf", 32, "Play", WHITE, 100, 400)
label_highscore = Label("Raleway-Regular.ttf", 32, "High Scores", WHITE, 100, 450)
label_highscore_header = Label("Raleway-Regular.ttf", 64, "High Scores (Top 20)", WHITE, 30, 50)
label_highscore_paragraph = Label("Raleway-Regular.ttf", 16, "SCORE | NAME | DATE", WHITE, 30, 130)
label_exit = Label("Raleway-Regular.ttf", 32, "Exit", WHITE, 100, 500)
label_goback = Label("Raleway-Regular.ttf", 32, "Go Back", WHITE, 500, 500)