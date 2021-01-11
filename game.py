# Import libraries
# Pygame version: Pygame 2.0.0 (SDL 2.0.12, python 3.7.9)
import pygame, os, sys
from pygame.locals import *
from random import randrange, choice, choices
from itertools import repeat
from data.scripts.sprites import Key, Particle, Shockwave, Text, PulsatingText, FadingText, Bubble, KFKey
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
    KB_YPOS = 390 # y pos of the whole keyboard

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
    
    def handle_events(self, events):
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
        # Sprite groups
        self.sprites = pygame.sprite.Group()
        self.bubbles = pygame.sprite.Group()

        # Color of the objects
        self.color = PALETTE["CYAN"]
        self.color_palette = PALETTE["CYAN_PAL"]

        # Texts
        self.text_title1 = Text(WIN_SZ[0]/2, WIN_SZ[1]/4, "Keyboard", GAME_FONT, 48, PALETTE["WHITE"])
        self.text_title2 = Text(WIN_SZ[0]/2, WIN_SZ[1]/3, "Smasher", GAME_FONT, 48, PALETTE["WHITE"])
        self.text_play = Text(WIN_SZ[0]/2, WIN_SZ[1]/1.5, "[Z] Play", GAME_FONT, 32, PALETTE["WHITE"])
        self.text_quit = Text(WIN_SZ[0]/2, WIN_SZ[1]/1.35, "[X] Quit", GAME_FONT, 32, PALETTE["WHITE"])

        self.sprites.add(self.text_title1)
        self.sprites.add(self.text_title2)
        self.sprites.add(self.text_play)
        self.sprites.add(self.text_quit)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    self.manager.go_to(ClassicGameScene())
                elif event.key == pygame.K_x:
                    pygame.quit()
                    sys.exit()

    def update(self): 
        # Spawn bubbles
        if len(self.bubbles) <= 20:
            b = Bubble(WIN_SZ, PALETTE["CYAN_PAL"])
            self.bubbles.add(b)

        self.sprites.update()
        self.bubbles.update()

    def draw(self, window):
        window.fill(BG_COLOR)
        self.bubbles.draw(window)
        self.sprites.draw(window)

