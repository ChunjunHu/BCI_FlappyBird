import pygame
import sys
from pygame.locals import *

class Bird(pygame.sprite.Sprite):
     width = 80
     height = 60
     number = 3
     bird0_0 = pygame.image.load("bird_0.png")
     bird0_1 = pygame.image.load("bird_1.png")
     bird0_2 = pygame.image.load("bird_2.png")
     images = [bird0_0, bird0_1, bird0_2]
     def __init__(self, start_x, start_y):
          self.order = 0
          pygame.sprite.Sprite.__init__(self)
          self.image = self.images[self.order]
          self.rect = self.image.get_rect()
          self.rect.x = start_x
          self.rect.y = start_y
          self.speed_y = 0
          
     def move_y(self):
          self.rect.y += self.speed_y
          self.speed_y += gravity
          
     def soar(self, speed):
          self.speed_y = speed
          
     def update(self):
          if self.order >= self.number - 1:
              self.order = -1
          self.order += 1
          self.image = self.images[self.order]
     
gamename = "Flappybird"
screen_width = 288
screen_height = 512
background_image = "bg_day.png"
land_image = "land.png"
soar_speed = -15
gravity = 2.5


pygame.init()
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption(gamename)
bird = Bird(screen_width/5, screen_height/3)
bird_plain = pygame.sprite.RenderPlain(bird)
background = pygame.image.load(background_image)
land = pygame.image.load(land_image)
clock = pygame.time.Clock()
while True:
     #check events
     for event in pygame.event.get():
          if event.type == QUIT:
               exit()
          if pygame.mouse.get_pressed()[0]:
               bird.soar(soar_speed)
     bird.move_y()
     bird.update()
     screen.blit(background, (0, 0))
     screen.blit(land, (0, 400))
     bird_plain.draw(screen)
     pygame.display.update()
     #set the speed
     clock.tick(20)
