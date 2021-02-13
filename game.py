# Low Key
# Programming by: zyenapz
    # E-maiL: zyenapz@gmail.com
    # Website: zyenapz.github.io
# Pygame version: Pygame 2.0.0 (SDL 2.0.12, python 3.7.9)

# Metadata
TITLE = "Low Key"
AUTHOR = "zyenapz"
EMAIL = "zyenapz@gmail.com"
WEBSITE = "zyenapz.github.io"

import pygame, os, sys, pickle, datetime
from pygame.locals import *
from random import randrange, choice, choices
from itertools import repeat
from data.scripts.sprites import Key, Particle, Shockwave, Text, PulsatingText, FadingText, Bubble, KFKey, Blast
from data.scripts.constants import *
from data.scripts.scenebases import Scene, SceneManager

# Initialize pygame
pygame.init()

# Directories
GAME_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(GAME_DIR, "data")
IMG_DIR = os.path.join(DATA_DIR, "img")
FONT_DIR = os.path.join(DATA_DIR, "fonts")
SFX_DIR = os.path.join(DATA_DIR, "sfx")
GAME_FONT = os.path.join(FONT_DIR, "prstartk.ttf")

# Load sounds
def load_sound(filename, sfx_dir, volume):
    path = os.path.join(sfx_dir, filename)
    snd = pygame.mixer.Sound(path)
    snd.set_volume(volume)
    return snd

sfx_enter = load_sound("enter.wav", SFX_DIR, 0.5)
sfx_select = load_sound("select.wav", SFX_DIR, 0.5)
sfx_denied = load_sound("denied.wav", SFX_DIR, 0.5)
sfx_presses = [
    load_sound("press1.wav", SFX_DIR, 0.1),
    load_sound("press2.wav", SFX_DIR, 0.1),
    load_sound("press3.wav", SFX_DIR, 0.1)
]
sfx_awards = [
    load_sound("award1.wav", SFX_DIR, 0.1),
    load_sound("award2.wav", SFX_DIR, 0.1),
    load_sound("award3.wav", SFX_DIR, 0.1)
]
sfx_go = load_sound("go.wav", SFX_DIR, 0.3)

# Functions
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

def load_png(file, directory, scale, convert_alpha=False):
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
        print(f"Error for {file}: {e} Loading default texture instead.")
        s = pygame.Surface((32,32))
        s.fill('red')
        return s

# Game Data
class GameData:
    def __init__(self):
        # stats for nerds
        self.high_score = 0
        self.times_pressed = 0
        self.play_time = 0

game_data = GameData()

# Load game data
try:
    infile = open(os.path.join(DATA_DIR, "user_data.dat"), "rb")
    game_data = pickle.load(infile)
    infile.close()
except:
    # Save game data
    outfile = open(os.path.join(DATA_DIR, "user_data.dat"), "wb")
    pickle.dump(game_data, outfile)
    outfile.close()


