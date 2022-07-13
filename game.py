import pygame, thorpy
from random import randint
from enemy import Enemy
from player import Player
from boss import Boss
from data import *
from sys import exit

#TODO: save score / high score

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1080, 720))
        pygame.display.set_caption("Asteroid Game")
        self.clock = pygame.time.Clock()
        self.background_img = pygame.transform.scale(pygame.image.load('assets/background.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))
        # score and font
        self.font = pygame.font.Font('assets/Score_Font.ttf', 50)
        self.mainfont = pygame.font.Font('assets/Score_Font.ttf', 200)
        self.start_button_padding = 100
        # load the scene
        self.load_scene()
    
    def load_scene(self):
        self.state = 'INIT'
        # background
        self.screen.blit(self.background_img, (0, 0))
        # player Single Group
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player(100, 5, (SCREEN_WIDTH/2, SCREEN_HEIGHT), 10))
        # Enemy Multiple Group
        self.enemy_group = pygame.sprite.Group()
        self.enemy_group.add(self.create_enemies(15))
        # score 
        self.score = 0
        # boss
        self.is_boss = False
        # state
        self.state = 'RUNNING'
        # main
        self.main()
    
    def main(self):
        while True:
            self.mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = 'MENU'
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == 'MENU':
                        if self.mouse_pos[0] in range(self.button_x, self.button_x_end) and self.mouse_pos[1] in range(self.button_y, self.button_y_end):
                            print("Button pressed.")
                            self.load_scene()
            # handle all states (menu, pause, game loop, boss)
            self.handle_states()

            # general update
            pygame.display.update()
            self.clock.tick(60)

    def loop(self):
        # fill with background
        self.screen.blit(self.background_img, (0, 0))
        # collisions
        self.handle_collisions()
        # player update
        self.player.draw(self.screen)
        self.player.sprite.ammo_group.draw(self.screen)
        self.player.update()
        # enemies update
        self.enemy_group.draw(self.screen)
        self.enemy_group.update()
        # display score
        self.display_score()
    
    def display_score(self):
        score_surface = self.font.render(f'score : {self.score}', False, 'lightblue')
        score_rect = score_surface.get_rect(topleft = (10, 10))
        self.screen.blit(score_surface, score_rect)

    def create_enemies(self, _nbr: int):
        # a list that contains all the enemies we want to add
        __enemies = []
        for _ in range(_nbr):
            # create an enemy at random position
            __enemy_pos = (randint(0, SCREEN_WIDTH-100), randint(0, SCREEN_HEIGHT/3))
            __enemies.append(Enemy(100, 1, __enemy_pos, 'SecondClass'))
        return __enemies

    def handle_collisions(self):
        # if the player is touched by an enemy, the game pauses.
        if pygame.sprite.spritecollide(self.player.sprite, self.enemy_group, False) or (self.is_boss and pygame.sprite.spritecollide(self.player.sprite, self.boss, False)):
            self.state = 'GAME OVER'
        # if an ammo kills an enemy, it spawns a new enemy
        if pygame.sprite.groupcollide(self.player.sprite.ammo_group, self.enemy_group, True, True):
            self.enemy_group.add(self.create_enemies(1))
            self.score += 1
            # check if we need to enter boss mode
            if self.score % 30 == 0 and self.score != 0:
                self.state = 'BOSS'
        if self.is_boss and pygame.sprite.groupcollide(self.player.sprite.ammo_group, self.boss, True, False):
            self.boss.sprite.health -= self.player.sprite.attack
            print(f"Boss has taken {self.player.sprite.attack} damages.")

    def handle_states(self):
        """This function handle all states and menus"""
        match self.state:
            case 'RUNNING':
                self.loop()
            case 'PAUSE':
                self.pause()
            case 'MENU':
                self.main_menu()
            case 'BOSS':
                if not self.is_boss:
                    self.call_boss()
                self.boss_loop()
            case 'VICTORY':
                self.victory()
            case 'GAME OVER':
                self.game_over()

    def pause(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            # reload the scene
            self.load_scene()
    
    def main_menu(self):
        self.screen.blit(self.background_img, (0, 0))
        # write start text
        start_surface = pygame.font.Font('assets/Score_Font.ttf', 100).render("New Game", False, 'lightblue')
        start_rect = start_surface.get_rect(center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-self.start_button_padding))
        self.screen.blit(start_surface, start_rect)
        # write best score text
        self.high_score = 100 # TO CHANGE LATER -> SAVING DATA
        score_surface = pygame.font.Font('assets/Score_Font.ttf', 40).render(f"Best Score : {self.high_score}", False, 'lightblue')
        score_rect = score_surface.get_rect(center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(score_surface, score_rect)
        # size of text
        self.button_x = SCREEN_WIDTH//2-start_surface.get_width()//2
        self.button_y = SCREEN_HEIGHT//2-start_surface.get_height()//2-self.start_button_padding
        self.button_x_end = SCREEN_WIDTH//2+start_surface.get_width()//2
        self.button_y_end = SCREEN_HEIGHT//2+start_surface.get_height()//2-self.start_button_padding
        
        
    def call_boss(self):
        assert not self.is_boss
        # clear all enemies
        for enemy in self.enemy_group:
            enemy.die()
        self.enemy_group.empty()
        # spawn the boss
        self.boss = pygame.sprite.GroupSingle()
        __boss_pos = (randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT/4))
        self.boss.add(Boss(100, 90, __boss_pos, 'Boss1', 15))
        self.is_boss = True

    def boss_loop(self):
        assert self.is_boss
        # fill with background
        self.screen.blit(self.background_img, (0, 0))
        # collisions
        self.handle_collisions()
        # player update
        self.player.draw(self.screen)
        self.player.sprite.ammo_group.draw(self.screen)
        self.player.update()
        # enemies update
        self.boss.draw(self.screen)
        self.boss.update()
        # display score
        self.display_score()
        # if the boss is dead
        if not self.boss:
            self.state = 'VICTORY'
            return
    
    def victory(self):
        self.screen.fill((150, 150, 150))
        # write victory text
        vic_surface = self.mainfont.render("Victory", False, 'lightblue')
        vic_rect = vic_surface.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.screen.blit(vic_surface, vic_rect)
        # restart the game
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.load_scene()
    
    def game_over(self):
        self.screen.fill((150, 150, 150))
        # write game over text
        over_surface = self.mainfont.render("Game Over", False, 'lightblue')
        over_rect = over_surface.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.screen.blit(over_surface, over_rect)
        # retart the game
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.load_scene()

game = Game()