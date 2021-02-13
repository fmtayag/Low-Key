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
import string

## Initialize the 'pygame' library
pygame.init()

## Initialize the screen
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Keyboard Smasher by Etherflux")
try:

    icon = pygame.image.load("images/icon.png")
    pygame.display.set_icon(icon)

except:

    print("Icon not found!")

try:

    sound = pygame.mixer.Sound("sounds/Off Limits.wav")

except:

    print("Sound not found!")

finally:

    sound.set_volume(0.2)
    sound_length = sound.get_length()
    sound_ticks = sound_length * FPS

#print(sound_ticks)

## Game loop
while game_state == True:

    ## Clock - locks the FPS to 60. Second statement decrements the sound tick by 1
    clock.tick(FPS)

    if sound_play == 2:
        sound_ticks -= 1

    ## Track mouse position
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()

    ## Tracks pygame events
    for event in pygame.event.get():

        ## Checks if player clicks the 'X' button
        if event.type == pygame.QUIT:

            game_state = False ## Ends the 'game loop' by turning it to 'False'

        ## Checks if mouse button is down
        elif event.type == pygame.MOUSEBUTTONDOWN:

            ## if, and elifs check whether labels are 'depressed'
            if label_play.is_depressed == True and current_section == "Start":

                ## Sets the section to 'Game'
                current_section = "Game"

            elif label_highscore.is_depressed == True and current_section == "Start":

                ## Sets the section to 'Highscores'
                current_section = "Highscores"

            elif label_goback.is_depressed == True and (current_section == "Game" or 
                current_section == "Highscores" or current_section == "entername"):

                ## Sets the section to 'Start'
                current_section = "Start"
                game_start = False

            elif label_exit.is_depressed == True and current_section == "Start":

                ## Ends the 'game loop' by turning it to 'False'
                game_state = False

            elif label_music.is_depressed == True and current_section == "Start":

                ## Toggles the music
                if sound_play >= 1:

                    sound_play = 0
                    sound_ticks = 0

                elif sound_play == 0:

                    sound_play = 1
                    sound_ticks = sound_length * FPS

        ## Checks if player is pressing any alphanumeric buttons
        elif event.type == pygame.KEYDOWN and current_section == "Game" and re.match(r'^[A-Za-z0-9_]+$', chr(event.key)):

            score += 1
            game_start = True

            ## Appends the pressed character into the 'fx_char' list
            fx_char.append(Label("Raleway-Regular.ttf", 32, f"{chr(event.key)}", WHITE, random.randint(175, 600), 100))

        ## Checks key events within the 'entername' section
        elif event.type == pygame.KEYDOWN and current_section == "entername":

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
                    writer.writerow([score, "".join(player_name), today.strftime("%b-%d-%Y")])

                current_section = "Start"

    ## Controls the music
    if sound_play == 1 and sound_ticks >= 0:

        sound.play()
        sound_play = 2
        print("Triggered!")

    elif sound_play == 0:

        sound.stop()

    elif sound_ticks <= 0:

        sound_ticks = sound_length * FPS
        sound_play = 1

    ## 'Start' section
    if current_section == "Start":

        ## Runs 'depress' method
        label_play.depress(mouse_pos)
        label_highscore.depress(mouse_pos)
        label_goback.depress(mouse_pos)
        label_exit.depress(mouse_pos)
        label_music.depress(mouse_pos)

        ## Special Effect 2
        if not fx_char2 or len(fx_char2) <= 135:

            fx_char2.append(Label("Raleway-Regular.ttf", 32, random.choice(string.ascii_letters), 
                                (75, 75, 75), random.randint(0, 1400), random.randint(600, 650)))
            fx_char2.append(Label("Raleway-Regular.ttf", 32, random.choice(string.ascii_letters), 
                                (50, 50, 50), random.randint(0, 1400), random.randint(675, 1200)))

        ## Clears the 'fx_char' list so that it does not appear when the player goes back to 'Start', and then re-enters the game
        fx_char.clear()

        ## Resets the time, score, and 'game_start' variable
        time = 30 * FPS
        score = 0
        game_start = False

        ## Fills the background with 'BLACK', blits the labels, and updates the screen
        screen.fill(BLACK)

        ## Special Effect 2
        for char in fx_char2:

            screen.blit(char.rendered_font, char.rect)
            char.go_sideways()

            if char.rect.x <= -35 and char.rect.y <= -35:

                fx_char2.remove(char)

        screen.blit(label_title.rendered_font, label_title.rect)
        screen.blit(label_music.rendered_font, label_music.rect)
        screen.blit(label_creator.rendered_font, label_creator.rect)
        screen.blit(label_play.rendered_font, label_play.rect)
        screen.blit(label_highscore.rendered_font, label_highscore.rect)
        screen.blit(label_exit.rendered_font, label_exit.rect)
        pygame.display.flip()

    ## 'Game' section
    elif current_section == "Game":

        ## Runs 'depress' method
        label_goback.depress(mouse_pos)

        ## clears the fx_char2 list to reduce lag
        fx_char2.clear()

        ## Fills the background with 'BLACK'
        screen.fill(BLACK)

        ## Creates the label objects to update the score, and timer. It's a lazy solution I know LOL
        label_score = Label("Raleway-Regular.ttf", 32, f"Score: {score}", WHITE, 30, 50)
        label_timer = Label("Raleway-Regular.ttf", 32, f"Time: {round((time / FPS), 1)}s", WHITE, 620, 50)

        ## Special effect: Blits characters typed into the game
        for char in fx_char:

            screen.blit(char.rendered_font, char.rect)

            if char.rect.y >= 420:

                fx_char.remove(char)

            char.go_down()

        ## Decrements the 'time' variable by 1 if game has started, displays text if not
        if game_start == True:

            time -= 1

        elif game_start == False:

            label_instruction = Label("Raleway-Regular.ttf", 32, "Press any 'alphanumeric' keys to start!", WHITE, 120, 300)
            screen.blit(label_instruction.rendered_font, label_instruction.rect)

        ## Checks if the 'time' variable is equal or less than 0 (zero), displays the final score,
        ## then sets the 'current_section' to "Gameover"
        if time <= 0:

            current_section = "Gameover"

        ## Blits the labels, and updates the screen    
        screen.blit(label_score.rendered_font, label_score.rect)
        screen.blit(label_timer.rendered_font, label_timer.rect)
        screen.blit(label_goback.rendered_font, label_goback.rect)
        pygame.display.flip()

    ## 'Gameover' setion
    elif current_section == "Gameover":
        screen.fill(BLACK)

        label_finalscore = Label("Raleway-Regular.ttf", 32, f"You got a score of: {score}", WHITE, ((screen_width / 2) - 156), (screen_height / 2) - 50)
        label_gameover = Label("Raleway-Regular.ttf", 32, "Game Over!", WHITE, ((screen_width / 2) - 156), (screen_height / 2) - 100)

        screen.blit(label_finalscore.rendered_font, label_finalscore.rect)
        screen.blit(label_gameover.rendered_font, label_gameover.rect)
        pygame.display.flip()
        pygame.time.delay(3000)
        current_section = "entername"
        clear_tick += 1 ## Increments the clear_tick by 1

    ## 'Entername' section
    elif current_section == "entername":

        ## Runs 'depress' method
        label_goback.depress(mouse_pos)

        ## Clears the 'player_name' variable when it starts this section
        if clear_tick == 1:
            print(player_name)
            player_name.clear()
            clear_tick -= 1

        label_entername_header = Label("Raleway-Regular.ttf", 32, "Enter your name, and press 'Enter' key", WHITE, ((screen_width / 2) - 312), 200)
        label_name = Label("Raleway-Regular.ttf", 32, "".join(player_name), WHITE, ((screen_width / 2) - 128), (screen_height / 2))

        ## Fills the background with 'BLACK', blits the labels, and updates the screen
        screen.fill(BLACK)
        screen.blit(label_entername_header.rendered_font, label_entername_header.rect)
        screen.blit(label_name.rendered_font, label_name.rect)
        screen.blit(label_goback.rendered_font, label_goback.rect)
        pygame.display.flip()

    ## 'High Scores' section
    elif current_section == "Highscores":

        ## Runs 'depress' method
        label_goback.depress(mouse_pos)

        ## clears the fx_char2 list to reduce lag
        fx_char2.clear()

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

        ## Turns the 0th element in the current iteration of the highscore list into an integer
        for i in range(len(highscore_list)):
            highscore_list[i][0] = int(highscore_list[i][0])

        ## Sorts the highscore list in ascending order
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

        ## Blits the labels
        screen.blit(label_highscore_header.rendered_font, label_highscore_header.rect)
        screen.blit(label_highscore_paragraph.rendered_font, label_highscore_paragraph.rect)
        
        ## Blits all the 'Label' objects from the 'highscore_labels' list onto the screen
        if len(highscore_labels) <= 10:

            for label in highscore_labels:

                y_offset += 17
                screen.blit(label.rendered_font, (label.rect.x, label.rect.y + y_offset))

        ## Blits ONLY the first 20 high scores if there is more than 10 scores in the high score list
        elif len(highscore_labels) > 20:

            for i in range(20):

                y_offset += 17
                screen.blit(highscore_labels[i].rendered_font, (highscore_labels[i].rect.x, highscore_labels[i].rect.y + y_offset))


        ## Blits the 'go_back' label, and then updates the screen
        screen.blit(label_goback.rendered_font, label_goback.rect)
        pygame.display.flip()

## Exits the game
pygame.quit()
exit()