class TitleScene(Scene):
    def __init__(self):
        # Screen shake
        sfx_enter.play()
        self.offset = repeat((0,0))
        self.offset = shake(10,5)

        # Menu
        self.img_logo = load_png("logo.png", IMG_DIR, 8)
        self.menu_area = pygame.Surface((300,400))

        self.selector_width = self.menu_area.get_width() * 0.9
        self.selector_height = 56
        self.selector_x = self.menu_area.get_width() / 2 - self.selector_width / 2
        self.selector_y = 32
        self.menu_texts_size = 32
        self.menu_texts_y = 64
        self.selected_option = 0

        self.menu_options = [
            ClassicGameScene,
            StatsScene
        ]

        # Sprite groups
        self.sprites = pygame.sprite.Group()
        self.bubbles = pygame.sprite.Group()
        self.menu_texts = pygame.sprite.Group()

        # Images
        self.img_background = load_png("background.png", IMG_DIR, 8)

        # Color of the objects
        self.color = PALETTE["CYAN"]
        self.color_palette = PALETTE["CYAN_PAL"]

        # Texts
        #self.text_title1 = Text(WIN_SZ[0]/2, WIN_SZ[1]/4, "low key", GAME_FONT, 64, PALETTE["WHITE"])
        #=self.text_title2 = Text(WIN_SZ[0]/2, WIN_SZ[1]/4, "", GAME_FONT, 48, PALETTE["WHITE"])
        self.text_developer = Text(WIN_SZ[0]/2, WIN_SZ[1]/4 + 128, "by Zyenapz", GAME_FONT, 28, PALETTE["WHITE"])
        self.text_play = Text(self.menu_area.get_width() / 2, self.menu_texts_y * 1, "Play", GAME_FONT, self.menu_texts_size, PALETTE["WHITE"])
        #self.text_shop = Text(self.menu_area.get_width() / 2, self.menu_texts_y * 2, "Shop", GAME_FONT, self.menu_texts_size, PALETTE["WHITE"])
        self.text_stats = Text(self.menu_area.get_width() / 2, self.menu_texts_y * 2, "Stats", GAME_FONT, self.menu_texts_size, PALETTE["WHITE"])
        #self.text_credits = Text(self.menu_area.get_width() / 2, self.menu_texts_y * 4, "Credits", GAME_FONT, self.menu_texts_size, PALETTE["WHITE"])
        self.text_quit = Text(self.menu_area.get_width() / 2, self.menu_texts_y * 3, "Quit", GAME_FONT, self.menu_texts_size, PALETTE["WHITE"])

        #self.sprites.add(self.text_title1)
        #self.sprites.add(self.text_title2)
        self.sprites.add(self.text_developer)
        self.menu_texts.add(self.text_play)
        #self.menu_texts.add(self.text_shop)
        self.menu_texts.add(self.text_stats)
        #self.menu_texts.add(self.text_credits)
        self.menu_texts.add(self.text_quit)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:       
                if (event.key == pygame.K_s or event.key == pygame.K_DOWN) and self.selected_option < len(self.menu_options):
                    self.selector_y += self.menu_texts_y
                    self.selected_option += 1
                    sfx_select.play()
                elif (event.key == pygame.K_w or event.key == pygame.K_UP) and self.selected_option > 0:
                    self.selector_y -= self.menu_texts_y
                    self.selected_option -= 1
                    sfx_select.play()
                elif event.key == pygame.K_RETURN:
                    if self.selected_option != len(self.menu_options):
                        self.manager.go_to(self.menu_options[self.selected_option]())
                    else:
                        # Save game data
                        outfile = open(os.path.join(DATA_DIR, "user_data.dat"), "wb")
                        pickle.dump(game_data, outfile)
                        outfile.close()

                        pygame.quit()
                        sys.exit()

    def update(self): 
        if len(self.bubbles) <= 20:
            b = Bubble(WIN_SZ, PALETTE["CYAN_PAL"])
            self.bubbles.add(b)

        self.sprites.update()
        self.menu_texts.update()
        self.bubbles.update()

    def draw(self, window):
        window.fill(BG_COLOR)
        window.blit(self.img_background, (0,0))
        self.bubbles.draw(window)
        self.sprites.draw(window)
        window.blit(self.img_logo, (WIN_SZ[0] / 2 - self.img_logo.get_width() / 2,30))

        self.menu_area.fill('black')
        self.menu_area.set_colorkey('black')
        self.menu_texts.draw(self.menu_area)
        pygame.draw.rect(self.menu_area, 'white', (self.selector_x,self.selector_y,self.selector_width,self.selector_height), 8)
        window.blit(self.menu_area, (window.get_width() / 2 - self.menu_area.get_width() / 2, window.get_height() / 2))
        window.blit(window, next(self.offset))

