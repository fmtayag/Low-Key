from datetime import date
import pygame

## Screen constants
screen_width = 800
screen_height = 600
screen_size = (screen_width, screen_height)

## Color constants
BLACK = (40, 40, 40)
WHITE = (255, 255, 255)
GREY = (150, 150, 150)

## Other constants
FPS = 30

## Game variables
game_start = False ## Goes 'True' if a key is pressed, signalling the game start.
game_state = True ## Checks if the game is running

## Lists
fx_char = list()
player_name = list()
score = 0
time = 0

## Clock, current_section initialize, and today's date
clock = pygame.time.Clock()
current_section = "Start" ## Accepts five (5) values: "Start", "Game", "Entername", "Gameover", and "Highscore". Glorified 'goto' really LOL.
today = date.today()

## Clear tick, a variable that is part of an 'if' statement in the 'Enterscore' section. More explanation there.
clear_tick = 0
