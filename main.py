import pygame
import os
import random
import datetime

pygame.init()
pygame.font.init()
pygame.mixer.init()

screenWidth = 800
screenHeight = 600
screenResolution = (screenWidth, screenHeight)
screen = pygame.display.set_mode(screenResolution)
pygame.display.set_caption("Board Smasher")

name = "Francis"
score = 0
time = 10000
warmupTime = 6000
timeAddTick = 0

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

scoreFont = pygame.font.Font("./Font/actionj.ttf", 128)
timeFont = pygame.font.Font("./Font/actionj.ttf", 64)
timeAddFont = pygame.font.Font("./Font/actionj.ttf", 32)
keysPressedFont = pygame.font.Font("./Font/actionj.ttf", 64)
gameOverFont = pygame.font.Font("./Font/actionj.ttf", 64)
nameEntryFont = pygame.font.Font("./Font/actionj.ttf", 32)
genericLargeFont = pygame.font.Font("./Font/actionj.ttf", 64)
genericSmallFont =  pygame.font.Font("./Font/actionj.ttf", 32)

keysList = [""]
nameList = [""]
currentKey = 0
displayName = ''
keysListPointer = 0
keysPressed = 0
keysPressedTick = 1000
startLoop = True
startLoopEnd = False
noEntryErrorTick = 0
gameLoop = False
forbiddenKeysList = [pygame.K_LSHIFT, pygame.K_RSHIFT] #TODO
clock = pygame.time.Clock()
FPS = 1000

while startLoop:
    clock.tick(FPS)
    logoDisplay = genericLargeFont.render("Board Smasher", False, BLACK)
    nameEntryDisplay = nameEntryFont.render(displayName, False, BLACK)
    enterNameDisplay = genericSmallFont.render("Enter Name:", False, BLACK)
    timeDisplay = genericSmallFont.render("Get Ready! " + str(round(warmupTime / 1000, 2)), False, BLACK)
    noEntryErrorDisplay = genericSmallFont.render("Please enter a name!", False, BLACK)
    #print(len(nameList))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            startLoop = False

        if event.type == pygame.KEYDOWN:

            noEntryErrorTick = 0
            
            if event.key != pygame.K_BACKSPACE and len(nameList) <= 12 and warmupTime >= 6000 and chr(event.key).isalnum() and event.key not in forbiddenKeysList:
                nameList.append(chr(event.key))
                displayName = ''.join(nameList)

            elif event.key == pygame.K_BACKSPACE and warmupTime >= 6000 and len(nameList) != 0:
                nameList.pop()
                displayName = ''.join(nameList)

            if event.key == pygame.K_RETURN and len(nameList) > 1:
                startLoopEnd = True

            if event.key == pygame.K_RETURN and len(nameList) <= 1:
                noEntryErrorTick = 2000

    screen.fill(WHITE)
    screen.blit(logoDisplay, (screenWidth / 2 - 256, 64))
    screen.blit(enterNameDisplay, (screenWidth / 2 - 108, 300))
    screen.blit(nameEntryDisplay, (screenWidth / 2 - 108, 350))

    if startLoopEnd == True:
        warmupTime -= 1
        screen.blit(timeDisplay, (screenWidth / 2 - 108, 400))

        if warmupTime == 0:
            startLoop = False
            gameLoop = True

    if noEntryErrorTick > 0:
        noEntryErrorTick -= 1
        screen.blit(noEntryErrorDisplay, (screenWidth / 2 - 108, 350))
        
    pygame.display.update()

while gameLoop:
    clock.tick(FPS)
    time -= 1
    keysPressedTick -= 1
    widthOffset = 64
    time_added = 5 - ((score + (time/10)) / 1000)
    
    scoreDisplay = scoreFont.render(str(score), False, BLACK)
    timeDisplay = timeFont.render(str(round(time / 1000, 2)), False, BLACK)
    timeAddDisplay = timeAddFont.render("+Time!",  False, BLACK)
    keysPressedDisplay = keysPressedFont.render(keysList[keysListPointer], False, BLACK)
    gameOverDisplay = gameOverFont.render("GAME OVER!", False, BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameLoop = False
        if event.type == pygame.KEYDOWN:
            score += 1
            keysList.append(str(chr(event.key)))
            keysListPointer += 1

            if score % 100 == 0 and score != 0 and time_added >= 1.5:
                time += time_added * 1000
                timeAddTick = 1000
                print(time_added)

            elif score % 100 == 0 and score != 0 and time_added <= 1.5:
                time += 1500
                timeAddTick = 1000
                print("Using default 1.5 time")
        
    if score >= 100:
        widthOffset = 108

    if score >= 1000:
        widthOffset = 160

    if score >= 10000:
        widthOffset = 192
        
    screen.fill(WHITE)

    if timeAddTick > 0:
        screen.blit(timeAddDisplay, (0, 64))
        timeAddTick -= 1
        
    screen.blit(timeDisplay, (0, 0))
    screen.blit(scoreDisplay, (screenWidth / 2 - widthOffset, screenHeight / 2 - 64))
    screen.blit(keysPressedDisplay, (screenWidth - 64, screenHeight - 64))

    if time <= 0:
        currentdate = datetime.date.today().strftime("%B") + " " + datetime.date.today().strftime("%d") + " " + datetime.date.today().strftime("%Y")
        screen.blit(gameOverDisplay, (screenWidth / 2 - 200, screenHeight / 2 - 128))
        pygame.display.update()
        highscores = open("highscores.txt", "a")
        highscores.write(''.join(nameList) + " | " + str(score) + " | " + str(currentdate) + "\n")
        highscores.close()
        
        pygame.time.wait(3000)
        gameLoop = False

    pygame.display.update()

pygame.quit()
quit()