class StatsScene(Scene):
    def __init__(self):
        sfx_enter.play()

        # Screen shake
        self.offset = repeat((0,0))
        self.offset = shake(10,5)

        # Stats area
        self.stats_area = pygame.Surface((WIN_SZ[0] - 64,500))
        self.stats_area.fill(BG_COLOR)
        self.stats_area.set_colorkey(BG_COLOR)

        # Sprite groups
        self.stats_texts = pygame.sprite.Group()
        self.bubbles = pygame.sprite.Group()

        # Images
        self.img_background = load_png("background.png", IMG_DIR, 8)

        # Texts
        self.text_statsheader = Text(self.stats_area.get_width() / 2,64, "STATS", GAME_FONT, 44, PALETTE['WHITE'])
        self.text_highscore = Text(16,128, f"Hi-score: {game_data.high_score}", GAME_FONT, 24, PALETTE['WHITE'], False)
        self.text_timespressed = Text(16, 184, f"Presses: {game_data.times_pressed}", GAME_FONT, 24, PALETTE['WHITE'], False)
        # Compute time
        minutes = round(game_data.play_time / 1000) // 60
        seconds = round(game_data.play_time / 1000) % 60
        time = f"{minutes}m{seconds}s"
        self.text_playtime = Text(16, 240, f"Play time: {time}", GAME_FONT, 22, PALETTE['WHITE'], False)
        self.text_exitbutton = Text(self.stats_area.get_width() / 2, self.stats_area.get_height() * 0.9, "[ESC]", GAME_FONT, 24, PALETTE['WHITE'])

        self.stats_texts.add(self.text_statsheader)
        self.stats_texts.add(self.text_highscore)
        self.stats_texts.add(self.text_timespressed)
        self.stats_texts.add(self.text_playtime)
        self.stats_texts.add(self.text_exitbutton)
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.manager.go_to(TitleScene())
    
    def update(self):
        # Spawn bubbles
        if len(self.bubbles) <= 20:
            b = Bubble(WIN_SZ, PALETTE["CYAN_PAL"])
            self.bubbles.add(b)

        self.stats_texts.update()
        self.bubbles.update()

    def draw(self, window):
        window.fill(BG_COLOR)
        window.blit(self.stats_area, (32,32))
        window.blit(self.img_background, (0,0))
        self.bubbles.draw(window)
        self.stats_texts.draw(self.stats_area)
        window.blit(window, next(self.offset))