class ClassicGameScene(Scene):
    def __init__(self):
        # Game variables
        self.score = 0
        self.offset = repeat((0,0)) # For screen shake
        self.cur_ticks = 0
        self.timer = 15 * 1000 + self.cur_ticks # n * 1000. Default: n = 60, Debug: n = 5
        self.rem_time = round((self.timer-self.cur_ticks) / 1000)
        self.is_paused = False
        self.choose_mash_ticks = 0
        self.choose_mash_delay = 5000
        self.mash_duration = 3000
        self.mash_ticks = 0
        self.selected_letter = "none"

        # Sprite groups
        self.sprites = pygame.sprite.Group()
        self.key_sprites = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.bubbles = pygame.sprite.Group()

        # Color of the objects
        self.color = PALETTE["CYAN"]
        self.color_palette = PALETTE["CYAN_PAL"]

        # Keys
        self.K_SIZE = 32 # key size
        self.letters = ["1234567890-=",
                        "QWERTYUIOP[]",
                        "ASDFGHJKL;'",
                        "ZXCVBNM,./"]
        self.key_shape = "roundrect" # rect, roundrect, round, arc
        self.chars = list()
        load_keys(self.letters, self.sprites, self.key_sprites, self.K_SIZE, self.color, GAME_FONT, self.key_shape)

        # Texts for the game
        self.text_score = PulsatingText(WIN_SZ[0]/2, 100, self.score, GAME_FONT, 64, self.color)
        timer_text = f"T{self.rem_time}"
        self.text_time = PulsatingText(WIN_SZ[0]/2, 200, timer_text, GAME_FONT, 48, PALETTE["WHITE"])
        self.sprites.add(self.text_score)
        self.sprites.add(self.text_time)

        # Texts for the pause screen
        self.paused_texts = pygame.sprite.Group()
        txt_paused = Text(WIN_SZ[0]/2, WIN_SZ[1]/2, "PAUSED", GAME_FONT, 48, PALETTE["WHITE"])
        txt_resume = Text(WIN_SZ[0]/2, WIN_SZ[1]/1.65, "[ESC] Resume", GAME_FONT, 24, PALETTE["WHITE"])
        txt_exit = Text(WIN_SZ[0]/2, WIN_SZ[1]/1.50, "[X] Exit", GAME_FONT, 24, PALETTE["WHITE"])
        self.paused_texts.add(txt_paused)
        self.paused_texts.add(txt_resume)
        self.paused_texts.add(txt_exit)

    def handle_events(self, events):
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_paused = not self.is_paused
                if event.key == pygame.K_x and self.is_paused:
                    self.manager.go_to(TitleScene())
        
        if not self.is_paused:
            # Get pressed characters
            keys_pressed = list()
            scan = pygame.key.get_pressed()
            self.chars[:] = []
            if 1 in list(scan):
                for i in range(len(list(scan))):
                    if scan[i] == 1:
                        keys_pressed.append(i)
                self.chars = [chr(i) for i in keys_pressed] # note: spacebar ascii conversion is ' '

            # Automatically press letters randomly 
            # TODO - this code is ugly as shit but it works
            #auto_row = randrange(0, len(self.letters))
            #automatic = [c for c in self.letters[auto_row][randrange(0, len(self.letters[auto_row]))].lower()]
            #self.chars.append(automatic[0])
            #print(self.chars)

            if self.rem_time <= 0:
                self.manager.go_to(GameOverScene(self.score))
            
    def update(self):
        
        if not self.is_paused:
           # Mash event
            if self.choose_mash_ticks >= self.choose_mash_delay and self.selected_letter == "none":
                row = randrange(0, len(self.letters))
                letters_list = [c for c in self.letters[row]]
                self.selected_letter = choice(letters_list)
                txt_exit = FadingText(WIN_SZ[0]/2, WIN_SZ[1]/2, f"MASH {self.selected_letter}", GAME_FONT, 48, PALETTE["WHITE"], self.mash_duration * 1.5)
                self.sprites.add(txt_exit)

            if self.selected_letter != "none":
                self.mash_ticks += 10

                if self.mash_ticks >= self.mash_duration:
                    self.selected_letter = "none"
                    self.choose_mash_ticks = 0
                    self.mash_ticks = 0
            else:
                self.choose_mash_ticks += 10

            #print(self.choose_mash_ticks, self.mash_ticks)

            # Increment current ticks
            self.cur_ticks += 10

            # Act on key presses
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

                        # Mash event
                        if sprite.text == self.selected_letter:
                            txt_mash = FadingText(randrange(0, WIN_SZ[0]), randrange(0, WIN_SZ[1]/2), f"TIME!", GAME_FONT, 24, PALETTE["WHITE"], 500)
                            self.sprites.add(txt_mash)
                            self.timer += 0.2 * 1000
            
            # Unpress the key if it is not in self.chars
            for sprite in self.key_sprites:
                if sprite.text.lower() not in self.chars:
                    sprite.pressed = False

            # Spawn bubbles
            if len(self.bubbles) <= self.score // 50 and len(self.bubbles) <= 20:
                b = Bubble(WIN_SZ, PALETTE["CYAN_PAL"])
                self.sprites.add(b)
                self.bubbles.add(b)

            # Update time
            if self.rem_time <= 0:
                self.rem_time = 0
            else:
                self.rem_time = round((self.timer-self.cur_ticks) / 1000)

            self.text_time.text = f"T{self.rem_time}" # Update timer text

            # Update sprites
            self.sprites.update()

    def draw(self, window):
        if not self.is_paused:
            window.fill(BG_COLOR)
            self.sprites.draw(window)
            window.blit(window, next(self.offset))
        else:
            self.paused_texts.draw(window)

