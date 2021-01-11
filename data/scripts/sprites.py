import pygame
from random import randrange, choice, choices
from data.scripts.constants import *

class Key(pygame.sprite.Sprite):
    def __init__(self, text, x, y, K_SIZE, color, font_name, shape, spacebar=False):
        super().__init__()
        self.color = color
        self.K_SIZE = K_SIZE
        self.shape = shape

        # For surface
        if not spacebar:
            self.image = pygame.Surface((self.K_SIZE,self.K_SIZE))
        else:
            self.image = pygame.Surface((self.K_SIZE*7,self.K_SIZE))
        self.img_width = self.image.get_width()
        self.img_height = self.image.get_height()
        self.image.fill(BG_COLOR)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        # For text
        self.text = text
        self.font = pygame.font.Font(font_name, self.K_SIZE//2)
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.hide_delay = 500
        self.alpha = 255
        self.pressed = False
        
        # For moving arc animation
        self.animate_timer = pygame.time.get_ticks()
        self.animate_delay = 50
        self.ca = 0 # current arc config
        self.arcs_config = [
            [1,0,0,1],
            [1,1,0,0],
            [0,1,1,0],
            [0,0,1,1]
        ]
        self.arcs = self.arcs_config[0]
        self.i = 0
        
    def update(self):
        if not self.hidden:
            self.hide()
            self.redraw()

    def unhide(self):
        self.hidden = False
        self.alpha = 255
        self.image.set_alpha(self.alpha)
        self.hide_timer = pygame.time.get_ticks()

    def hide(self):
        now = pygame.time.get_ticks()
        if now - self.hide_timer > self.hide_delay:
            self.alpha -= 10
            self.image.set_alpha(self.alpha)
            if self.alpha <= 0:
                self.hidden = True

    def update_arc(self):
        now = pygame.time.get_ticks()
        if now - self.animate_timer > self.animate_delay:
            self.animate_timer = now

            if self.ca >= len(self.arcs_config) - 1:
                self.ca = 0
            else:
                self.ca += 1

            self.arcs = self.arcs_config[self.ca]

    def redraw(self):
        self.image.fill(BG_COLOR)

        if self.shape == "rect":
            pygame.draw.rect(self.image, self.color, (0,0,self.img_width,self.img_height), 8)
        elif self.shape == "roundrect":
            pygame.draw.rect(self.image, self.color, (0,0,self.img_width,self.img_height), 4, 8)
        elif self.shape == "round":
            pygame.draw.rect(self.image, self.color, (0,0,self.img_width,self.img_height), 4, 32)
        elif self.shape == "arc":
            pygame.draw.circle(self.image, self.color, (self.image.get_width()/2, self.image.get_height()/2), 
                               16, 5, self.arcs[0], self.arcs[1], self.arcs[2], self.arcs[3])
            self.update_arc()

        self.r_font = self.font.render(self.text, 0, self.color)
        self.image.blit(self.r_font, (9,8))

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.color = choice(color)
        self.size = choice([8,12])
        self.image = pygame.Surface((self.size,self.size)).convert_alpha()
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.movspd = 8
        self.spdx = choice([num for num in range(-8,8) if num not in [-2,-1,0,1,2]])
        self.spdy = choice([num for num in range(-6,6) if num not in [-2,-1,0,1,2]])

        # For fade animation
        self.alpha = 255

    def update(self):
        self.rect.x += self.spdx
        self.rect.y += self.spdy

        if self.spdy < self.movspd:
            self.spdy += 0.1
        elif self.spdy > self.movspd:
            self.spdy -= 0.1

        if self.alpha <= 0:
            self.kill()

        self.fade()

    def fade(self):
        self.alpha -= 8
        self.image.set_alpha(self.alpha)

class Shockwave(pygame.sprite.Sprite):
    def __init__(self, x, y, color, K_SIZE):
        super().__init__()
        # The surface
        self.image = pygame.Surface((K_SIZE*4,K_SIZE*4)).convert_alpha()
        self.image.set_colorkey('black')
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.img_width = self.image.get_width()
        self.color = color
        self.alpha = 255
        
        # The circle
        self.expand_timer = pygame.time.get_ticks()
        self.expand_delay = 10
        self.radius = 2
        self.c_width = 5
        self.expand_amnt = 2

    def update(self):
        self.expand()
        if self.alpha <= 0:
            self.kill()

    def expand(self):
        now = pygame.time.get_ticks()
        if now - self.expand_timer > self.expand_delay:
            self.alpha -= 10
            self.radius += self.expand_amnt
            #self.c_width += 1
            #self.image.fill((20,18,29,0))
            self.image.fill((0,0,0,0))
            self.image.set_alpha(self.alpha)
            pygame.draw.circle(self.image, self.color, self.image.get_rect().center, self.radius, self.c_width)

class Text(pygame.sprite.Sprite):
    def __init__(self, x, y, text, font_type, size, color):
        super().__init__()
        self.image = pygame.Surface((size*8 + len(str(text)) * (size/2), size*8)).convert_alpha()
        self.image.set_colorkey('black')
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        # The text
        self.text = str(text)
        self.cur_text = self.text
        self.font_type = font_type
        self.size = size
        self.color = color
        self.font = pygame.font.Font(self.font_type, self.size)
        self.rendered = self.font.render(str(self.text), 0, self.color)
        self.rendered_rect = self.rendered.get_rect(center=(self.image.get_width()/2, self.image.get_height()/2))
        self.image.blit(self.rendered, self.rendered_rect)

    def update(self):
        pass

class PulsatingText(pygame.sprite.Sprite):
    def __init__(self, x, y, text, font_type, size, color):
        super().__init__()
        # The surface
        self.image = pygame.Surface((size*8 + len(str(text)) * 4, size*8)).convert_alpha()
        self.image.set_colorkey('black')
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        # The text
        self.text = str(text)
        self.cur_text = self.text
        self.font_type = font_type
        self.size = size
        self.orig_size = self.size
        self.color = color
        self.font = pygame.font.Font(self.font_type, self.size)
        self.rendered = self.font.render(str(self.text), 0, self.color)
        self.rendered_rect = self.rendered.get_rect(center=(self.image.get_width()/2, self.image.get_height()/2))
        self.image.blit(self.rendered, self.rendered_rect)

        # Contract variables
        self.contract_timer = pygame.time.get_ticks()
        self.contract_delay = 100

    def update(self):
        # Only re-render when text changes
        if self.text != self.cur_text:
            self.cur_text = self.text
            self.re_render()
            self.expand()

        if self.size > self.orig_size:
            self.contract()

    def expand(self):
        self.size = int(self.orig_size * 1.5)

    def contract(self):
        now = pygame.time.get_ticks()
        if now - self.contract_timer > self.contract_delay:
            self.size -= 1
            self.re_render()

    def re_render(self):
        self.image.fill((0,0,0,0))
        self.font = pygame.font.Font(self.font_type, self.size)
        self.rendered = self.font.render(str(self.text), 0, self.color)
        self.rendered_rect = self.rendered.get_rect(center=(self.image.get_width()/2, self.image.get_height()/2))
        self.image.blit(self.rendered, self.rendered_rect)

class FadingText(pygame.sprite.Sprite):
    def __init__(self, x, y, text, font_type, size, color, duration, do_kill=True):
        super().__init__()
        self.image = pygame.Surface((size*8 + len(str(text)) * 4, size*8)).convert_alpha()
        self.image.set_colorkey('black')
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        # The text
        self.text = str(text)
        self.cur_text = self.text
        self.font_type = font_type
        self.size = size
        self.color = color
        self.font = pygame.font.Font(self.font_type, self.size)
        self.rendered = self.font.render(str(self.text), 0, self.color)
        self.rendered_rect = self.rendered.get_rect(center=(self.image.get_width()/2, self.image.get_height()/2))
        self.image.blit(self.rendered, self.rendered_rect)

        # For fading effect
        self.fade_delay = duration
        self.fade_timer = pygame.time.get_ticks()
        self.alpha = 255
        self.do_kill = do_kill # If the sprite gets deleted if it has faded

    def update(self):
        self.fade()

        if self.alpha <= 0 and self.do_kill == True:
            self.kill()

    def fade(self):
        now = pygame.time.get_ticks()
        if now - self.fade_timer > self.fade_delay:
            self.alpha -= 10
            self.image.set_alpha(self.alpha)

    def unfade(self):
        self.alpha = 255
        self.image.set_alpha(self.alpha)

class Bubble(pygame.sprite.Sprite):
    def __init__(self, win_size, colors):
        super().__init__()
        self.color = choice(colors)
        self.size = randrange(8,32)
        self.image = pygame.Surface((self.size,self.size)).convert_alpha()
        self.image.fill(BG_COLOR)
        self.img_width = self.image.get_width()
        self.img_height = self.image.get_height()
        self.alpha = 0
        self.alpha_change = randrange(5,10)
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect()
        self.rect.x = randrange(0, win_size[0])
        self.rect.y = randrange(0, win_size[1])
        self.spdy = randrange(-2, -1)
        self.is_fading = False
        pygame.draw.rect(self.image, self.color, (0,0,self.img_width,self.img_height), choice([0,8]))
        
    def update(self):
        if self.alpha <= 0 and self.is_fading:
            self.kill()

        self.rect.y += self.spdy
        self.fade()

    def fade(self):
        if not self.is_fading:
            self.alpha += self.alpha_change
            if self.alpha >= 255:
                self.is_fading = True
        else:
            self.alpha -= self.alpha_change
        self.image.set_alpha(self.alpha)

class KFKey(pygame.sprite.Sprite):
    def __init__(self, text, x, y, K_SIZE, color, font_name, shape, speed):
        super().__init__()
        self.color = color
        self.K_SIZE = K_SIZE
        self.shape = shape
        self.speed = speed

        # For surface
        self.image = pygame.Surface((self.K_SIZE,self.K_SIZE))
        self.img_width = self.image.get_width()
        self.img_height = self.image.get_height()
        self.image.fill(BG_COLOR)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        # For text
        self.text = text
        self.font = pygame.font.Font(font_name, self.K_SIZE//2)
        self.hide_timer = pygame.time.get_ticks()
        self.hide_delay = 500
        self.alpha = 255
        self.pressed = False
        
        # For moving arc animation
        self.animate_timer = pygame.time.get_ticks()
        self.animate_delay = 50
        self.ca = 0 # current arc config
        self.arcs_config = [
            [1,0,0,1],
            [1,1,0,0],
            [0,1,1,0],
            [0,0,1,1]
        ]
        self.arcs = self.arcs_config[0]
        self.i = 0
        
    def update(self):
        if self.pressed:
            self.hide()

        if self.alpha <= 0 or self.rect.top > WIN_SZ[1]:
            self.kill()

        self.rect.y += self.speed
        self.redraw()

    def hide(self):
        now = pygame.time.get_ticks()
        if now - self.hide_timer > self.hide_delay:
            self.alpha -= 20
            self.image.set_alpha(self.alpha)

    def update_arc(self):
        now = pygame.time.get_ticks()
        if now - self.animate_timer > self.animate_delay:
            self.animate_timer = now

            if self.ca >= len(self.arcs_config) - 1:
                self.ca = 0
            else:
                self.ca += 1

            self.arcs = self.arcs_config[self.ca]

    def redraw(self):
        self.image.fill(BG_COLOR)

        if self.shape == "rect":
            pygame.draw.rect(self.image, self.color, (0,0,self.img_width,self.img_height), 8)
        elif self.shape == "roundrect":
            pygame.draw.rect(self.image, self.color, (0,0,self.img_width,self.img_height), 4, 8)
        elif self.shape == "round":
            pygame.draw.rect(self.image, self.color, (0,0,self.img_width,self.img_height), 4, 32)
        elif self.shape == "arc":
            pygame.draw.circle(self.image, self.color, (self.image.get_width()/2, self.image.get_height()/2), 
                               16, 5, self.arcs[0], self.arcs[1], self.arcs[2], self.arcs[3])
            self.update_arc()

        self.r_font = self.font.render(self.text, 0, self.color)
        self.image.set_colorkey(BG_COLOR)
        self.image.blit(self.r_font, (9,8))