import pygame
from random import randrange, choice, choices
from data.scripts.constants import *

class Key(pygame.sprite.Sprite):
    def __init__(self, text, x, y, K_SIZE, color, font):
        super().__init__()
        self.color = color
        self.K_SIZE = K_SIZE
        self.image = pygame.Surface((self.K_SIZE,self.K_SIZE))
        self.image.fill(BG_COLOR)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.text = text
        self.font = pygame.font.Font(font, self.K_SIZE//2)
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

class Shockwave(pygame.sprite.Sprite):
    def __init__(self, x, y, color, K_SIZE):
        super().__init__()
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
        if self.radius >= self.img_width / 2:
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

class PulsatingText(pygame.sprite.Sprite):
    def __init__(self, x, y, text, font_type, size, color):
        super().__init__()
        self.image = pygame.Surface((size*8,size*8)).convert_alpha()
        self.image.set_colorkey('black')
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        # The text
        self.text = text
        self.cur_text = self.text
        self.font_type = font_type
        self.size = size
        self.orig_size = self.size
        self.color = PALETTE[color]
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
        self.size = 64

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