import pygame
import sys
from pygame.locals import *
import random

class Bird(pygame.sprite.Sprite):
     def __init__(self, bird_0, bird_1, bird_2, start_x, start_y):
          pygame.sprite.Sprite.__init__(self)
          self.images = [bird_0, bird_1, bird_2]
          self.order = 0
          self.number = 3
          self.image = self.images[self.order]
          self.rect = self.image.get_rect()
          self.rect.x = start_x
          self.rect.y = start_y
          self.base = pygame.Rect(self.rect.x + 6, self.rect.y + 13, 34, 24)
          self.speed_y = 0
          self.crash = 0
     def update(self):
          if self.order >= self.number - 1:
              self.order = -1
          self.order += 1
          self.image = self.images[self.order]
     def move_y(self):
          self.rect.y += self.speed_y
          self.speed_y += gravity
          self.base = pygame.Rect(self.rect.x + 6, self.rect.y + 13, 34, 24)
     def soar(self, speed):
          self.speed_y = speed
     def drop(self):
          self.rect.y += self.speed_y
          self.speed_y += gravity
     def die(self):
          self.rect.y = 365
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
     def halt(self):
          pass
               
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
     def halt(self):
          pass

class Land():
     def __init__(self):
          self.image = land_image
          self.rect = self.image.get_rect()
          self.rect.x = 0
          self.rect.y = 400
          
     def draw(self, screen):
          screen.blit(self.image, (self.rect.x, self.rect.y))
     def move_x(self):
          if self.rect.x > -42:
               self.rect.x -= pipe_speed
          else:
               self.rect.x = 0
     def collide(self, bird_rect):
          if self.rect.colliderect(bird_rect):
               collide_land = 1
          else:
               collide_land = 0
          return collide_land
     def halt(self):
          pass

gamename = "Flappybird"              
screen_width = 288
screen_height = 512
pipe_width = 52
pipe_height = 320
pipe_speed = 5
gravity = 2.5
soar_speed = -8

pygame.init()
pygame.mixer.pre_init(44100,-16,8,2048)
pygame.mixer.init()
background_image = pygame.image.load("bg_day.png")
land_image = pygame.image.load("land.png")
pipe_up_image = pygame.image.load("pipe_up.png")
pipe_down_image = pygame.image.load("pipe_down.png")
bird_0 = pygame.image.load("bird_0.png")
bird_1 = pygame.image.load("bird_1.png")
bird_2 = pygame.image.load("bird_2.png")
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption(gamename)
bird = Bird(bird_0, bird_1, bird_2, screen_width/5, screen_height/3)
bird_plain = pygame.sprite.RenderPlain(bird)
pipe_1 = Pipe_1()
pipe_2 = Pipe_2()
land = Land()
clock = pygame.time.Clock()

while True:
     screen.blit(background_image, (0, 0))
     for event in pygame.event.get():
          if event.type == QUIT:
                    exit()
     if pipe_1.collide(bird.base) == 0 and pipe_2.collide(bird.base) ==0 and land.collide(bird.rect) == 0:
          if pygame.mouse.get_pressed()[0]:
               bird.soar(soar_speed)
          #pressed_keys = pygame.key.get_pressed()
          #if pressed_keys[K_SPACE]:
               #bird.soar(soar_speed)
          pipe_1.move_x()
          pipe_1.draw(screen)
          pipe_2.move_x()
          pipe_2.draw(screen)
          bird.move_y()
          bird.update()
          bird_plain.draw(screen)
          land.move_x()
          land.draw(screen)
     elif (pipe_1.collide(bird.base) == 1 or pipe_2.collide(bird.base) ==1) and land.collide(bird.rect) == 0:
          pipe_1.halt()
          pipe_1.draw(screen)
          pipe_2.halt()
          pipe_2.draw(screen)
          bird.drop()
          bird.update()
          bird_plain.draw(screen)
          land.halt()
          land.draw(screen)
          
     else:
          pipe_1.halt()
          pipe_1.draw(screen)
          pipe_2.halt()
          pipe_2.draw(screen)
          bird.die()
          bird_plain.draw(screen)
          land.halt()
          land.draw(screen)
          pygame.display.update()
     pygame.display.update()
     clock.tick(20)


     
