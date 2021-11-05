import pygame
import sys
import random
from pygame.locals import *


class Pipe_1():
     def __init__(self):
          self.images = [pipe_up_image, pipe_down_image]
          self.pos_x = screen_width
          self.rand = random.randrange(50, 270, 20)
     def draw(self, screen):
          screen.blit(self.images[0], (self.pos_x, 400-self.rand), ((0, 0), (pipe_width, self.rand)))
          screen.blit(self.images[1], (self.pos_x, 0), ((0, self.rand), (pipe_width, pipe_height)))
     def move_x(self):
          if self.pos_x > -pipe_width:
               self.pos_x -= pipe_speed
          else:
               self.reset()
     def reset(self):
          self.pos_x = screen_width
          self.rand = random.randrange(50, 270, 20)

class Pipe_2():
     def __init__(self):
          self.images = [pipe_up_image, pipe_down_image]
          self.pos_x = pipe_1.pos_x + (screen_width + pipe_width)/2
          self.rand = random.randrange(50, 270, 20)
     def draw(self, screen):
          screen.blit(self.images[0], (self.pos_x, 400-self.rand), ((0, 0), (pipe_width, self.rand)))
          screen.blit(self.images[1], (self.pos_x, 0), ((0, self.rand), (pipe_width, pipe_height)))
     def move_x(self):
          if pipe_1.pos_x < self.pos_x:
               self.pos_x = pipe_1.pos_x + (screen_width + pipe_width)/2
          elif pipe_1.pos_x > self.pos_x and self.pos_x > -pipe_width:
               self.pos_x -= pipe_speed
          else:
               self.reset()
     def reset(self):
          self.pos_x = pipe_1.pos_x + (screen_width + pipe_width)/2
          self.rand = random.randrange(50, 270, 20)

class Land():
     def __init__(self):
          self.image = land_image
          self.pos_x = 0
     def draw(self, screen):
          screen.blit(self.image, (self.pos_x, 400))
     def move_x(self):
          if self.pos_x > -45:
               self.pos_x -= pipe_speed
          else:
               self.pos_x = 0
          
gamename = "Flappybird"
screen_width = 288
screen_height = 512

background_image = "bg_day.png"
pipe_width = 52
pipe_height = 320
pipe_up_image = pygame.image.load("pipe_up.png")
pipe_down_image = pygame.image.load("pipe_down.png")
pipe_speed = 2
land_image = pygame.image.load("land.png")

pygame.init()
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption(gamename)
background = pygame.image.load(background_image)
land = Land()
pipe_1 = Pipe_1()
pipe_2 = Pipe_2()
clock = pygame.time.Clock()

while True:
     for event in pygame.event.get():
          if event.type == QUIT:
               exit()
     screen.blit(background, (0, 0))
     land.move_x()
     land.draw(screen)
     pipe_1.move_x()
     pipe_1.draw(screen)
     pipe_2.move_x()
     pipe_2.draw(screen)
     pygame.display.update()
     clock.tick(20)
     
