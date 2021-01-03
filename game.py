# Import libraries
# Pygame version: Pygame 2.0.0 (SDL 2.0.12, python 3.7.9)
import pygame, os
from pygame.locals import *
from random import randrange, choice, choices
from itertools import repeat
from data.scripts.sprites import Key, Particle, Shockwave, PulsatingText
from data.scripts.constants import *

# Initialize pygame
pygame.init()

# Metadata
TITLE = "Keyboard Smasher"
AUTHOR = "zyenapz"
EMAIL = "zyenapz@gmail.com"
WEBSITE = "zyenapz.github.io"

# Directories
GAME_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(GAME_DIR, "data")
IMG_DIR = os.path.join(DATA_DIR, "img")
FONT_DIR = os.path.join(DATA_DIR, "fonts")
GAME_FONT = os.path.join(FONT_DIR, "prstartk.ttf")

def load_keys(letters, sprites, key_sprites, K_SIZE, color, font):
    x = 0 # x offset
    y = 0 # y offset
    o = 0 # row offset
    KB_XPOS = 50 # x pos of the whole keyboard
    KB_YPOS = 350 # y pos of the whole keyboard

    for row in letters:
        x = 0
        for letter in row:
            x_pos = K_SIZE*x + (x*K_SIZE/8) + (16*o)
            y_pos = 38*y
            key = Key(letter, x_pos + KB_XPOS, y_pos + KB_YPOS, K_SIZE, color, font)
            sprites.add(key)
            key_sprites.add(key)
            x += 1
        y += 1
        o += 1

def spawn_particles(sprites, particles, x, y, color, amount):
    for _ in range(amount):
        p = Particle(x, y, color)
        particles.add(p)
        sprites.add(p)

def shake(intensity, n):
    # Credits to sloth from StackOverflow, thanks buddy!
    shake = -1
    for _ in range(n):
        for x in range(0, intensity, 5):
            yield (x*shake, 0)
        for x in range(intensity, 0, 5):
            yield (x*shake, 0)
        shake *= -1
    while True:
        yield (0, 0)

class Scene():
    def __init__(self):
        pass
    
    def handle_events(self):
        raise NotImplementedError
    
    def update(self):
        raise NotImplementedError

    def draw(self, window):
        raise NotImplementedError

class SceneManager(object):
    def __init__(self, InitScene):
        self.go_to(InitScene)

    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self

class GameScene(Scene):
    def __init__(self):
        # Game variables
        self.score = 0

        # Sprite groups
        self.sprites = pygame.sprite.Group()
        self.key_sprites = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()

        # Color of the objects
        self.color = "ORANGE"

        # Keys
        self.K_SIZE = 32 # key size
        self.letters = ["1234567890-=",
                        "QWERTYUIOP[]",
                        "ASDFGHJKL;'",
                        "ZXCVBNM,./"]
        load_keys(self.letters, self.sprites, self.key_sprites, self.K_SIZE, self.color, GAME_FONT)
        self.chars = list()

        # For screen shake
        self.offset = repeat((0,0))
        
        # Texts
        self.text_score = PulsatingText(WIN_S[WIN_CS][0]/2, 100, self.score, GAME_FONT, 48, "ORANGE")
        self.text_title = PulsatingText(88,16, "Keyboard", GAME_FONT, 16, "WHITE")
        self.text_title2 = PulsatingText(88,32, "Smasher", GAME_FONT, 16, "WHITE")
        self.text_ver = PulsatingText(78,48, "v.A5", GAME_FONT, 16, "WHITE")
        self.sprites.add(self.text_score)
        self.sprites.add(self.text_ver)
        self.sprites.add(self.text_title)
        self.sprites.add(self.text_title2)

    def handle_events(self):

        # Get pressed characters
        keys_pressed = list()
        scan = pygame.key.get_pressed()
        self.chars[:] = []
        if 1 in list(scan):
            for i in range(len(list(scan))):
                if scan[i] == 1:
                    keys_pressed.append(i)

            self.chars = [chr(i) for i in keys_pressed]
            
    def update(self):
        
        if len(self.chars) != 0:
            for sprite in self.key_sprites:
                if sprite.text.lower() in self.chars and not sprite.pressed:
                    sprite.unhide()
                    sprite.pressed = True

                    # Add score
                    self.score += 1
                    self.text_score.text = self.score

                    # Spawn particle
                    spawn_particles(self.sprites, self.particles, sprite.rect.centerx, sprite.rect.centery, self.color, 2)
                    # Produce iterable for screen sahke
                    self.offset = shake(10,5)
                    # Spawn shockwave / ripple...whatever you call it
                    s = Shockwave(sprite.rect.centerx, sprite.rect.centery, self.color, self.K_SIZE)
                    self.sprites.add(s)
        
        for sprite in self.key_sprites:
            if sprite.text.lower() not in self.chars:
                sprite.pressed = False
                    
        self.sprites.update()

    def draw(self, window):
        window.fill(BG_COLOR)
        self.sprites.draw(window)
        window.blit(window, next(self.offset))
    
# Application loop
def main():

    # Initialize the window
    window = pygame.display.set_mode(WIN_S[WIN_CS], HWSURFACE|DOUBLEBUF)
    pygame.display.set_caption(TITLE)

    # Loop
    running = True
    manager = SceneManager(GameScene())
    clock = pygame.time.Clock()
    FPS = 60

    while running:

        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        manager.scene.handle_events()
        manager.scene.update()
        manager.scene.draw(window)
        #print(clock.get_fps())
        pygame.display.flip()
        
# Run the application loop
main()

# Exit pygame
pygame.quit()
