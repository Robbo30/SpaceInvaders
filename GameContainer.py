import pygame, random
from Player import Spaceship
from Obstacle import Barrier
from Obstacle import grid
from Aliens import Alien
from Lasers import Laser
from Aliens import MysteryShip

#defines all variables
class Game:
    def __init__(self, screenWidth, screenHeight, offset):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.Offset = offset
        self.spaceshipGroup = pygame.sprite.GroupSingle()
        self.spaceshipGroup.add(Spaceship(self.screenWidth, self.screenHeight, self.Offset))
        self.obstacles = self.createObstacles()
        self.alienGroup = pygame.sprite.Group()
        self.createAliens()
        self.alienDirection = 1
        self.alienLaserGroup = pygame.sprite.Group()
        self.mysteryShipGroup = pygame.sprite.GroupSingle()
        self.lives = 3
        self.run = True
        self.score = 0
        self.highScore = 0
        self.loadHighScore()
        pygame.mixer.music.load("Arcade Game Music Type Beat (RDCworld1 Outro) [TubeRipper.com].ogg")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        self.explosion_sound = pygame.mixer.Sound("Sounds_explosion.ogg")
        self.explosion_sound.set_volume(0.2)
        self.numOfAliens = 0

    #function to creates the obstacles with the same gap between all 4
    def createObstacles(self):
        obstacle_width = len(grid[0]) * 3
        gap = (self.screenWidth + self.Offset - (4 * obstacle_width)) / 5
        obstacles = []
        for i in range(4):
            xOffset = (i + 1) * gap + i * obstacle_width
            obstacle = Barrier(xOffset, self.screenHeight - 100)
            obstacles.append(obstacle)
        return obstacles
    
    #function to spawns in the aliens in organised rows
    def createAliens(self):
        for row in range(5):
            for column in range(11):
                x = 75 + column * 55
                y = 110 + row * 55
                if row == 0:
                    alien_type = 3
                elif row in (1,2):
                    alien_type = 2
                else:
                    alien_type = 1

                alien = Alien(alien_type, x + self.Offset / 2, y)
                self.alienGroup.add(alien)

    #function to move the aliens
    def alienMovement(self):
        self.alienGroup.update(self.alienDirection)

        alien_sprites = self.alienGroup.sprites()
        for alien in alien_sprites:
            if alien.rect.right >= self.screenWidth + self.Offset / 2:#when they hit a wall they move down
                self.alienDirection = -1
                self.alienMoveDown(2)
            elif alien.rect.left <= self.Offset / 2:
                self.alienDirection = 1
                self.alienMoveDown(2)
                
    #function to move the aliens down 
    def alienMoveDown(self, distance):
        if self.alienGroup:
            for alien in self.alienGroup.sprites():
                alien.rect.y += distance

    #function to make the aliens shoot randomly
    def shootAlienLaser(self):
        if self.alienGroup.sprites():
            random_alien = random.choice(self.alienGroup.sprites())
            laser_sprite = Laser(random_alien.rect.center, -6, self.screenHeight)
            self.alienLaserGroup.add(laser_sprite)

    #function to spawn in the mystery ship
    def createMysteryShip(self):
        self.mysteryShipGroup.add(MysteryShip(self.screenWidth, self.Offset))

    #function to constantly check for a collision and act upon it 
    def checkForCollisions(self):
        if self.spaceshipGroup.sprite.laserGroup:
            for laser_sprite in self.spaceshipGroup.sprite.laserGroup:

                aliens_hit = pygame.sprite.spritecollide(laser_sprite, self.alienGroup, True)
                if aliens_hit:
                    self.explosion_sound.play()
                    for alien in aliens_hit:
                        self.score = self.score + alien.type * 100#adds score to the score each kill
                        self.checkForHighScore()
                        laser_sprite.kill()
                        self.numOfAliens = self.numOfAliens - 1

                aliens_hit = pygame.sprite.spritecollide(laser_sprite, self.mysteryShipGroup, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score = self.score + 600
                        self.explosion_sound.play()
                        self.checkForHighScore()
                        laser_sprite.kill()
                        self.numOfAliens = self.numOfAliens - 1

                for obstacle in self.obstacles:
                        if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
                            laser_sprite.kill()#kills each section of the obstacle hit

        
                    
        if self.alienLaserGroup:#checks if lives are 0 
            for laser_sprite in self.alienLaserGroup:
                if pygame.sprite.spritecollide(laser_sprite, self.spaceshipGroup, False):
                    laser_sprite.kill()
                    self.lives -= 1
                    if self.lives == 0:
                        self.gameOver()
                
                for obstacle in self.obstacles:
                        if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
                            laser_sprite.kill()
        
        if self.alienGroup:
            for alien in self.alienGroup:
                for obstacle in self.obstacles:
                    pygame.sprite.spritecollide(alien, obstacle.blocks_group, True)

                if pygame.sprite.spritecollide(alien, self.spaceshipGroup, False):
                    self.gameOver()

    #function to end the game
    def gameOver(self):
        self.run = False

    #function to reset all attributes
    def reset(self):
        self.run = True
        self.lives = 3
        self.spaceshipGroup.sprite.reset()
        self.alienGroup.empty()
        self.alienLaserGroup.empty()
        self.createAliens()
        self.mysteryShipGroup.empty()
        self.obstacles = self.createObstacles()
        self.score = 0 

    #function to update and store the highscore
    def checkForHighScore(self):
        if self.score > self.highScore:
            self.highScore = self.score

            with open("highscore.txt", "w") as file:
                file.write(str(self.highScore))
    
    #function to load the highscore to be displayed
    def loadHighScore(self):
        try:
            with open("highscore.txt", "r") as file:
                self.highScore = int(file.read())
        except FileNotFoundError:
            self.highScore = 0





        
