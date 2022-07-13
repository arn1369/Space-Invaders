import pygame
from random import choice

def create_star():
    path = choice('assets/star1.png', 'assets/star2.png', 'assets/star3.png')
    _img = pygame.image.load(path)
