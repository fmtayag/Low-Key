### Keyboard Smasher
### By Francis Tayag (Etherflux)
### Version 3 (Rewrote it for the 3rd time)
### Visit my website: etherflux.github.io

## Import all needed libraries
import pygame

## Import local libraries
from classes import *
from constants import *

## Initialize the 'pygame' library
pygame.init()

## Creates a Game object, and runs the 'game_loop' method
game = Game()
game.game_loop()

## Closes 'pygame', and closes the program
pygame.quit()
exit()
