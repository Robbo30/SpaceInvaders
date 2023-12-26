import pygame, sys, random
from GameContainer import Game

pygame.init()

#creates the screen with these dimensions
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700
OFFSET = 50

#colours for the game
GREY = (29, 29, 27)
BLUE = (31,206,203)
YELLOW = (243,216,63)

#creates the text to display on the screen
font = pygame.font.Font("Gametext.ttf", 40)
levelText = font.render("LEVEL 01", False, BLUE)
gameOverText = font.render("GAME OVER", False, BLUE)
scoreText = font.render("SCORE", False, BLUE)
highScoreText = font.render("HIGH SCORE", False, BLUE)

screen = pygame.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + 2 * OFFSET))
pygame.display.set_caption("Space Raiders")

clock = pygame.time.Clock()

game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET)

SHOOT_LASER = pygame.USEREVENT
pygame.time.set_timer(SHOOT_LASER, 300)

MYSTERYSHIP = pygame.USEREVENT + 1
pygame.time.set_timer(MYSTERYSHIP, random.randint(7000,15000))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SHOOT_LASER and game.run:
            game.shootAlienLaser() 

        if event.type == MYSTERYSHIP and game.run:
            game.createMysteryShip()
            pygame.time.set_timer(MYSTERYSHIP, random.randint(7000,15000))

        keyPressed = pygame.key.get_pressed()
        if keyPressed[pygame.K_SPACE] and game.run == False:
            game.reset()
        

    if game.run:
        game.spaceshipGroup.update()
        game.alienMovement()
        game.alienLaserGroup.update()
        game.mysteryShipGroup.update()
        game.checkForCollisions()

    screen.fill(GREY)

    pygame.draw.rect(screen, BLUE, (10, 10, 780, 780), 3, 0, 60, 60, 60, 60)
    pygame.draw.line(screen, BLUE, (25, 730), (775, 730), 3)

    if game.run:
        screen.blit(levelText,(620,740,35,50))
    else:
        screen.blit(gameOverText,(620,740,35,50))

    x = 50
    for life in range(game.lives):
        screen.blit(game.spaceshipGroup.sprite.image,(x, 745))
        x = x + 50
    
    screen.blit(scoreText, (50,25,50,50))
    formatted_score = str(game.score).zfill(5)
    score = font.render(formatted_score, False, BLUE)
    screen.blit(score, (50,50,50,50))
    screen.blit(highScoreText, (590,25,50,50))
    formatted_highScore = str(game.highScore).zfill(5)
    highScoreTextS = font.render(formatted_highScore, False, BLUE)
    screen.blit(highScoreTextS, (590,50,50,50))


    game.spaceshipGroup.draw(screen)
    game.spaceshipGroup.sprite.laserGroup.draw(screen)
    for obstacle in game.obstacles:
        obstacle.blocks_group.draw(screen)
    game.alienGroup.draw(screen)
    game.alienLaserGroup.draw(screen)
    game.mysteryShipGroup.draw(screen)
            
    pygame.display.update()
    clock.tick(60)

     
