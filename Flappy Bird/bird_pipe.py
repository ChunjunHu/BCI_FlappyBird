import pygame
import sys
from pygame.locals import *
import random

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
          self.base = pygame.Rect(self.rect.x + 5, self.rect.y + 12, 36, 26)
     def move_y(self):
          self.rect.y += self.speed_y
          self.speed_y += gravity
          self.base = pygame.Rect(self.rect.x + 5, self.rect.y + 12, 36, 26)
     def soar(self, speed):
          if pipe_1.collide(self.base) == 0 and pipe_2.collide(self.base) == 0:
               self.speed_y = speed
          else:
               self.speed_y = 0
          
     def update(self):
          if self.order >= self.number - 1:
              self.order = -1
          self.order += 1
          self.image = self.images[self.order]

class Pipe_1():
     def __init__(self):
          self.images = [pipe_up_image, pipe_down_image]
          self.rand= random.randrange(50, 270, 20)
          self.rect_up = self.images[0].get_rect()
          self.rect_down = self.images[1].get_rect()
          self.reset()
     def draw(self, screen):
          screen.blit(self.images[0], (self.rect_up.x, self.rect_up.y))
          screen.blit(self.images[1], (self.rect_down.x, self.rect_down.y))
     def move_x(self):
          if self.collide(bird.base) == 0 and pipe_2.collide(bird.base) == 0:
               if self.rect_up.x > -pipe_width:
                    self.rect_up.x -= pipe_speed
                    self.rect_down.x -= pipe_speed
               else:
                    self.reset()
     def reset(self):
          self.rand = random.randrange(50, 270, 20)
          self.rect_up.x = screen_width
          self.rect_down.x = screen_width
          self.rect_up.y = 400 - self.rand
          self.rect_down.y  = -self.rand
     def collide(self, bird_rect):
          if self.rect_up.colliderect(bird_rect):
               collide_pipe = 1
          elif self.rect_down.colliderect(bird_rect):
               collide_pipe= 1
          else:
               collide_pipe = 0
          return collide_pipe
               
class Pipe_2():
     def __init__(self):
          self.images = [pipe_up_image, pipe_down_image]
          self.rand= random.randrange(50, 270, 20)
          self.rect_up = self.images[0].get_rect()
          self.rect_down = self.images[1].get_rect()
          self.reset()
     def draw(self, screen):
          screen.blit(self.images[0], (self.rect_up.x, self.rect_up.y))
          screen.blit(self.images[1], (self.rect_down.x, self.rect_down.y))
     def move_x(self):
          if self.collide(bird.base) == 0 and pipe_1.collide(bird.base) == 0:
               if pipe_1.rect_up.x < self.rect_up.x:
                    self.rect_up.x = pipe_1.rect_up.x + (screen_width + pipe_width)/2
                    self.rect_down.x = pipe_1.rect_down.x + (screen_width + pipe_width)/2
               elif pipe_1.rect_up.x > self.rect_up.x and self.rect_up.x > -pipe_width:
                    self.rect_up.x -= pipe_speed
                    self.rect_down.x -= pipe_speed
               else:
                    self.reset()
     def reset(self):
          self.rand = random.randrange(50, 270, 20)
          self.rect_up.x = pipe_1.rect_up.x + (screen_width + pipe_width)/2
          self.rect_down.x = pipe_1.rect_up.x + (screen_width + pipe_width)/2
          self.rect_up.y = 400 - self.rand
          self.rect_down.y  = -self.rand
     def collide(self, bird_rect):
          if self.rect_up.colliderect(bird_rect):
               collide_pipe = 1
          elif self.rect_down.colliderect(bird_rect):
               collide_pipe= 1
          else:
               collide_pipe = 0
          return collide_pipe

gamename = "Flappybird"
screen_width = 288
screen_height = 512
background_image = "bg_day.png"


pipe_width = 52
pipe_height = 320
pipe_up_image = pygame.image.load("pipe_up.png")
pipe_down_image = pygame.image.load("pipe_down.png")
pipe_speed = 5
gravity = 2
soar_speed = -10

pygame.init()
background = pygame.image.load(background_image)
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption(gamename)
bird = Bird(screen_width/5, screen_height/3)
bird_plain = pygame.sprite.RenderPlain(bird)
pipe_1 = Pipe_1()
pipe_2 = Pipe_2()
clock = pygame.time.Clock()

while True:
     #check events
     for event in pygame.event.get():
          if event.type == QUIT:
               exit()
          if pygame.mouse.get_pressed()[0]:
               bird.soar(soar_speed)
     screen.blit(background, (0, 0))
     bird.move_y()
     bird.update()
     bird_plain.draw(screen)
     pipe_1.move_x()
     pipe_1.draw(screen)
     pipe_2.move_x()
     pipe_2.draw(screen)
     pygame.display.update()
     #set the speed
     clock.tick(20)
