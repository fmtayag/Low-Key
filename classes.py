## Import all needed libraries
import csv
import os
import pygame
import random
import re
from datetime import date

## Import local libraries
from constants import *

## The 'Game' class
class Game:

    ## 'Constructor' method
    def __init__(self):

        ## Screen declarations
        self.screen_width = 800
        self.screen_height = 600
        self.screen_size =  (self.screen_width, self.screen_height)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Keyboard Smasher v3 by Etherflux")
        pygame.display.set_icon(pygame.image.load(os.path.join("Resources", "Images", "Icon.png")))

        ## Clock, and FPS constant
        self.clock = pygame.time.Clock()
        self.FPS = 60

        ## 'game_state', accepts four values: "start", "game", "gameover", and "highscores"
        self.game_state = "start"

        ## 'running' loop
        self.running = True

        ## Score, and date
        self.score = int()
        self.timer = float()
 
    ## 'Game loop' method, this is where most of the game actually happens
    def game_loop(self):

        while self.running:

            if self.game_state == "start":

                self.start_screen()

            if self.game_state == "game":

                self.game_screen()

            if self.game_state == "gameover":

                self.gameover_screen()

            if self.game_state == "highscores":

                self.highscores_screen()

            if self.game_state == "quit":

                self.running = False

    ## 'Start menu' screen of the game
    def start_screen(self):

        ## Sets the score, and timer
        self.score = 0
        self.timer = 30 * self.FPS

        ## Labels
        label_title = Label("Keyboard Smasher (v3.0)", "NONSTOP", 32, WHITE, [100, 100])
        label_author = Label("by Etherflux", "NONSTOP", 24, WHITE, [100, 150])
        label_play = Label("Play", "NONSTOP", 36, WHITE, [100, 250])
        label_highscores = Label("High Scores", "NONSTOP", 36, WHITE, [100, 300])
        label_quit = Label("Quit", "NONSTOP", 36, WHITE, [100, 350])

        ## 'loop' boolean
        loop = True

        while loop == True:

            ## Ticks the clock, locks the FPS to <= 30
            self.clock.tick(self.FPS)

            ## Retrieves, and then stores the mouse's position
            mouse_position = pygame.mouse.get_pos()

            ## Loops through the 'event' sequence
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
 
                    loop = False
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    if label_author.rendered_rect.collidepoint(mouse_position):

                        label_author.text = "by Francis Tayag"

                    elif label_play.rendered_rect.collidepoint(mouse_position):

                        self.game_state = "game"
                        loop = False

                    elif label_highscores.rendered_rect.collidepoint(mouse_position):

                        self.game_state = "highscores"
                        loop = False

                    elif label_quit.rendered_rect.collidepoint(mouse_position):

                        loop = False
                        self.running = False

            ## Runs the 'depress' method
            label_author.depress(mouse_position)
            label_play.depress(mouse_position)
            label_highscores.depress(mouse_position)
            label_quit.depress(mouse_position)

            ## Fills the background with black
            self.screen.fill(BLACK)

            ## Blits surfaces onto the screen surface
            self.screen.blit(label_title.render(), label_title.position)
            self.screen.blit(label_author.render(), label_author.position)
            self.screen.blit(label_play.render(), label_play.position)
            self.screen.blit(label_highscores.render(), label_highscores.position)
            self.screen.blit(label_quit.render(), label_quit.position)

            ## Updates, or "flips" the screen
            pygame.display.flip()

    ## 'Game' screen of the game, this is where the game actually takes place       
    def game_screen(self):

        ## Effect list, stores the labels for the character effect
        effect_char_list = list()

        ## 'timer_start' boolean
        timer_start = False

        ## Labels
        label_score = Label(f"Score: {self.score}", "NONSTOP", 32, WHITE, [10, 100])
        label_timer = Label(f"Timer: {round(self.timer / self.FPS, 1)}", "NONSTOP", 32, WHITE, [550, 100])
        label_goback = Label("Go Back", "NONSTOP", 24, WHITE, [600, 500])

        ## 'loop' boolean
        loop = True

        while loop == True:

            ## Ticks the clock, locks the FPS to <= 30
            self.clock.tick(self.FPS)

            ## Decrements the timer (in ticks) as long as it is above 0 seconds
            if self.timer >= 0 and timer_start == True:

                self.timer -= 1

            if self.timer <= 0:

                self.game_state = "gameover"
                loop = False

            ## Retrieves, and then stores the mouse's position
            mouse_position = pygame.mouse.get_pos()

            ## Loops through the 'event' sequence
            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    loop = False
                    self.running = False

                elif event.type == pygame.KEYDOWN:

                    if re.match(r'^[A-Za-z0-9_]+$', chr(event.key)):

                        self.score += 1
                        timer_start = True

                        label_char = Label(f"{chr(event.key)}", "NONSTOP", 50, GREEN, 
                            [random.randint(100, 700), 125])
                        effect_char_list.append(label_char)

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    if label_goback.rendered_rect.collidepoint(mouse_position):

                        self.game_state = "start"
                        loop = False

            ## Updates score, and timer
            label_score.text = f"Score: {self.score}"
            label_timer.text = f"Timer: {round(self.timer / self.FPS, 1)}"

            ## Runs the 'depress' method
            label_goback.depress(mouse_position)

            ## Fills the background with black
            self.screen.fill(BLACK)

            ## Label rain effect
            self.label_rain(effect_char_list)

            ## Blits surfaces onto the screen surface
            self.screen.blit(label_score.render(), label_score.position)
            self.screen.blit(label_timer.render(), label_timer.position)
            self.screen.blit(label_goback.render(), label_goback.position)

            ## Updates, or "flips" the screen
            pygame.display.flip()

    ## 'Game over' screen of the game
    def gameover_screen(self):

        ## Declarations for storing player name
        name_list = list()

        ## Labels
        label_gameover = Label("Game over!", "NONSTOP", 32, WHITE, [50, 100])
        label_totalscore = Label(f"You scored {self.score} under 30 seconds!", "NONSTOP", 32, WHITE, [50, 150])
        label_typename = Label(f"Type your name: {str().join(name_list)}", "NONSTOP", 32, WHITE, [50, 250])

        ## 'loop' boolean
        loop = True

        while loop == True:

            ## Ticks the clock, locks the FPS to <= 30
            self.clock.tick(self.FPS)

            ## Retrieves, and then stores the mouse's position
            mouse_position = pygame.mouse.get_pos()

            ## Loops through the 'event' sequence
            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    loop = False
                    self.running = False

                elif event.type == pygame.KEYDOWN:

                    if re.match(r'^[A-Za-z0-9_]+$', chr(event.key)) and len(name_list) <= 16:

                        name_list.append(chr(event.key))

                    elif event.key == pygame.K_BACKSPACE and len(name_list) > 0:

                        name_list.pop()

                    elif event.key == pygame.K_RETURN:

                        with open(os.path.join("Resources", "High Scores", "highscores.txt"),
                            mode = "a", newline = "") as csv_file:

                            writer = csv.writer(csv_file, delimiter = "|")
                            writer.writerow([self.score, str().join(name_list), date.today().strftime("%b-%d-%Y")])

                        self.game_state = "start"
                        loop = False


            ## Updates the 'typename' label's text
            label_typename.text = f"Type your name: {str().join(name_list)}"

            ## Fills the background with black
            self.screen.fill(BLACK)

            ## Blits surfaces onto the screen surface
            self.screen.blit(label_gameover.render(), label_gameover.position)
            self.screen.blit(label_totalscore.render(), label_totalscore.position)
            self.screen.blit(label_typename.render(), label_typename.position)

            ## Updates, or "flips" the screen
            pygame.display.flip()

    ## 'High Scores' screen of the game
    def highscores_screen(self):

        ## High scores list
        highscore_list = list()
        highscore_labels_list = list()
        y_offset = 0

        ## Labels
        label_header = Label("High Scores (Top 10)", "NONSTOP", 32, WHITE, [50, 100])
        label_nohighscores = Label("No high scores set, yet! Play the game!", "NONSTOP", 24, WHITE, [50, 150])
        label_goback = Label("Go Back", "NONSTOP", 24, WHITE, [600, 500])

        ## 'loop' boolean
        loop = True

        ## 'appended' boolean
        appended = False

        ## Special effect
        list_specialeffect = list()

        ## Loops through the 'event' sequence
        while loop == True:

            ## Ticks the clock, locks the FPS to <= 30
            self.clock.tick(self.FPS)

            ## Retrieves, and then stores the mouse's position
            mouse_position = pygame.mouse.get_pos()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    loop = False
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    if label_goback.rendered_rect.collidepoint(mouse_position):

                        self.game_state = "start"
                        loop = False

            ## Opens the 'highscores.txt' file, and appends the contents into a list
            with open(os.path.join("Resources", "High Scores", "highscores.txt")) as csv_file:

                reader = csv.reader(csv_file, delimiter = "|")

                for row in reader:

                    highscore_list.append(row)

            ## Turns the 0th element in the current iteration of the highscore list into an integer
            for i in range(len(highscore_list)):

                highscore_list[i][0] = int(highscore_list[i][0])

            ## Sorts the highscore list in ascending order
            highscore_list.sort(reverse = True)

            ## Runs the 'depress' method
            label_goback.depress(mouse_position)

            ## Fills the background with black
            self.screen.fill(BLACK)

            ## Checks if 'highscores.txt' file's length is 0 (zero)
            if os.stat(os.path.join("Resources", "High Scores", "highscores.txt")).st_size == 0:

                screen.blit(label_nohighscores.render(), label_nohighscores.position)

            if appended == False:

                for highscore in highscore_list:

                    label_highscore = Label(f"{highscore[0]} | {highscore[1]} | {highscore[2]}", 
                        "NONSTOP", 24, WHITE, [50, 150 + y_offset])
                    highscore_labels_list.append(label_highscore)

                    y_offset += 30

                appended = True

            ## Checks if the length of the high scores list is less than 10, then blits the high score list
            if len(highscore_labels_list) <= 10:

                for label in highscore_labels_list:

                    self.screen.blit(label.render(), label.position)

            ## Blits only the top 10 high scores if list is above 20
            elif len(highscore_labels_list) > 10:

                for i in range(10):

                    self.screen.blit(highscore_labels_list[i].render(), highscore_labels_list[i].position)

            ## Blits surfaces onto the screen surface
            self.screen.blit(label_header.render(), label_header.position)
            self.screen.blit(label_goback.render(), label_goback.position)

            ## Updates, or "flips" the screen
            pygame.display.flip()

    ## 'Label rain' effect
    def label_rain(self, char_list):

        ## Loops through list
        for label in char_list:

            ## Blits the label, and runs the label's 'go_down' method
            self.screen.blit(label.render(), label.position)
            label.go_down()

            ## Deletes labels that have reached a boundary to reduce lag
            if label.position[1] >= 375:

                char_list.remove(label)

## The 'Label' class, for texts
class Label:

    ## 'Constructor' method
    def __init__(self, text, filename, size, color, position):

        ## Initializes the instance variables
        self.text = text
        self.filename = filename
        self.size = size
        self.color = color
        self.position = position ## Is a list [x_position, y_position]

        ## Sets the path
        self.path = os.path.join("Resources", "Fonts", self.filename + ".ttf")

        ## Create 'Font' object
        self.font = pygame.font.Font(self.path, self.size)

        ## Renders the label
        self.rendered = self.font.render(self.text, True, self.color)
        self.rendered_rect = self.rendered.get_rect()
        self.rendered_rect.x = self.position[0]
        self.rendered_rect.y = self.position[1]

    ## Render method
    def render(self):

        self.rendered = self.font.render(self.text, True, self.color)
        return self.rendered

    ## Special effect, 'depresses' or grays out the label
    def depress(self, mouse_position):

        ## Checks if the object's rect attribute collides with the mouse position
        if self.rendered_rect.collidepoint(mouse_position):

            self.color = GRAY
            self.render()

        else:

            self.color = WHITE
            self.render()

    ## Special effect, makes the label go down
    def go_down(self):

        self.position[1] += 5