# Import libraries
# Pygame version: Pygame 2.0.0 (SDL 2.0.12, python 3.7.9)
import pygame, os
from pygame.locals import *
from random import randrange, choice, choices
from itertools import repeat
from data.scripts.sprites import Key, Particle, Shockwave, Text, PulsatingText, FadingText
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

def load_keys(letters, sprites, key_sprites, K_SIZE, color, font, shape):
    x = 0 # x offset
    y = 0 # y offset
    o = 0 # row offset
    KB_XPOS = 50 # x pos of the whole keyboard
    KB_YPOS = 320 # y pos of the whole keyboard

    for row in letters:
        x = 0
        for letter in row:
            x_pos = K_SIZE*x + (x*K_SIZE/8) + (16*o)
            y_pos = 38*y
            key = Key(letter, x_pos + KB_XPOS, y_pos + KB_YPOS, K_SIZE, color, font, shape)
            sprites.add(key)
            key_sprites.add(key)
            x += 1
        y += 1
        o += 1

    # Just winging it here.
    # This is placing the spacebar on the keyboard. Not my proudest block of code.
    y_pos = 38 * len(letters)
    key = Key(" ", KB_XPOS + 190,  y_pos + KB_YPOS, K_SIZE, color, font, shape, spacebar=True)
    sprites.add(key)
    key_sprites.add(key)

def spawn_particles(sprites, particles, x, y, colors, amount):
    for _ in range(amount):
        p = Particle(x, y, colors)
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

class TitleScene(Scene):
    def __init__(self):
        self.sprites = pygame.sprite.Group()

        self.text_title1 = Text(WIN_S[WIN_CS][0]/2, WIN_S[WIN_CS][1]/4, "Keyboard", GAME_FONT, 48, PALETTE["WHITE"])
        self.text_title2 = Text(WIN_S[WIN_CS][0]/2, WIN_S[WIN_CS][1]/3, "Smasher", GAME_FONT, 48, PALETTE["WHITE"])
        self.text_play = Text(WIN_S[WIN_CS][0]/2, WIN_S[WIN_CS][1]/1.5, "[Z] Play", GAME_FONT, 32, PALETTE["WHITE"])
        self.text_quit = Text(WIN_S[WIN_CS][0]/2, WIN_S[WIN_CS][1]/1.35, "[X] Quit", GAME_FONT, 32, PALETTE["WHITE"])

        self.sprites.add(self.text_title1)
        self.sprites.add(self.text_title2)
        self.sprites.add(self.text_play)
        self.sprites.add(self.text_quit)

    def handle_events(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_z]:
            self.manager.go_to(GameScene())
        elif pressed[pygame.K_x]:
            pygame.quit()

    def update(self): 
        self.sprites.update()

    def draw(self, window):
        window.fill(BG_COLOR)
        self.sprites.draw(window)

class GameScene(Scene):
    def __init__(self):
        # Game variables
        self.score = 0
        self.offset = repeat((0,0))
        self.timer = 5 * 1000 + pygame.time.get_ticks() # n * 1000. Default: n = 30, Debug: n = 5
        self.rem_time = round((self.timer-pygame.time.get_ticks()) / 1000)

        # Sprite groups
        self.sprites = pygame.sprite.Group()
        self.key_sprites = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()

        # Color of the objects
        self.color = PALETTE["CYAN"]
        self.color_palette = PALETTE["CYAN_PAL"]

        # Keys
        self.K_SIZE = 32 # key size
        self.letters = ["1234567890-=",
                        "QWERTYUIOP[]",
                        "ASDFGHJKL;'",
                        "ZXCVBNM,./"]
        self.key_shape = "arc" # rect, roundrect, round, arc
        self.chars = list()
        load_keys(self.letters, self.sprites, self.key_sprites, self.K_SIZE, self.color, GAME_FONT, self.key_shape)

        # Texts
        self.text_score = PulsatingText(WIN_S[WIN_CS][0]/2, 100, self.score, GAME_FONT, 48, self.color)
        timer_text = f"T{self.rem_time}"
        self.text_time = PulsatingText(256, 152, timer_text, GAME_FONT, 32, PALETTE["WHITE"])
        self.text_title = Text(88,16, "Keyboard", GAME_FONT, 16, PALETTE["WHITE"])
        self.text_title2 = Text(88,32, "Smasher", GAME_FONT, 16, PALETTE["WHITE"])
        self.text_ver = Text(78,48, "v.A5", GAME_FONT, 16, PALETTE["WHITE"])
        self.sprites.add(self.text_score)
        self.sprites.add(self.text_time)
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
            self.chars = [chr(i) for i in keys_pressed] # note: spacebar ascii conversion is ' '

        if self.rem_time <= 0:
            self.manager.go_to(GameOverScene(self.score))
            
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
                    spawn_particles(self.sprites, self.particles, sprite.rect.centerx, sprite.rect.centery, self.color_palette, 2)

                    # Produce iterable for screen sahke
                    self.offset = shake(10,5)

                    # Spawn shockwave / ripple...whatever you call it
                    s = Shockwave(sprite.rect.centerx, sprite.rect.centery, self.color, self.K_SIZE)
                    self.sprites.add(s)
        
        # Unpress the key if it is not in self.chars
        for sprite in self.key_sprites:
            if sprite.text.lower() not in self.chars:
                sprite.pressed = False

        # Update time
        if self.rem_time <= 0:
            self.rem_time = 0
        else:
            self.rem_time = round((self.timer-pygame.time.get_ticks()) / 1000)

        self.text_time.text = f"T{self.rem_time}" # Update timer text

        # Update sprites
        self.sprites.update()

    def draw(self, window):
        window.fill(BG_COLOR)
        self.sprites.draw(window)
        window.blit(window, next(self.offset))

class GameOverScene(Scene):
    def __init__(self, score):
        self.score = score

        # Sprites
        self.sprites = pygame.sprite.Group()

        # Texts
        self.text_go = Text(WIN_S[WIN_CS][0]/2, WIN_S[WIN_CS][1]/3, "Game Over", GAME_FONT, 48, PALETTE["WHITE"])
        self.text_score = Text(WIN_S[WIN_CS][0]/2, WIN_S[WIN_CS][1]/2, self.score, GAME_FONT, 32, PALETTE["WHITE"])
        # TODO - make a comments function, complimenting the player
        self.text_comment = Text(WIN_S[WIN_CS][0]/2, WIN_S[WIN_CS][1]/1.6, "Pretty good!", GAME_FONT, 32, PALETTE["WHITE"])
        self.text_return = Text(WIN_S[WIN_CS][0]/2, WIN_S[WIN_CS][1]/1.4, "[R] Return", GAME_FONT, 32, PALETTE["WHITE"])

        self.sprites.add(self.text_go)
        self.sprites.add(self.text_score)
        self.sprites.add(self.text_comment)
        self.sprites.add(self.text_return)

    def handle_events(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_r]:
            self.manager.go_to(TitleScene())


    def update(self):
        self.sprites.update()

    def draw(self, window):
        window.fill(BG_COLOR)
        self.sprites.draw(window)
    
# Application loop
def main():

    # Initialize the window
    window = pygame.display.set_mode(WIN_S[WIN_CS], HWSURFACE|DOUBLEBUF)
    pygame.display.set_caption(TITLE)

    # Loop
    running = True
    manager = SceneManager(TitleScene())
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

        pygame.display.flip()
        
# Run the application loop
main()

# Exit pygame
pygame.quit()
