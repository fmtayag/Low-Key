# Discontinued for the time being...maybe even forever
# class KeyfallGameScene(Scene):
#     # Still brainstorming. The gameplay isn't fun currently.
#         # TODO
#         # 1. Add a "bomb" key that destroys keys in its blast zone
#         # 2. Add a way to check if a key has crossed "the line"
#     def __init__(self):

#         # Game variables
#         self.score = 0
#         self.offset = repeat((0,0)) # For screen shake
#         self.is_paused = False
#         self.enemy_count = 0
#         self.the_line = WIN_SZ[1] / 1.25
#         self.bparticles_colors = [(255,0,0), (255,20,10), (255,75,80)]
#         self.lives = 10

#         # Keys
#         self.color = PALETTE["CYAN"]
#         self.color_palette = PALETTE["CYAN_PAL"]
#         self.key_shape = "roundrect" # rect, roundrect, round, arc
#         self.K_SIZE = 32 # key size
#         self.letters = "QWERTYUIOPASDFGHJKLZXCVBNM"
#         self.letters = [char for char in self.letters]
#         self.chars = list()

#         # Sprite groups
#         self.sprites = pygame.sprite.Group()
#         self.key_sprites = pygame.sprite.Group()
#         self.particles = pygame.sprite.Group()
#         self.bubbles = pygame.sprite.Group()
#         self.blasts = pygame.sprite.Group()

#         # Texts
#         self.text_score = PulsatingText(WIN_SZ[0]/2, WIN_SZ[1]/1.1, self.score, GAME_FONT, 64, PALETTE["WHITE"])
#         self.sprites.add(self.text_score)

#     def handle_events(self, events):
#         for event in events:
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     self.is_paused = not self.is_paused
#                 if event.key == pygame.K_x and self.is_paused:
#                     self.manager.go_to(TitleScene())

#         if not self.is_paused:
#             # Get pressed characters
#             keys_pressed = list()
#             scan = pygame.key.get_pressed()
#             self.chars[:] = []
#             if 1 in list(scan):
#                 for i in range(len(list(scan))):
#                     if scan[i] == 1:
#                         keys_pressed.append(i)
#                 self.chars = [chr(i) for i in keys_pressed] # note: spacebar ascii conversion is ' '
    
#         #print(self.chars)

#     def update(self):
#         if not self.is_paused:

#             if self.lives <= 0:
#                 self.manager.go_to(GameOverScene(self.score))

#             # Act on key presses
#             if len(self.chars) != 0:
#                 for sprite in self.key_sprites:
#                     if sprite.text.lower() in self.chars and not sprite.pressed and sprite.rect.bottom > 0:
#                         sprite.hide()
#                         sprite.pressed = True
#                         sprite.speed = 0

#                         # Add score
#                         self.score += 1
#                         self.text_score.text = self.score

#                         if not sprite.is_bomb:
#                             s = Shockwave(sprite.rect.centerx, sprite.rect.centery, self.color, self.K_SIZE)
#                             spawn_particles(self.sprites, self.particles, sprite.rect.centerx, sprite.rect.centery, self.color_palette, 2)
#                             self.sprites.add(s)
#                         else:
#                             spawn_particles(self.sprites, self.particles, sprite.rect.centerx, sprite.rect.centery, self.bparticles_colors, 8)
#                             b = Blast(sprite.rect.centerx,sprite.rect.centery)
#                             self.sprites.add(b)
#                             self.blasts.add(b)

#                         self.offset = shake(10,5)
                        
#                         self.chars = list()
#                         break
            
#             # Check for blast collisions
#             hits = pygame.sprite.groupcollide(self.key_sprites, self.blasts, False, False, pygame.sprite.collide_circle)
#             for hit in hits:
#                 spawn_particles(self.sprites, self.particles, hit.rect.centerx, hit.rect.centery, self.color_palette, 8)
#                 self.offset = shake(15,5)
#                 hit.kill()
#                 self.score += 1
#                 self.text_score.text = self.score

#                 if hit.is_bomb:
#                     spawn_particles(self.sprites, self.particles, hit.rect.centerx, hit.rect.centery, self.bparticles_colors, 8)
#                     b = Blast(hit.rect.centerx, hit.rect.centery)
#                     self.sprites.add(b)
#                     self.blasts.add(b)

#             # Check for keys that have passed over the line
#             for sprite in self.key_sprites:
#                 if sprite.rect.bottom > self.the_line:
#                     if not sprite.is_bomb:
#                         spawn_particles(self.sprites, self.particles, sprite.rect.centerx, sprite.rect.centery, self.color_palette, 8)
#                         s = Shockwave(sprite.rect.centerx, sprite.rect.centery, self.color, self.K_SIZE)
#                         self.sprites.add(s)
#                     else:
#                         spawn_particles(self.sprites, self.particles, sprite.rect.centerx, sprite.rect.centery, self.bparticles_colors, 8)
#                         b = Blast(sprite.rect.centerx, sprite.rect.centery)
#                         self.sprites.add(b)
#                         self.blasts.add(b)
#                     self.offset = shake(15,5)
#                     self.lives -= 2
#                     sprite.kill()

#             # Spawn bubbles
#             if len(self.bubbles) <= self.score // 50 and len(self.bubbles) <= 20:
#                 b = Bubble(WIN_SZ, PALETTE["CYAN_PAL"])
#                 self.sprites.add(b)
#                 self.bubbles.add(b)        

#             # Spawn key ================
#             self.enemy_count = 5 + self.score // 30
#             if self.enemy_count > 15:
#                 self.enemy_count = 15

#             if len(self.key_sprites) < self.enemy_count:
#                 is_bomb = choices([True, False], weights=[1,9])[0]
#                 has_duplicate = False
#                 speed = choices([1,2,3,4], weights=[8,8,8,2])[0]
#                 k = KFKey(choice(self.letters), randrange(32, WIN_SZ[0]-32), randrange(-256,-32), self.K_SIZE, self.color, GAME_FONT, self.key_shape, speed, is_bomb)

#                 for sprite in self.key_sprites:
#                     if sprite.text.lower() == k.text.lower():
#                         has_duplicate = True

#                 # Prevent overlapping sprites
#                 if not has_duplicate and not pygame.sprite.spritecollide(k, self.key_sprites, True):
#                     self.sprites.add(k)
#                     self.key_sprites.add(k)

#             self.sprites.update()

#     def draw(self, window):
#         if not self.is_paused:
#             window.fill(BG_COLOR)
#             pygame.draw.line(window, PALETTE["WHITE"], (0,self.the_line), (WIN_SZ[0],self.the_line), self.lives)
#             self.bubbles.draw(window)
#             self.sprites.draw(window)
#             window.blit(window, next(self.offset))
#             self.sprites.draw(window)
#         else:
#             self.paused_texts.draw(window)