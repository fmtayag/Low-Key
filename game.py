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

class Scene():
    def __init__(self):
        pass
    
    def process_input(self):
        raise NotImplementedError
    
    def update(self):
        raise NotImplementedError

    def draw(self, window):
        raise NotImplementedError

class GameScene(Scene):
    def __init__(self):
        pass
    
    def process_input(self):

        # Get pressed characters
        keys_pressed = list()
        scan = pygame.key.get_pressed()
        if 1 in list(scan):
            for i in range(len(list(scan))):
                if scan[i]:
                    keys_pressed.append(i)

            characters = [chr(i) for i in keys_pressed]
            #print(characters)
    
    def update(self):
        pass

    def draw(self, window):
        pygame.draw.circle(window, 'red', (50,50), 20)

class SceneManager(object):
    def __init__(self):
        self.go_to(GameScene())

    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self

# Application loop
def main():

    # Initialize the window
    WINDOW = pygame.display.set_mode(WIN_R)
    pygame.display.set_caption(TITLE)
    running = True

    manager = SceneManager()

    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        manager.scene.process_input()
        manager.scene.update()
        manager.scene.draw(WINDOW)

        pygame.display.flip()
        

# Run the application loop
main()

# Exit pygame
pygame.quit()