class KeyfallGameScene(Scene):
    # Still brainstorming. The gameplay isn't fun currently.
    def __init__(self):

        # Game variables
        self.score = 0
        self.offset = repeat((0,0)) # For screen shake
        self.is_paused = False

        # Keys
        self.color = PALETTE["CYAN"]
        self.color_palette = PALETTE["CYAN_PAL"]
        self.key_shape = "roundrect" # rect, roundrect, round, arc
        self.K_SIZE = 32 # key size
        self.letters = "QWERTYUIOPASDFGHJKLZXCVBNM"
        self.letters = [char for char in self.letters]
        self.chars = list()

        # Sprite groups
        self.sprites = pygame.sprite.Group()
        self.key_sprites = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.bubbles = pygame.sprite.Group()

        # Texts
        self.text_score = PulsatingText(WIN_SZ[0]/2, WIN_SZ[1]/1.2, self.score, GAME_FONT, 64, PALETTE["WHITE"])
        self.sprites.add(self.text_score)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_paused = not self.is_paused
                if event.key == pygame.K_x and self.is_paused:
                    self.manager.go_to(TitleScene())

                if not self.is_paused:
                    self.chars.append(chr(event.key))
    
        #print(self.chars)

    def update(self):
        if not self.is_paused:

            # Act on key presses
            if len(self.chars) != 0:
                for sprite in self.key_sprites:
                    if sprite.text.lower() in self.chars and not sprite.pressed:
                        sprite.hide()
                        sprite.pressed = True
                        sprite.speed = 0

                        # Add score
                        self.score += 1
                        self.text_score.text = self.score

                        # Spawn shockwave / ripple...whatever you call it
                        s = Shockwave(sprite.rect.centerx, sprite.rect.centery, self.color, self.K_SIZE)
                        self.sprites.add(s)

                        # Spawn particle
                        spawn_particles(self.sprites, self.particles, sprite.rect.centerx, sprite.rect.centery, self.color_palette, 2)

                        # Produce iterable for screen sahke
                        self.offset = shake(10,5)
                        
                        self.chars = list()
                        break
            
            # Produces a pretty cool bug!
            # Unpress the key if it is not in self.chars
            #for sprite in self.key_sprites:
                #if sprite.text.lower() not in self.chars:
                    #sprite.pressed = False

            # Spawn bubbles
            if len(self.bubbles) <= self.score // 50 and len(self.bubbles) <= 20:
                b = Bubble(WIN_SZ, PALETTE["CYAN_PAL"])
                self.sprites.add(b)
                self.bubbles.add(b)        

            # Spawn key
            if len(self.key_sprites) < 8:
                has_duplicate = False
                k = KFKey(choice(self.letters), randrange(32, WIN_SZ[0]-32), randrange(-256,-32), self.K_SIZE, self.color, GAME_FONT, self.key_shape, randrange(2,4))

                for sprite in self.key_sprites:
                    if sprite.text.lower() == k.text.lower():
                        has_duplicate = True

                # Prevent overlapping sprites
                if not has_duplicate and not pygame.sprite.spritecollide(k, self.key_sprites, True):
                    self.sprites.add(k)
                    self.key_sprites.add(k)

            self.sprites.update()

    def draw(self, window):
        if not self.is_paused:
            window.fill(BG_COLOR)
            self.bubbles.draw(window)
            self.sprites.draw(window)
            window.blit(window, next(self.offset))
            self.sprites.draw(window)
        else:
            self.paused_texts.draw(window)

class GameOverScene(Scene):
    def __init__(self, score):
        self.score = score

        # Sprites
        self.sprites = pygame.sprite.Group()

        # Texts
        self.text_go = Text(WIN_SZ[0]/2, WIN_SZ[1]/3, "Game Over", GAME_FONT, 48, PALETTE["WHITE"])
        self.text_score = Text(WIN_SZ[0]/2, WIN_SZ[1]/2, self.score, GAME_FONT, 32, PALETTE["WHITE"])
        # TODO - make a comments function, complimenting the player
        self.text_comment = Text(WIN_SZ[0]/2, WIN_SZ[1]/1.6, "Pretty good!", GAME_FONT, 32, PALETTE["WHITE"])
        self.text_return = Text(WIN_SZ[0]/2, WIN_SZ[1]/1.4, "[R] Return", GAME_FONT, 32, PALETTE["WHITE"])

        self.sprites.add(self.text_go)
        self.sprites.add(self.text_score)
        self.sprites.add(self.text_comment)
        self.sprites.add(self.text_return)

    def handle_events(self, events):
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
    window = pygame.display.set_mode(WIN_SZ, HWSURFACE|DOUBLEBUF)
    pygame.display.set_caption(TITLE)
    pygame.mouse.set_cursor(*pygame.cursors.tri_left)

    # Loop
    running = True
    manager = SceneManager(KeyfallGameScene())
    clock = pygame.time.Clock()
    FPS = 60

    while running:
        
        clock.tick(FPS)
        
        if pygame.event.get(QUIT):
            running = False

        manager.scene.handle_events(pygame.event.get())
        manager.scene.update()
        manager.scene.draw(window)

        pygame.display.flip()
    
# Run the application loop
main()

# Exit pygame and application
pygame.quit()
sys.exit()
