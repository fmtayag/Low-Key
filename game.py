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

# Directories
GAME_DIR = os.path.dirname(__file__)

# Font
GAME_FONT = os.path.join(GAME_DIR, "prstartk.ttf")

# Load image function
def load_img(file, directory, scale, convert_alpha=False):
    try:
        path = os.path.join(directory, file)
        if not convert_alpha:
            img = pygame.image.load(path).convert_alpha()
        else:
            img = pygame.image.load(path).convert()
            transColor = img.get_at((0,0))
            img.set_colorkey(transColor)
        img_w = img.get_width()
        img_h = img.get_height()
        img = pygame.transform.scale(img, (img_w*scale, img_h*scale))
        return img
    except Exception as e:
        print(e)
        exit()

# Draw text function
def draw_text(surf, text, size, font, x, y, color, align="normal"):
    font = pygame.font.Font(font, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if align == "centered":
        text_rect.centerx = x
        text_rect.y = y
    elif align == "normal":
        text_rect.x = x
        text_rect.y = y
    surf.blit(text_surface, (text_rect.x, text_rect.y))

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
        # Images
        key_img = load_img("key.png", GAME_DIR, 3)

        # Sprites
        key_spr = Key(key_img, "A")
        
        # Sprite groups
        self.sprites = pygame.sprite.Group()
        self.sprites.add(key_spr)
    
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
        self.sprites.update()

    def draw(self, window):
        self.sprites.draw(window)

class SceneManager(object):
    def __init__(self):
        self.go_to(GameScene())

    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self

class Key(pygame.sprite.Sprite):
    def __init__(self, image, key):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10
        self.key = key

    def update(self):
        draw_text(self.image, self.key, 16, GAME_FONT, self.rect.centerx-8, 12, 'black', align="centered")

# Application loop
def main():

    WIN_S = {"128x128": (128, 128),
             "256x256": (256, 256),
             "512x512": (512, 512),
             "1024x1024": (1024,1024)}
    W_RATIO = 5
    H_RATIO = 5
    
    # Initialize the window
    window = pygame.display.set_mode(WIN_S["512x512"], HWSURFACE|DOUBLEBUF)
    pygame.display.set_caption(TITLE)

    # Loop
    running = True
    manager = SceneManager()

    while running:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        manager.scene.process_input()
        manager.scene.update()
        manager.scene.draw(window)
        pygame.display.flip()
        
# Run the application loop
main()

# Exit pygame
pygame.quit()
