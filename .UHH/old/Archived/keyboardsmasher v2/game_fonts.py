import os
import pygame

pygame.font.init()

## Functions
def load_font(file_name, size):

    path = os.path.join("fonts", file_name)
    return pygame.font.Font(path, size)