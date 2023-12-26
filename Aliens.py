import pygame, random

class Alien(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__()
        self.type = type
        path = f"D:\Pygame Images\SpaceRaiders\Alien{type}.png"
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(topleft = (x,y))

    def update(self, direction):
        self.rect.x += direction

class MysteryShip(pygame.sprite.Sprite):
    def __init__(self, screenWidth, offset):
        super().__init__()
        self.Offset = offset
        self.image = pygame.image.load("D:\Pygame Images\SpaceRaiders\MysteryShip.png")
        self.screenWidth = screenWidth

        x = random.choice([self.Offset / 2, self.screenWidth + self.Offset - self.image.get_width()])
        if x == self.Offset / 2:#sets the speed and changes it when the wall is hit
            self.speed = 3
        else:
            self.speed = -3

        self.rect = self.image.get_rect(topleft = (x, 90))

    def update(self):#function to update all attributes
        self.rect.x += self.speed
        if self.rect.right > self.screenWidth + self.Offset / 2:
            self.kill()
        elif self.rect.left < self.Offset / 2:
            self.kill()