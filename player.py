import pygame
from data import *

#TODO: better shooting (rect, etc.)

class Player(pygame.sprite.Sprite):
    class Ammo(pygame.sprite.Sprite):
        def __init__(self, speed: float, attack: float, pos: tuple):
            super().__init__()
            self.speed = speed
            self.attack = attack
            # draw the rectangle
            self.image = pygame.transform.scale(pygame.image.load('assets/green.png').convert_alpha(), (AMMO_SIZE, AMMO_SIZE))
            self.rect = self.image.get_rect(midbottom=pos)

        def die(self):
            # kill the player
            pygame.sprite.Sprite.kill(self)
        
        def update(self):
            # move the ammo
            self.rect.y -= self.speed

    def __init__(self, health: float, speed : float, pos: tuple, attack: float):
        super().__init__()
        # data
        self.health = health
        self.speed = speed
        self.attack = attack
        # sprite
        self.image = pygame.image.load('assets/player.png')
        self.rect = self.image.get_rect(midbottom=pos)
        self.ammo_group = pygame.sprite.Group()
        # setup shoot
        self.is_ready = True
        self.laser_time = 0
        self.laser_cooldown = 600

    def reload(self):
        if not self.is_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.is_ready = True

    
    def shoot(self):
        # spawn ammo
        self.ammo_group.add(self.Ammo(5, self.attack, (self.rect.x+self.image.get_width()/2, self.rect.y)))
            
    def update(self):
        # move
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        # in the screen
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        # shoot
        elif keys[pygame.K_a] and self.is_ready:
            self.is_ready = False
            self.laser_time = pygame.time.get_ticks()
            self.shoot()
        # reload
        self.reload()
        # move the ammo
        if self.ammo_group != None:
            self.ammo_group.update()