import pygame
import sys
from pygame.locals import *
import random
import imp
exercise_02=imp.load_source('exercise_02','C:/Users/WJXJ/Desktop/Muse/windows/bci-workshop-master/bci-workshop-master/python/exercise_02.py')
import exercise_02


class Bird():
     def __init__(self, pos_x, pos_y, speed):
          self.images = [bird_0_image, bird_1_image, bird_2_image]
          self.order = 0
          self.number = 3
          self.image = self.images[self.order]
          self.rect = self.image.get_rect()
          self.rect.x = pos_x
          self.rect.y = pos_y
          self.base = pygame.Rect(self.rect.x + 6, self.rect.y + 13, 34, 24)
          self.speed_y = speed
          self.crash = 0
          self.score = 0
          self.direct = 1
     def draw(self, screen):
          screen.blit(self.image, (self.rect.x, self.rect.y))
     def flap(self):
          if self.order >= self.number - 1:
              self.order = -1
          self.order += 1
          self.image = self.images[self.order]
     def move_y(self):
          coin_sound = pygame.mixer.Sound("coin_sound.wav")
          self.rect.y += self.speed_y
          self.speed_y += gravity
          self.base = pygame.Rect(self.rect.x + 6, self.rect.y + 13, 34, 24)
          if self.rect.x == pipe_1.rect_up.x or self.rect.x == pipe_2.rect_up.x + 1:
               coin_sound.play()
               self.score = max(pipe_1.order, pipe_2.order) - 1
               
     def up_and_down(self, pos_y):
          if self.rect.y <= pos_y:
               self.direct = 1
               self.rect.y += self.direct
          elif self.rect.y >= pos_y + 5 :
               self.direct = -1
               self.rect.y += self.direct
          else:
               self.rect.y += self.direct
     def soar(self, speed):
          self.speed_y = speed
     def drop(self):
          self.rect.y += self.speed_y
          self.speed_y += gravity
     def die(self):
          self.rect.y = 365
          self.image = self.images[2]
class Pipe_1():
     def __init__(self):
          self.images = [pipe_up_image, pipe_down_image]
          self.rand= random.randrange(50, 270, 20)
          self.rect_up = self.images[0].get_rect()
          self.rect_down = self.images[1].get_rect()
          self.order = 1
          self.rect_up.x = 1.5 * screen_width
          self.rect_down.x = 1.5 * screen_width
          self.rect_up.y = 400 - self.rand
          self.rect_down.y  = -self.rand
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
          self.order += 2
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
          self.order = 0
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
          self.order += 2
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
          if self.rect.x > -44:
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

class Score():
     def __init__(self):
          self.images = [num_0_image, num_1_image, num_2_image, num_3_image,
                         num_4_image, num_5_image, num_6_image, num_7_image,
                         num_8_image, num_9_image]
          self.hun_pos_3 = 108
          self.dec_pos_3 = 132
          self.dec_pos_2 = 120
          self.uni_pos_3 = 156
          self.uni_pos_2 = 144
          self.uni_pos_1 = 132
     def draw(self, screen, score):
          if score < 10:
               screen.blit(self.images[score], (self.uni_pos_1, 0))
          if score >= 10 and score <100:
               screen.blit(self.images[score%10], (self.uni_pos_2, 0))
               screen.blit(self.images[int(score/10)], (self.dec_pos_2, 0))
          if score > 100:
               screen.blit(self.images[score%10], (self.uni_pos_3, 0))
               screen.blit(self.images[int((score%100)/10)], (self.dec_pos_3, 0))
               screen.blit(self.images[int(score/100)], (self.hun_pos_3, 0))

gamename = "Flappy Bird"              
screen_width = 288
screen_height = 512
pipe_width = 52
pipe_height = 320
pipe_speed = 3
gravity = 1.2
soar_speed = -5
play_x = 120
play_y = 190
ready_x = 60
ready_y = 210
game_over_x = 60
game_over_y = 365


