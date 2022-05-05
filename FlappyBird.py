import pygame
import sys
import random

def drawFloor():
    screen.blit(floorSurface, (floorXPos, 450))
    screen.blit(floorSurface, (floorXPos + 288, 450))

def createPipe():
    randomPipePos = random.choice(pipeHeights)
    bottomPipe = pipeSurface.get_rect(midtop = (350, randomPipePos)) # The size is half of the screen's dimension
    topPipe =  pipeSurface.get_rect(midbottom = (350, randomPipePos - 150))
    return bottomPipe, topPipe

def movePipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2.5
    return pipes

def drawPipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipeSurface, pipe)
        else:
            flipPipe = pygame.transform.flip(pipeSurface, False, True) # If the pipe is at the top of the screen, flip it, because the pipe image has only 1 direction.
            screen.blit(flipPipe, pipe)

def checkCollision(pipes):
    for pipe in pipes:
        if birdRect.colliderect(pipe):
            deathSound.play()
            return False

    if birdRect.top <= -50 or birdRect.bottom >= 450:
        return False

    return True

def rotateBird(bird):
    newBird = pygame.transform.rotozoom(bird, -birdMovement * 3, 1)
    return newBird

def birdAnimation():
    newBird = birdFrames[birdIndex]
    newBirdRect = newBird.get_rect(center = (50, birdRect.centery))
    return newBird, newBirdRect

def scoreDisplay(gameState):
    if gameState == 'main_game':
        scoreSurface = gameFont.render(str(int(score)), True, (255, 255, 255))
        scoreRect = scoreSurface.get_rect(center = (144, 50))
        screen.blit(scoreSurface, scoreRect)

    if gameState == 'game_over':
        # Current Score at the top of the screen
        scoreSurface = gameFont.render(f'Score: {int(score)}', True, (255, 255, 255))
        scoreRect = scoreSurface.get_rect(center = (144, 50))
        screen.blit(scoreSurface, scoreRect)
        # High Score at the bottom of the screen
        highScoreSurface = gameFont.render(f'High Score: {int(highScore)}', True, (255, 255, 255))
        highScoreRect = highScoreSurface.get_rect(center = (144, 425))
        screen.blit(highScoreSurface, highScoreRect)

def updateScore(score, highScore):
    if score > highScore:
        highScore = score
    return highScore

pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512) #####
pygame.init()
screen = pygame.display.set_mode((288, 512)) # The dimensions of the game background
clock = pygame.time.Clock() # Limit our game frame
gameFont = pygame.font.SysFont('04B_19.ttf', 40) # Used to add text 

# Game Variables
gravity = 0.25
birdMovement = 0 # Moves the birdRect down
gameActive = True
score = 0
highScore = 0

bgSurface = pygame.image.load('assets/images/backgrounds/background-day.png').convert() # The background of the game screen
#bgSurface = pygame.transform.scale2x(bgSurface) # Make the above image fit into the game screen by changing the scale of the image if needed

floorSurface = pygame.image.load('assets/images/environment/base.png').convert()
#floorSurface = pygame.transform.scale2x(floorSurface)
floorXPos = 0

'''
birdDownflap = pygame.transform.scale2x(pygame.image.load('assets/images/birds/blue/bluebird-downflap.png').convert_alpha())
birdMidflap = pygame.transform.scale2x(pygame.image.load('assets/images/birds/blue/bluebird-midflap.png').convert_alpha())
birdUpflap = pygame.transform.scale2x(pygame.image.load('assets/images/birds/blue/bluebird-upflap.png').convert_alpha())
'''
birdDownflap = pygame.image.load('assets/images/birds/blue/bluebird-downflap.png').convert_alpha()
birdMidflap = pygame.image.load('assets/images/birds/blue/bluebird-midflap.png').convert_alpha()
birdUpflap = pygame.image.load('assets/images/birds/blue/bluebird-upflap.png').convert_alpha()
birdFrames = [birdDownflap, birdMidflap, birdUpflap]
birdIndex = 0
birdSurface = birdFrames[birdIndex]
birdRect = birdSurface.get_rect(center = (50, 256))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

'''
birdSurface = pygame.image.load('assets/images/birds/blue/bluebird-midflap.png').convert()
#birdSurface = pygame.transform.scale2x(floorSurface)
birdRect = birdSurface.get_rect(center = (50, 256))
'''

pipeSurface = pygame.image.load('assets/images/environment/pipe-green.png').convert()
#pipeSurface = pygame.transform.scale2x(floorSurface)
pipeList = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200) # 1200ms
pipeHeights = [200, 300, 400]

gameOverSurface = pygame.image.load('assets/images/messages/message.png').convert_alpha()
#gameOverSurface = pygame.transform.scale2x(gameOverSurface)
gameOverRect = gameOverSurface.get_rect(center = (144, 256))

flapSound = pygame.mixer.Sound('assets/sounds/wing.wav')
deathSound = pygame.mixer.Sound('assets/sounds/hit.wav')
scoreSound = pygame.mixer.Sound('assets/sounds/point.wav')
scoreSoundCountdown = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() # Make sure that we have exitted completely
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and gameActive:
                birdMovement = 0
                birdMovement -= 6
                flapSound.play()
            if event.key == pygame.K_SPACE and gameActive == False:
                gameActive = True
                pipeList.clear()
                birdRect.center = (50, 256)
                birdMovement = 0
                score = 0 # Reset the score after each game loop
        if event.type == SPAWNPIPE:
            pipeList.extend(createPipe())
        if event.type == BIRDFLAP:
            if birdIndex < 2:
                birdIndex += 1
            else:
                birdIndex = 0
            birdSurface, birdRect = birdAnimation()
    
    screen.blit(bgSurface, (0, 0)) # The background is not gonna appear until we have this line

    if gameActive:
        # Bird
        birdMovement += gravity
        rotatedBird = rotateBird(birdSurface)
        birdRect.centery += birdMovement
        screen.blit(rotatedBird, birdRect)
        gameActive = checkCollision(pipeList)
        # Pipes
        pipeList = movePipes(pipeList)
        drawPipes(pipeList)
        # Score
        score += 0.01
        scoreDisplay('main_game')
        scoreSoundCountdown -= 1
        if scoreSoundCountdown <= 0:
            scoreSound.play()
            scoreSoundCountdown = 100
    else:
        screen.blit(gameOverSurface, gameOverRect)
        highScore = updateScore(score, highScore)
        scoreDisplay('game_over')

    # Floor
    floorXPos -= 1
    drawFloor()
    if floorXPos <= -288:
        floorXPos = 0
    
    pygame.display.update()
    clock.tick(100) # The game never runs faster than 120 frames/sec