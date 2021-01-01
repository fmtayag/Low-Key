# Import libraries
# Pygame version: Pygame 2.0.0 (SDL 2.0.12, python 3.7.9)
import pygame, os
from pygame.locals import *
from random import randrange, choice, choices

# Initialize pygame
pygame.init()

# Metadata
TITLE = "Keyboard Smasher"
AUTHOR = "zyenapz"
EMAIL = "zyenapz@gmail.com"
WEBSITE = "zyenapz.github.io"

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
        window.fill('blue')

class SceneManager(object):
    def __init__(self):
        self.go_to(GameScene())

    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self

# Application loop
def main():

    WIN_S = {"400x400": (400, 400),
             "500x500": (500, 500),
             "600x600": (600, 600),
             "700x700": (700, 700)}
    W_RATIO = 5
    H_RATIO = 5
    INIT_SIZE = WIN_S["700x700"]
    
    # Initialize the window
    window = pygame.display.set_mode(INIT_SIZE, HWSURFACE|DOUBLEBUF|OPENGL)
    pygame.display.set_caption(TITLE)

    # Images
    tree_img = pygame.image.load("tree.png").convert_alpha()
    tree_img = pygame.transform.scale(tree_img, (INIT_SIZE[0] // W_RATIO, INIT_SIZE[1] // H_RATIO))
    tree_orig = tree_img.copy()

    # Loop
    running = True
    #manager = SceneManager()

    while running:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    size = "400x400"
                    window = pygame.display.set_mode(WIN_S[size], HWSURFACE|DOUBLEBUF)
                    tree_img = pygame.transform.scale(tree_orig, (WIN_S[size][0] // W_RATIO, WIN_S[size][1] // H_RATIO))
                elif event.key == pygame.K_w:
                    size = "500x500"
                    window = pygame.display.set_mode(WIN_S[size], HWSURFACE|DOUBLEBUF)
                    tree_img = pygame.transform.scale(tree_orig, (WIN_S[size][0] // W_RATIO, WIN_S[size][1] // H_RATIO))
                elif event.key == pygame.K_e:
                    window = pygame.display.set_mode((0,0), HWSURFACE|DOUBLEBUF|FULLSCREEN)
                    tree_img = pygame.transform.scale(tree_orig, (window.get_width() // W_RATIO, window.get_height() // H_RATIO))

        window.blit(tree_img, (10,10))
        #manager.scene.process_input()
        #manager.scene.update()
        #manager.scene.draw(window)
        pygame.display.flip()
        
# Run the application loop
main()

# Exit pygame
pygame.quit()