background_image = pygame.image.load("bg_day.png")
land_image = pygame.image.load("land.png")
pipe_up_image = pygame.image.load("pipe_up.png")
pipe_down_image = pygame.image.load("pipe_down.png")
bird_0_image = pygame.image.load("bird_0.png")
bird_1_image = pygame.image.load("bird_1.png")
bird_2_image = pygame.image.load("bird_2.png")
num_0_image = pygame.image.load("num_0.png")
num_1_image = pygame.image.load("num_1.png")
num_2_image = pygame.image.load("num_2.png")
num_3_image = pygame.image.load("num_3.png")
num_4_image = pygame.image.load("num_4.png")
num_5_image = pygame.image.load("num_5.png")
num_6_image = pygame.image.load("num_6.png")
num_7_image = pygame.image.load("num_7.png")
num_8_image = pygame.image.load("num_8.png")
num_9_image = pygame.image.load("num_9.png")
score_0_image = pygame.image.load("score_0.png")
score_1_image = pygame.image.load("score_1.png")
score_2_image = pygame.image.load("score_2.png")
score_3_image = pygame.image.load("score_3.png")
score_4_image = pygame.image.load("score_4.png")
score_5_image = pygame.image.load("score_5.png")
score_6_image = pygame.image.load("score_6.png")
score_7_image = pygame.image.load("score_7.png")
score_8_image = pygame.image.load("score_8.png")
score_9_image = pygame.image.load("score_9.png")
medals_0_image = pygame.image.load("medals_0.png")
medals_1_image = pygame.image.load("medals_1.png")
medals_2_image = pygame.image.load("medals_2.png")
medals_3_image = pygame.image.load("medals_3.png")
title_image = pygame.image.load("title.png")
button_play_image = pygame.image.load("button_play.png")
ready_image = pygame.image.load("text_ready.png")
tutorial_image = pygame.image.load("tutorial.png")
game_over_image = pygame.image.load("text_game_over.png")
score_panel_image = pygame.image.load("score_panel.png")
new_image = pygame.image.load("new.png")

pipe_1 = Pipe_1()
pipe_2 = Pipe_2()
land = Land()
clock = pygame.time.Clock()
def play_page():
     pygame.init()
     screen = pygame.display.set_mode([screen_width, screen_height])
     pygame.display.set_caption(gamename)
     bird = Bird(play_x, play_y, 0)
     while True:
          for event in pygame.event.get():
               if event.type == QUIT:
                    exit()
          mouse_x, mouse_y = pygame.mouse.get_pos()
          if pygame.mouse.get_pressed()[0] and mouse_x >= 92 and mouse_x <= 196 and mouse_y >= 287 and mouse_y <= 345:
               break
          screen.blit(background_image, (0, 0))
          screen.blit(title_image, (55, 98))
          screen.blit(button_play_image, (86, 284))
          bird.up_and_down(play_y)
          bird.flap()
          bird.draw(screen)
          land.move_x()
          land.draw(screen)
          pygame.display.update()
          clock.tick(30)

def ready_page():
     pygame.init()
     screen = pygame.display.set_mode([screen_width, screen_height])
     pygame.display.set_caption(gamename)
     bird = Bird(ready_x, ready_y, 0)
     while True:
          for event in pygame.event.get():
               if event.type == QUIT:
                    exit()
          if exercise_02.y_hat==1:
               bird.soar(soar_speed)
               return [bird.rect.x, bird.rect.y, bird.speed_y]
               break
          screen.blit(background_image, (0, 0))
          screen.blit(ready_image, (55, 128))
          screen.blit(tutorial_image, (87, 205))
          bird.up_and_down(ready_y)
          bird.flap()
          bird.draw(screen)
          land.move_x()
          land.draw(screen)
          pygame.display.update()
          clock.tick(30)

