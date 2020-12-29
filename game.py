# Import libraries
import pygame, os
from random import randrange, choice, choices

# Initialize pygame
pygame.init()

# Metadata and constants
TITLE = "Keyboard Smasher"
AUTHOR = "zyenapz"
EMAIL = "zyenapz@gmail.com"
WEBSITE = "zyenapz.github.io"
WIN_S = {"W": 800, "H": 800}
WIN_R = (WIN_S["W"], WIN_S["H"])

# Initialize the window
WINDOW = pygame.display.set_mode(WIN_R)
pygame.display.set_caption(TITLE)

# Application loop
def main():
    running = True

    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

# Run the application loop
main()

# Exit pygame
pygame.quit()
