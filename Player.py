import pygame
from Lasers import Laser

#defining all variables 
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, screenWidth, screenHeight, offset):
        super().__init__()
        self.Offset = offset
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.image = pygame.image.load("D:\Pygame Images\SpaceRaiders\Spaceship.png")
        self.rect = self.image.get_rect(midbottom = ((self.screenWidth + self.Offset) / 2, self.screenHeight))
        self.speed = 6
        self.laserGroup = pygame.sprite.Group()
        self.isLaserReady = True
        self.timeOfLaser = 0
        self.laserDelay = 300
        self.laserSound = pygame.mixer.Sound("Sounds_laser.ogg")

    #function to determine the user inputs and act on the input
    def userInput(self):
        keyPressed = pygame.key.get_pressed()

        if keyPressed[pygame.K_RIGHT]:#move right
            self.rect.x += self.speed
        
        if keyPressed[pygame.K_LEFT]:#move left
            self.rect.x -= self.speed

        if keyPressed[pygame.K_SPACE] and self.isLaserReady:#shoot the laser 
            self.isLaserReady = False
            laser = Laser(self.rect.center, 5, self.screenHeight)
            self.laserGroup.add(laser)
            self.timeOfLaser = pygame.time.get_ticks()
            self.laserSound.play()
            self.laserSound.set_volume(0.2)

    #function to update all the laser variables
    def update(self):
        self.userInput()
        self.constrain_movement()
        self.laserGroup.update()
        self.recharge_laser()
    
    #function to stop moving off the screen
    def constrain_movement(self):
        if self.rect.right > self.screenWidth:
            self.rect.right = self.screenWidth
        if self.rect.left < self.Offset:
            self.rect.left = self.Offset

    #function to determine when the laser can be shot again
    def recharge_laser(self):
        if not self.isLaserReady:
            current_time = pygame.time.get_ticks()
            if current_time - self.timeOfLaser >= self.laserDelay:
                self.isLaserReady = True

    #function to reset the player position
    def reset(self):
        self.rect = self.image.get_rect(midbottom = ((self.screenWidth + self.Offset) / 2, self.screenHeight))
        self.laserGroup.empty()