def start_page(start_x, start_y, start_speed):
     pygame.init()
     collide_sound = pygame.mixer.Sound("collide_sound.wav")
     pygame.mixer.music.load("bg_music.wav")
     pygame.mixer.music.set_volume(0.5)
     pygame.mixer.music.play(-1)
     screen = pygame.display.set_mode([screen_width, screen_height])
     pygame.display.set_caption(gamename)
     bird = Bird(start_x, start_y, start_speed)
     pipe_1.__init__()
     pipe_2.__init__()
     score = Score()
     first_collide = 1
     while True:
          for event in pygame.event.get():
               if event.type == QUIT:
                    exit()
          screen.blit(background_image, (0, 0))
          if pipe_1.collide(bird.base) == 0 and pipe_2.collide(bird.base) ==0 and land.collide(bird.rect) == 0:
               if pygame.mouse.get_pressed()[0]:
                    bird.soar(soar_speed)
                    #soar_sound.play()
               #pressed_keys = pygame.key.get_pressed()
               #if pressed_keys[K_SPACE]:
                    #bird.soar(soar_speed)
               pipe_1.move_x()
               pipe_1.draw(screen)
               pipe_2.move_x()
               pipe_2.draw(screen)
               bird.move_y()
               bird.flap()
               bird.draw(screen)
               land.move_x()
               land.draw(screen)
               score.draw(screen, bird.score)
          elif (pipe_1.collide(bird.base) == 1 or pipe_2.collide(bird.base) ==1) and land.collide(bird.rect) == 0:
               if first_collide == 1:
                    collide_sound.play()
               pipe_1.halt()
               pipe_1.draw(screen)
               pipe_2.halt()
               pipe_2.draw(screen)
               bird.drop()
               bird.flap()
               bird.draw(screen)
               land.halt()
               land.draw(screen)
               score.draw(screen, bird.score)
               first_collide = 0
          else:
               pipe_1.halt()
               pipe_1.draw(screen)
               pipe_2.halt()
               pipe_2.draw(screen)
               bird.die()
               bird.draw(screen)
               land.halt()
               land.draw(screen)
               score.draw(screen, bird.score)
               pygame.display.update()
               return bird.score
               break
          pygame.display.update()
          clock.tick(30)

def game_over_page(score, best, new):
     pygame.init()
     pygame.mixer.music.load("dead_sound.wav")
     pygame.mixer.music.set_volume(0.5)
     pygame.mixer.music.play()
     screen = pygame.display.set_mode([screen_width, screen_height])
     pygame.display.set_caption(gamename)
     bird = Bird(game_over_x, game_over_y, 0)
     restart = 0
     images = [score_0_image, score_1_image, score_2_image, score_3_image,
               score_4_image, score_5_image, score_6_image, score_7_image,
               score_8_image, score_9_image]
     while True:
          for event in pygame.event.get():
               if event.type == QUIT:
                    exit()
          mouse_x, mouse_y = pygame.mouse.get_pos()
          if pygame.mouse.get_pressed()[0] and mouse_x >= 92 and mouse_x <= 196 and mouse_y >= 337 and mouse_y <= 395:
               restart = 1
               return restart
               break
          screen.blit(background_image, (0, 0))
          pipe_1.halt()
          pipe_1.draw(screen)
          pipe_2.halt()
          pipe_2.draw(screen)
          bird.die()
          bird.draw(screen)
          land.halt()
          land.draw(screen)
          screen.blit(game_over_image, (42, 98))
          screen.blit(score_panel_image, (25, 183))
          screen.blit(button_play_image, (86, 334))
          if score < 10:
               pass
          elif score >= 10 and score < 50:
               screen.blit(medals_3_image, (57, 226))
          elif score >= 50 and score < 100:
               screen.blit(medals_2_image, (57, 226))
          elif score >= 100 and score < 500:
               screen.blit(medals_1_image, (57, 226))
          else:
               screen.blit(medals_0_image, (57, 226))
          if score < 10:
               screen.blit(images[score], (215, 219))
          if score >= 10 and score <100:
               screen.blit(images[score%10], (215, 219))
               screen.blit(images[int(score/10)], (202, 219))
          if score > 100:
               screen.blit(images[score%10], (215, 219))
               screen.blit(images[int((score%100)/10)], (202, 219))
               screen.blit(images[int(score/100)], (189, 219))
          if best < 10:
               screen.blit(images[best], (215, 261))
          if best >= 10 and best <100:
               screen.blit(images[best%10], (215, 261))
               screen.blit(images[int(best/10)], (202, 261))
          if best > 100:
               screen.blit(images[best%10], (215, 261))
               screen.blit(images[int((best%100)/10)], (202, 261))
               screen.blit(images[int(best/100)], (189, 261))
          if new == 1:
               screen.blit(new_image, (165, 243))
          pygame.display.update()
          clock.tick(30)
          
def run():
     play_page()
     restart = 1
     best = 0
     while restart:
          new = 0
          [start_x, start_y, start_speed] = ready_page()
          score = start_page(start_x, start_y, start_speed)
          if score > best:
               best = score
               new = 1
          restart = game_over_page(score, best, new)
          
run()
