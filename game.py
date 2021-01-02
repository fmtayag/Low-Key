# Import libraries
# Pygame version: Pygame 2.0.0 (SDL 2.0.12, python 3.7.9)
import pygame, os
from pygame.locals import *
from random import randrange, choice, choices
from itertools import repeat

# Initialize pygame
pygame.init()

# Metadata
TITLE = "Keyboard Smasher"
AUTHOR = "zyenapz"
EMAIL = "zyenapz@gmail.com"
WEBSITE = "zyenapz.github.io"

WIN_S = {"128x128": (128, 128),
         "256x256": (256, 256),
         "512x512": (512, 512),
         "1024x1024": (1024,1024)}
WIN_CS = "512x512" # current size

# Directories
GAME_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(GAME_DIR, "data")
IMG_DIR = os.path.join(DATA_DIR, "img")
FONT_DIR = os.path.join(DATA_DIR, "fonts")

# Palette
PALETTE = {"WHITE": (241,242,255),
           "BLACK": (20,18,29),
           "BLUE": (39,137,205),
           "CYAN": (115,239,232),
           "ORANGE": (232,138,54)}

BG_COLOR = PALETTE["BLACK"]

# Font
GAME_FONT = os.path.join(FONT_DIR, "prstartk.ttf")

def load_keys(letters, sprites, K_SIZE, color):
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
            key = Key(letter, x_pos + KB_XPOS, y_pos + KB_YPOS, K_SIZE, color)
            sprites.add(key)
            x += 1
        y += 1
        o += 1

def spawn_particles(particles, x, y, color, amount):
    for _ in range(amount):
        particles.add(Particle(x, y, color))

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
        # Sprite groups
        self.sprites = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.chars = list()

        # Color of the objects
        self.color = "ORANGE"

        # Keys
        K_SIZE = 32
        letters = ["1234567890-=",
                   "QWERTYUIOP[]",
                   "ASDFGHJKL;'",
                   "ZXCVBNM,./"]
        load_keys(letters, self.sprites, K_SIZE, self.color)
        # For screen shake
        self.offset = repeat((0,0))
        
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
            for sprite in self.sprites:
                if sprite.text.lower() in self.chars and not sprite.pressed:
                    sprite.unhide()
                    sprite.pressed = True
                    spawn_particles(self.particles, sprite.rect.centerx, sprite.rect.centery, self.color, 2)
                    self.offset = shake(10,5)
        
        for sprite in self.sprites:
            if sprite.text.lower() not in self.chars:
                sprite.pressed = False
                    
        self.sprites.update()
        self.particles.update()

    def draw(self, window):
        window.fill(BG_COLOR)
        self.sprites.draw(window)
        self.particles.draw(window)
        window.blit(window, next(self.offset))

class Key(pygame.sprite.Sprite):
    def __init__(self, text, x, y, K_SIZE, color):
        super().__init__()
        self.color = color
        self.K_SIZE = K_SIZE
        self.image = pygame.Surface((self.K_SIZE,self.K_SIZE))
        self.image.fill(BG_COLOR)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.text = text
        self.font = pygame.font.Font(GAME_FONT, self.K_SIZE//2)
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.hide_delay = 250
        self.alpha = 255
        self.pressed = False
        #self.unhide()
        
    def update(self):
        if not self.hidden:
            self.hide()
        
    def unhide(self):
        self.hidden = False
        self.alpha = 255
        #pygame.draw.polygon(self.image, PALETTE[self.color], [(10,0),(0,10),(20,10),(10,20)], 1)
        pygame.draw.rect(self.image, PALETTE[self.color], (0,0,self.K_SIZE,self.K_SIZE), 8)
        self.r_font = self.font.render(self.text, 0, PALETTE[self.color])
        self.image.blit(self.r_font, (9,8))
        self.image.set_alpha(self.alpha)
        self.hide_timer = pygame.time.get_ticks()

    def hide(self):
        now = pygame.time.get_ticks()
        if now - self.hide_timer > self.hide_delay:
            self.alpha -= 10
            self.image.set_alpha(self.alpha)
            if self.alpha <= 0:
                self.hidden = True

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((8,8))
        self.image.fill(PALETTE[color])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.movspd = 8
        self.spdx = choice([num for num in range(-8,8) if num not in [-2,-1,0,1,2]])
        self.spdy = choice([num for num in range(-6,6) if num not in [-2,-1,0,1,2]])
        self.size = choice([8,12])

    def update(self):
        self.rect.x += self.spdx
        self.rect.y += self.spdy
        if self.spdx > 0:
            self.spdx -= 0.1
        if self.spdy < self.movspd:
            self.spdy += 0.1
        elif self.spdy > self.movspd:
            self.spdy -= 0.1

        if self.rect.y > WIN_S[WIN_CS][1]:
            self.kill()
    
# Application loop
def main():

    # Initialize the window
    window = pygame.display.set_mode(WIN_S[WIN_CS], HWSURFACE|DOUBLEBUF|NOFRAME)
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
