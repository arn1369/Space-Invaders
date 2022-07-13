import pygame
from data import *
from random import randint

#TODO: shootin'

class Enemy(pygame.sprite.Sprite):
    def __init__(self, health: float=100, speed: float=1, pos: tuple=(0, 0), type_: str='SecondClass'):
        # general init
        super().__init__()
        self.health = health
        self.speed = speed
        # image and type of enemy
        match type_:
            case 'FirstClass':
                self.image = pygame.image.load('assets/red.png').convert_alpha()
            case 'SecondClass':
                self.image = pygame.image.load('assets/yellow.png').convert_alpha()
        # create image and rect for the enemy
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
    
    def die(self):
        pygame.sprite.Sprite.kill(self)

    def update(self):
        # move the enemy to the bottom of the screen
        self.rect.y += self.speed
        # if enemy reach the borders of the screen
        if self.rect.y > SCREEN_HEIGHT-self.image.get_height():
            self.rect.x, self.rect.y = randint(0, SCREEN_WIDTH-100), randint(0, SCREEN_HEIGHT/3)
        elif self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.x > SCREEN_WIDTH-self.image.get_width():
            self.rect.x = SCREEN_WIDTH-self.image.get_width()
        elif self.rect.x < 0:
            self.rect.x = 0