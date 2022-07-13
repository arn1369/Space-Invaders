import pygame
from data import *
from random import randint

#TODO: shoot

class Boss(pygame.sprite.Sprite):
    def __init__(self, health : int, attack : int, pos : tuple, type_ : str, speed : int):
        super().__init__()
        self.health = health
        self.speed = speed
        self.attack = attack
        self.type_ = type_
        self.image = pygame.image.load('assets/red.png')
        self.rect = self.image.get_rect(midbottom=pos)
        # movement
        self.boss_time = 0
        self.boss_cooldown = 75
        self.is_ready = True

    def move(self):
        assert self.health > 0
        self.rect.x += randint(-self.speed, self.speed)
        self.rect.y += randint(-self.speed, self.speed)
    
    def die(self):
        pygame.sprite.Sprite.kill(self)
    
    def wait_time(self):
        if not self.is_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.boss_time >= self.boss_cooldown:
                self.is_ready = True
    
    def update(self):
        # is boss dead ?
        if self.health <= 0:
            self.health = 0
            self.die()
            return
        # stay in the screen
        if self.rect.x >= SCREEN_WIDTH:
            self.rect.x = SCREEN_WIDTH
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.y >= SCREEN_HEIGHT or self.rect.y <= 0:
            self.rect.y = 0
        # reload movement
        self.wait_time()
        if self.is_ready:
            self.is_ready = False
            self.boss_time = pygame.time.get_ticks()
            # move the boss
            self.move()

