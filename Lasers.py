import pygame

#defining all variables
class Laser(pygame.sprite.Sprite):
    def __init__(self, position, speed, screenHeight):
        super().__init__()
        self.image = pygame.Surface((4,15))#creating the laser rectangle
        self.image.fill((31,206,203))
        self.rect = self.image.get_rect(center = position)
        self.speed = speed
        self.screenHeight = screenHeight
    
    #function to update variables and kill the lasers 
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y > self.screenHeight + 15 or self.rect.y < 0:
            self.kill()