class ClassicGameScene(Scene):
    def __init__(self):
        sfx_enter.play()

        # Game variables
        self.score = 0
        self.offset = repeat((0,0)) # For screen shake
        self.offset = shake(10,5)
        self.cur_ticks = 0
        self.timer = 25 * 1000 + self.cur_ticks # n * 1000. Default: n = 20, Debug: n = 5
        self.rem_time = round((self.timer-self.cur_ticks) / 1000)
        self.is_paused = False
        self.choose_mash_ticks = 0
        self.choose_mash_delay = 5000
        self.mash_duration = 3000
        self.mash_ticks = 0
        self.mash_reward = 2
        self.selected_letter = "none"
        self.mash_reward_score = 2
        self.get_ready_ticks = 0
        self.get_ready_delay = 4000
        self.is_ready = False
        self.play_ready_sfx_ticks = 0

        # Sprite groups
        self.sprites = pygame.sprite.Group()
        self.key_sprites = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.bubbles = pygame.sprite.Group()
        self.ready_texts = pygame.sprite.Group()

        # Images
        self.img_background = load_png("background.png", IMG_DIR, 8)

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
        self.text_readytime = PulsatingText(WIN_SZ[0]/2, 300, "Get Ready", GAME_FONT, 48, self.color)
        self.text_scorelabel = Text(WIN_SZ[0]/2, 60, "Score", GAME_FONT, 64, self.color)
        self.text_score = PulsatingText(WIN_SZ[0]/2, 100, self.score, GAME_FONT, 64, self.color)
        timer_text = f"T{self.rem_time}"
        self.text_time = PulsatingText(WIN_SZ[0]/2, 200, timer_text, GAME_FONT, 48, PALETTE["WHITE"])
        #self.sprites.add(self.text_scorelabel)
        self.sprites.add(self.text_score)
        self.sprites.add(self.text_time)
        self.sprites.add(self.text_readytime)
        self.ready_texts.add(self.text_readytime)

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
                    sfx_enter.play()
                if event.key == pygame.K_x and self.is_paused:
                    self.manager.go_to(TitleScene())
                else:
                    try:
                        if chr(event.key).upper() in "1234567890QWERTYUIOPASDFGHJKLZXCVBNM[];',./-=" or event.key == pygame.K_SPACE:
                            if self.is_ready:
                                choice(sfx_presses).play()
                            else:
                                sfx_denied.play()
                    except:
                        pass
        
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

        if not self.is_paused and self.is_ready:
            # Mash event
            if self.choose_mash_ticks >= self.choose_mash_delay and self.selected_letter == "none":
                row = randrange(0, len(self.letters))
                letters_list = [c for c in self.letters[0] if (c != "O") and (c != "0") and (c != " ") and (c != "")]
                self.selected_letter = choice(letters_list)
                txt_exit = FadingText(WIN_SZ[0]/2, WIN_SZ[1]/2, f"SMASH {self.selected_letter}!", GAME_FONT, 48, PALETTE["WHITE"], self.mash_duration * 1.5)
                self.sprites.add(txt_exit)

            if self.selected_letter != "none":
                self.mash_ticks += 10

                if self.mash_ticks >= self.mash_duration:
                    self.selected_letter = "none"
                    self.choose_mash_ticks = 0
                    self.mash_ticks = 0
                    self.mash_duration = randrange(2000,3000)
                    self.mash_reward = 2
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

                        # Spawn particle
                        spawn_particles(self.sprites, self.particles, sprite.rect.centerx, sprite.rect.centery, self.color_palette, 2)

                        # Produce iterable for screen sahke
                        self.offset = shake(10,5)

                        # Spawn shockwave / ripple...whatever you call it
                        s = Shockwave(sprite.rect.centerx, sprite.rect.centery, self.color, self.K_SIZE)
                        self.sprites.add(s)

                        # Mash event reward
                        if sprite.text == self.selected_letter:
                            reward_roll = choice(choices(("score", "time"), weights=[7,3]))
                            if reward_roll == "score":
                                txt_mash = FadingText(randrange(0, WIN_SZ[0]), randrange(0, WIN_SZ[1]/2), f"+{round(self.mash_reward)}", GAME_FONT, 24, PALETTE["WHITE"], 500)
                                self.sprites.add(txt_mash)
                                self.mash_reward += 0.05
                                self.score += round(self.mash_reward)
                            elif reward_roll == "time":
                                txt_mash = FadingText(randrange(0, WIN_SZ[0]), randrange(0, WIN_SZ[1]/2), "+TIME!", GAME_FONT, 24, PALETTE["WHITE"], 500)
                                self.sprites.add(txt_mash)
                                self.timer += 100
                            choice(sfx_awards).play()

                        game_data.times_pressed += 1
            
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

            # Update sprites
            self.sprites.update()
            self.text_time.text = f"T{self.rem_time}"
            self.text_score.text = self.score

        elif not self.is_ready and not self.is_paused:
            self.get_ready_ticks += 10
            self.play_ready_sfx_ticks += 10
            if self.play_ready_sfx_ticks >= 1000:
                sfx_enter.play()
                self.play_ready_sfx_ticks = 0
            if self.get_ready_ticks > 1000:
                self.text_readytime.text = f"{self.get_ready_delay // 1000 - round(self.get_ready_ticks // 1000)}"
            if self.get_ready_ticks > self.get_ready_delay - 100:
                self.is_ready = True
                self.text_go = FadingText(WIN_SZ[0]/2, 290, "Press", GAME_FONT, 48, self.color, 3000)
                self.text_go2 = FadingText(WIN_SZ[0]/2, 340, "Keys!", GAME_FONT, 48, self.color, 3000)
                self.sprites.add(self.text_go)
                self.sprites.add(self.text_go2)
                self.text_readytime.kill()
                sfx_go.play()
            for key in self.key_sprites:
                key.unhide()
            self.sprites.update()
            self.ready_texts.update()

    def draw(self, window):
        if not self.is_paused:
            window.fill(BG_COLOR)
            self.sprites.draw(window)
            window.blit(self.img_background, next(self.offset))
            window.blit(window, next(self.offset))
        else:
            self.paused_texts.draw(window)

