### Keyboard Smasher
### by Etherflux, playtester(s): MJGamerTV (my cousin)
### Contact: franztayag@gmail.com
### Website: etherflux.github.io

## Import libraries
from datetime import date
from game_variables import *
from game_fonts import *
from game_classes import *
import csv
import os
import pygame
import random
import re

## Initialize the 'pygame' library
pygame.init()

## Initialize the screen
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Keyboard Smasher by Etherflux")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

## Game loop
while game_state == True:

    ## Clock - locks the FPS to 60
    clock.tick(FPS)

    ## Track mouse position
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()

    ## Tracks pygame events
    for event in pygame.event.get():

        ## Checks if player clicks the 'X' button
        if event.type == pygame.QUIT:

            game_state = False ## Ends the 'game loop' by turning it to 'False'

        ## Checks if mouse button is down
        if event.type == pygame.MOUSEBUTTONDOWN:

            ## if, and elifs check whether labels are 'depressed'
            if label_play.is_depressed == True and current_section == "Start":

                ## Sets the section to 'Game'
                current_section = "Game"

            elif label_highscore.is_depressed == True and current_section == "Start":

                ## Sets the section to 'Highscores'
                current_section = "Highscores"

            elif label_goback.is_depressed == True and (current_section == "Game" or 
                current_section == "Highscores" or current_section == "Enterscore"):

                ## Sets the section to 'Start'
                current_section = "Start"
                game_start = False

            elif label_exit.is_depressed == True and current_section == "Start":

                ## Ends the 'game loop' by turning it to 'False'
                game_state = False

        ## Checks if player is pressing any alphanumeric buttons
        if event.type == pygame.KEYDOWN and current_section == "Game" and re.match(r'^[A-Za-z0-9_]+$', chr(event.key)):

            score += 1
            game_start = True

            ## Appends the pressed character into the 'fx_char' list
            fx_char.append(Label("Raleway-Regular.ttf", 32, f"{chr(event.key)}", WHITE, random.randint(100, 700), 100))

        ## Checks key events within the 'Enterscore' section
        if event.type == pygame.KEYDOWN and current_section == "Enterscore":

            ## Checks if the length of 'player_name' is less than 16, and if input is alphanumeric
            if len(player_name) <= 16 and re.match(r'^[A-Za-z0-9_]+$', chr(event.key)):

                player_name.append(chr(event.key))

            ## Checks if the 'Backspace' key is pressed, and then pops the last letter
            elif event.key == pygame.K_BACKSPACE and len(player_name) > 0:

                player_name.pop()

            ## Checks if the 'RETURN' or 'ENTER' key is pressed
            elif event.key == pygame.K_RETURN:

                with open("highscores.txt", mode = "a", newline="") as csv_file:

                    writer = csv.writer(csv_file, delimiter = "|")
                    writer.writerow(score, ["".join(player_name), today.strftime("%b-%d-%Y")])

                current_section = "Start"

    # Runs 'depress' method
    label_play.depress(mouse_pos)
    label_highscore.depress(mouse_pos)
    label_goback.depress(mouse_pos)
    label_exit.depress(mouse_pos)

    ## 'Start' section
    if current_section == "Start":

        ## Clears the 'fx_char' list so that it does not appear when the player goes back to 'Start', and then re-enters the game
        fx_char.clear()

        ## Resets the time, and score
        time = 30 * FPS
        score = 0

        ## Fills the background with 'BLACK', blits the labels, and updates the screen
        screen.fill(BLACK)
        screen.blit(label_title.rendered_font, label_title.rect)
        screen.blit(label_creator.rendered_font, label_creator.rect)
        screen.blit(label_play.rendered_font, label_play.rect)
        screen.blit(label_highscore.rendered_font, label_highscore.rect)
        screen.blit(label_exit.rendered_font, label_exit.rect)
        pygame.display.flip()

    ## 'Game' section
    elif current_section == "Game":

        ## Fills the background with 'BLACK'
        screen.fill(BLACK)

        ## Creates the label objects to update the score, and timer. It's a lazy solution I know LOL
        label_score = Label("Raleway-Regular.ttf", 32, f"Score: {score}", WHITE, 30, 50)
        label_timer = Label("Raleway-Regular.ttf", 32, f"Time: {round((time / FPS), 1)}s", WHITE, 500, 50)

        ## Special effect: Blits characters typed into the game
        for char in fx_char:
            screen.blit(char.rendered_font, char.rect)

            if char.rect.y > 420:

                fx_char.remove(char)

            char.go_down()

        ## Decrements the 'time' variable by 1
        if game_start == True:

            time -= 1

        ## Checks if the 'time' variable is equal or less than 0 (zero).
        if time <= 0:
            screen.fill(BLACK)
            label_gameover = Label("Raleway-Regular.ttf", 32, "Game Over!", WHITE, ((screen_width / 2) - 128), (screen_height / 2))
            screen.blit(label_gameover.rendered_font, label_gameover.rect)
            pygame.display.flip()
            pygame.time.delay(30*FPS)
            current_section = "Enterscore"

        ## Blits the labels, and updates the screen    
        screen.blit(label_score.rendered_font, label_score.rect)
        screen.blit(label_timer.rendered_font, label_timer.rect)
        screen.blit(label_goback.rendered_font, label_goback.rect)
        pygame.display.flip()

    ## 'Enter score' section
    elif current_section == "Enterscore":

        label_enterscore_header = Label("Raleway-Regular.ttf", 32, "Enter your name, and press 'Enter' key", WHITE, ((screen_width / 2) - 256), 200)
        label_name = Label("Raleway-Regular.ttf", 32, "".join(player_name), WHITE, ((screen_width / 2) - 128), (screen_height / 2))

        ## Fills the background with 'BLACK', blits the labels, and updates the screen
        screen.fill(BLACK)
        screen.blit(label_enterscore_header.rendered_font, label_enterscore_header.rect)
        screen.blit(label_name.rendered_font, label_name.rect)
        screen.blit(label_goback.rendered_font, label_goback.rect)
        pygame.display.flip()

    ## 'High Scores' section
    elif current_section == "Highscores":

        ## Miscellaneous variables
        highscore_list = list()
        highscore_labels = list()
        y_offset = 0

        ## Fills the background with 'BLACK'
        screen.fill(BLACK)

        ## Opens the 'highscores.txt' file, and appends the contents into a list
        with open("highscores.txt") as csv_file:

            reader = csv.reader(csv_file, delimiter = "|")

            for row in reader:

                highscore_list.append(row)

        ## Turns the 0th element in the highscore list into an integer
        for i in range(len(highscore_list)):
            highscore_list[i][0] = int(highscore_list[i][0])

        ## Sorts the highscore list
        highscore_list.sort(reverse = True)

        ## Checks if 'highscores.txt' file's length is 0 (zero)
        if os.stat("highscores.txt").st_size == 0:

            label_highscore_list = Label("Raleway-Regular.ttf", 16, "No Highscores", WHITE, 50, 150)
            screen.blit(label_highscore_list.rendered_font, label_highscore_list.rect)

        else:

            ## Appends all the 'Label' objects into a 'highscore_labels' list
            for highscore in highscore_list:

                label_highscore_list = Label("Raleway-Regular.ttf", 16, f"{highscore[0]} | {highscore[1]} | {highscore[2]}", WHITE, 50, 150)
                highscore_labels.append(label_highscore_list)

        ## Blits the labels, and updates the screen
        screen.blit(label_highscore_header.rendered_font, label_highscore_header.rect)
        screen.blit(label_highscore_paragraph.rendered_font, label_highscore_paragraph.rect)
        
        ## Blits all the 'Label' objects from the 'highscore_labels' list onto the screen
        for label in highscore_labels:

            y_offset += 17
            screen.blit(label.rendered_font, (label.rect.x, label.rect.y + y_offset))

        screen.blit(label_goback.rendered_font, label_goback.rect)
        pygame.display.flip()

## Exits the game
pygame.quit()
exit()