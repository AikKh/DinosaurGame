import pygame
import random
import os
import time
import threading
import sys

WIDTH = 1200
HEIGHT = 750

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Cactuss(pygame.sprite.Sprite):

    images = []
    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'img')
    cactus_img_1 = pygame.image.load(os.path.join(img_folder, 'cactus3.png'))
    cactus_img_2 = pygame.image.load(os.path.join(img_folder, 'cactus3-2.png'))
    cactus_img_3 = pygame.image.load(os.path.join(img_folder, 'cactus3-3.png'))

    images.append(cactus_img_1)
    images.append(cactus_img_2)
    images.append(cactus_img_3)

    def __init__(self, img_index):
        self.img_index = img_index
        self.random_time = random.randrange(15, 25)
        pygame.sprite.Sprite.__init__(self)
        self.image = self.images[self.img_index]
        self.rect = self.image.get_rect()
        self.rect.center = (1300, 525)

    def cactusRush(self):
        self.rect.x -= 10
        
    def check(self):
        pass


class Dino(pygame.sprite.Sprite):

    images = []
    img_index = 0
    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'img')
    player_img = pygame.image.load(os.path.join(img_folder, 'dino.png'))
    player_dead = pygame.image.load(os.path.join(img_folder, 'dinodead.png'))
    player_leg1 = pygame.image.load(os.path.join(img_folder, 'dinofirstleg.png'))
    player_leg2 = pygame.image.load(os.path.join(img_folder, 'dinosecondleg.png'))

    images.append(player_leg1)
    images.append(player_leg1)
    images.append(player_leg2)
    images.append(player_leg2)

    def __init__(self, gravity, land):
        self.gravity = gravity
        self.land = land
        pygame.sprite.Sprite.__init__(self)
        self.image = self.images[self.img_index]
        self.rect = self.player_img.get_rect()
        self.rect.center = (100, 525)
        
    

        
        
    def jump(self):

        self.img_index += 1
        self.image = self.images[self.img_index % 4]

        if self.gravity != 0:
            self.image = self.player_img 

        if self.gravity == 0:
            pass
        elif self.gravity > 0 and self.gravity <= 20:
            self.rect.y -= (22 - self.gravity)
            self.gravity += 1
        elif self.gravity == 21 and self.land > 0:
            self.rect.y += (22 - self.land)
            self.land -= 1
        elif self.land == 0:
            self.gravity = 0
            self.land = 20

    
                    

class Game():
    
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    player = Dino(0, 20)
    all_sprites.add(player)

    running = True
    game_over = False
    score = 0

    fps = 60
                
    def cactusMaker(self):
        while self.running:
            new_cactus = Cactuss(random.randint(0, 2))
            self.all_sprites.add(new_cactus)
            time.sleep(random.randrange(50, 200)/100)
                
    def cactusRusher(self):
        while self.running:
            for cactus in self.all_sprites:
                if cactus.rect.right < 0:
                    self.all_sprites.remove(cactus)
                    cactus.kill()
                try:
                    cactus.cactusRush()
                except:
                    pass
                time.sleep(0.004)
                
            
    def game(self):
        
        handCactusMaker = threading.Thread(target=self.cactusMaker)
        handCactusRusher = threading.Thread(target=self.cactusRusher)
        
        handCactusMaker.start()
        handCactusRusher.start()

        while self.running:
            
            while self.game_over:
                my_font = pygame.font.SysFont('times new roman', 49)
                game_over_surface = my_font.render('GAME OVER', True, (0, 0, 0))
                game_over_rect = game_over_surface.get_rect()
                game_over_rect.midtop = (WIDTH/2, HEIGHT/3)
                self.screen.blit(game_over_surface, game_over_rect)
                score_surface = my_font.render('Score:{}'.format(int(self.score/10)), True, (0, 0, 0))
                score_rect = score_surface.get_rect()
                score_rect.midtop = (WIDTH/2, HEIGHT/4)
                self.screen.blit(score_surface, score_rect)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        pygame.quit()
                    if event.type == pygame.KEYDOWN: 
                        if event.key == pygame.K_SPACE:
                            self.score = 0
                            self.all_sprites.clear(self.screen, self.screen)
                            self.all_sprites.add(self.player)
                            self.running = True
                            self.game_over = False
                            pygame.display.flip()


            self.clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_SPACE:
                        if self.player.gravity == 0 and self.player.land == 20:
                            self.player.gravity = 1


            self.player.jump()
            self.score += 1

            
            for spr_cactus in self.all_sprites:
                try:
                    spr_cactus.check()
                    if self.player.rect.right >=  spr_cactus.rect.left and self.player.rect.y + 52  > spr_cactus.rect.y and self.player.rect.left < spr_cactus.rect.right:
                        self.player.image = self.player.player_dead
                        self.fps = 60
                        self.game_over = True
                except:
                    pass
                    

            if self.score % 100 == 0:
                    self.fps += 1

            self.screen.fill(WHITE)
            self.all_sprites.draw(self.screen)
            pygame.display.flip()

        pygame.quit()
        sys.exit()
        
game = Game()
game.game()