class GameOverScene(Scene):
    def __init__(self, score):
        sfx_enter.play()

        # Screen shake
        self.offset = repeat((0,0))
        self.offset = shake(10,5)

        self.score = score
        if self.score > game_data.high_score:
            game_data.high_score = self.score 

        # Images
        self.img_background = load_png("background.png", IMG_DIR, 8)

        # Sprites
        self.sprites = pygame.sprite.Group()
        self.bubbles = pygame.sprite.Group()

        # Texts
        self.text_go = Text(WIN_SZ[0]/2, WIN_SZ[1]/2 - 198, "Game", GAME_FONT, 96, PALETTE["WHITE"])
        self.text_go2 = Text(WIN_SZ[0]/2, WIN_SZ[1]/2 - 96, "Over", GAME_FONT, 96, PALETTE["WHITE"])
        self.text_score = Text(WIN_SZ[0]/2, WIN_SZ[1]/2, f"Score: {self.score}", GAME_FONT, 32, PALETTE["WHITE"])
        self.text_comment = Text(WIN_SZ[0]/2, WIN_SZ[1]/1.6, self.generate_comment(self.score), GAME_FONT, 32, PALETTE["WHITE"])
        self.text_return = Text(WIN_SZ[0]/2, WIN_SZ[1]/1.4, "[RETURN]", GAME_FONT, 32, PALETTE["WHITE"])

        self.sprites.add(self.text_go)
        self.sprites.add(self.text_go2)
        self.sprites.add(self.text_score)
        self.sprites.add(self.text_comment)
        self.sprites.add(self.text_return)

    def handle_events(self, events):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RETURN]:
            self.manager.go_to(TitleScene())

    def update(self):
        # Spawn bubbles
        if len(self.bubbles) <= self.score // 50 and len(self.bubbles) <= 20:
            b = Bubble(WIN_SZ, PALETTE["CYAN_PAL"])
            self.bubbles.add(b)

        self.sprites.update()
        self.bubbles.update()

    def draw(self, window):
        window.fill(BG_COLOR)
        window.blit(self.img_background, (0,0))
        self.bubbles.draw(window)
        self.sprites.draw(window)
        window.blit(window, next(self.offset))

    def generate_comment(self, score):
        if score < 0:
            return "HOW THE F-?!"
        elif score == 0:
            return "Lol"
        elif score < 100:
            return "Meh..."
        elif score < 500:
            return "Alright!"
        elif score >= 5000:
            return "Auto Clicker!"
        elif score >= 3000:
            return "Impossible!"
        elif score >= 2000:
            return "Godlike!"
        elif score >= 1000:
            return "Awesome!"
        elif score >= 500:
            return "Good!"
    
# Application loop
def main():

    # Initialize the window
    window = pygame.display.set_mode(WIN_SZ, HWSURFACE|DOUBLEBUF)
    pygame.display.set_caption(TITLE)
    pygame.mouse.set_visible = False
    pygame.display.set_icon(load_png("icon.png", IMG_DIR, 1))

    # Loop
    running = True
    manager = SceneManager(TitleScene())
    clock = pygame.time.Clock()
    FPS = 60

    while running:
        
        clock.tick(FPS)
        game_data.play_time += 10

        if pygame.event.get(QUIT):
            running = False

            # Save game data
            outfile = open(os.path.join(DATA_DIR, "user_data.dat"), "wb")
            pickle.dump(game_data, outfile)
            outfile.close()

        manager.scene.handle_events(pygame.event.get())
        manager.scene.update()
        manager.scene.draw(window)

        pygame.display.flip()
    
# Run the application loop
main()

# Exit pygame and application
pygame.quit()
sys.exit()