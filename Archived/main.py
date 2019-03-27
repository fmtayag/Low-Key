import pygame
pygame.init()
pygame.font.init()

### Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

### Font

score_font = pygame.font.Font("./Font/8-BIT WONDER.ttf", 32)
time_font = pygame.font.Font("./Font/8-BIT WONDER.ttf", 16)

### Screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Board Smasher!")

### Game variables
clock = pygame.time.Clock()
FPS = 60
time = 0

def warm_up():
    running = True
    time = 5000
    time_minus = 1
    while running:

        if time <= 0:
            running = False
        
        ready_label = time_font.render("Get Ready to SMASH YOUR KEYBOARD!", False, WHITE)
        time_label = time_font.render(str(round(time / 1000, 2)), False, WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)
        screen.blit(ready_label, ((800 / 2) - 16, 600 / 2))
        screen.blit(time_label, ((800 / 2) - 16, (600 / 2) + 50))

        pygame.display.update()
        time -= time_minus
    
def main_loop():
    running = True
    time = 10000
    time_minus = 1
    score = 0
    
    while running:
        clock.tick()
        time -= time_minus
        if time <= 0:
            print("STOP!")
            time_minus = 0
            pygame.time.wait(10000)

        score_board = score_font.render(str(score), False, WHITE)
        time_board = time_font.render(str(time / 1000), False, WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                score += 1

        screen.fill(BLACK)
        screen.blit(score_board, ((800 / 2) - 16, 600 / 2))
        screen.blit(time_board, (10, 10))

        pygame.display.update()

warm_up()
main_loop()

pygame.quit()
