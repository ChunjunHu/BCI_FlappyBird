import pygame
import sys
from pygame.locals import *
import random
import argparse
import numpy as np  # Module that simplifies computations on matrices
import matplotlib.pyplot as plt  # Module used for plotting
from pylsl import StreamInlet, resolve_byprop  # Module to receive EEG data
import winsound
import bci_workshop_tools as BCIw  # Our own functions for the workshop

###小鸟类##
class Bird():
     def __init__(self, pos_x, pos_y, speed):  #初始化
          self.images = [bird_0_image, bird_1_image, bird_2_image]
          self.order = 0  #应该放第几张图片
          self.number = 3   #做一个动画一共需要3张图
          self.image = self.images[self.order]
          self.rect = self.image.get_rect()  #取出一个代表图片的矩形
          self.rect.x = pos_x  #矩形左上角的坐标
          self.rect.y = pos_y
          #小鸟图片并非充满整个rect，做碰撞检测需要小鸟的精确位置，记做self.base
          self.base = pygame.Rect(self.rect.x + 6, self.rect.y + 13, 34, 24)
          self.speed_y = speed
          self.crash = 0  #坠落情况
          self.score = 0  #分数
          self.direct = 1  #用于开始界面，小鸟上下浮动的动画，判断小鸟飞动方向
     def draw(self, screen):  #画在屏幕上
          screen.blit(self.image, (self.rect.x, self.rect.y))
     def flap(self):  #扇翅膀动画
          if self.order >= self.number - 1:
              self.order = -1
          self.order += 1
          self.image = self.images[self.order]
     def move_y(self):  #小鸟动作规律以及积分情况
          coin_sound = pygame.mixer.Sound("coin_sound.wav")
          self.rect.y += self.speed_y
          self.speed_y += gravity
          self.base = pygame.Rect(self.rect.x + 6, self.rect.y + 13, 34, 24)
          if self.rect.x == pipe_1.rect_up.x or self.rect.x == pipe_2.rect_up.x + 1:
               coin_sound.play()
               self.score = max(pipe_1.order, pipe_2.order) - 1
               
     def up_and_down(self, pos_y):  #开始界面，小鸟上下浮动的动画
          if self.rect.y <= pos_y:
               self.direct = 1
               self.rect.y += self.direct
          elif self.rect.y >= pos_y + 5 :
               self.direct = -1
               self.rect.y += self.direct
          else:
               self.rect.y += self.direct
     def soar(self, speed):  #点击小鸟飞起
          self.speed_y = speed
     def drop(self):  #小鸟坠落
          self.rect.y += self.speed_y
          self.speed_y += gravity
     def die(self):  #小鸟死亡
          self.rect.y = 365
          self.image = self.images[2]
          
###柱子1###
class Pipe_1():
     def __init__(self):  #初始化
          self.images = [pipe_up_image, pipe_down_image]
          self.rand= random.randrange(50, 270, 20)
          self.rect_up = self.images[0].get_rect()  #上部分柱子
          self.rect_down = self.images[1].get_rect()  #下部分柱子
          self.order = 1  #柱子编号
          self.rect_up.x = 1.5 * screen_width  #位置
          self.rect_down.x = 1.5 * screen_width
          self.rect_up.y = 400 - self.rand
          self.rect_down.y  = - self.rand - 100
     def draw(self, screen):  #画在屏幕上
          screen.blit(self.images[0], (self.rect_up.x, self.rect_up.y))
          screen.blit(self.images[1], (self.rect_down.x, self.rect_down.y))
     def move_x(self):  #柱子动作规律
          if self.rect_up.x > -pipe_width:
               self.rect_up.x -= pipe_speed
               self.rect_down.x -= pipe_speed
          else:
               self.reset()
     def reset(self):  #移出屏幕后重新进入屏幕
          self.rand = random.randrange(50, 270, 20)
          self.rect_up.x = screen_width
          self.rect_down.x = screen_width
          self.rect_up.y = 400 - self.rand
          self.rect_down.y  = -self.rand - 100  ##柱子是320个像素点，地面以上部分400个像素点，两柱之间距离有点近，- 20拉大20个像素的距离，可根据喜好随意设置
          self.order += 2
     def collide(self, bird_rect):  #判断与小鸟的碰撞
          if self.rect_up.colliderect(bird_rect):
               collide_pipe = 1
          elif self.rect_down.colliderect(bird_rect):
               collide_pipe= 1
          else:
               collide_pipe = 0
          return collide_pipe
     def halt(self):
          pass
     
###柱子2，与柱子1一模一样，不再注释###
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
          self.rect_down.y  = - self.rand - 100
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
     
###地面###
class Land():
     def __init__(self):  #初始化
          self.image = land_image
          self.rect = self.image.get_rect()
          self.rect.x = 0
          self.rect.y = 400
          
     def draw(self, screen):  #画在屏幕上
          screen.blit(self.image, (self.rect.x, self.rect.y))
     def move_x(self):  #地面动作规律
          if self.rect.x > -44:
               self.rect.x -= pipe_speed
          else:
               self.rect.x = 0
     def collide(self, bird_rect):  #判断与小鸟碰撞
          if self.rect.colliderect(bird_rect):
               collide_land = 1
          else:
               collide_land = 0
          return collide_land
     def halt(self):
          pass
     
###分数###
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
     def draw(self, screen, score):  #画在屏幕上，为了保持分数在屏幕正中央，判断分数有几位，根据位数画图
          if score < 10:  
               screen.blit(self.images[score], (self.uni_pos_1, 0))
          if score >= 10 and score <100:
               screen.blit(self.images[score%10], (self.uni_pos_2, 0))
               screen.blit(self.images[int(score/10)], (self.dec_pos_2, 0))
          if score > 100:
               screen.blit(self.images[score%10], (self.uni_pos_3, 0))
               screen.blit(self.images[int((score%100)/10)], (self.dec_pos_3, 0))
               screen.blit(self.images[int(score/100)], (self.hun_pos_3, 0))

###可控制变量###
gamename = "Flappy Bird"              
screen_width = 288
screen_height = 512
pipe_width = 52
pipe_height = 320
pipe_speed = 3
gravity = 1.2
soar_speed = -5
play_x = 120  #play界面下小鸟的位置
play_y = 190
ready_x = 60
ready_y = 210  #ready界面下小鸟的位置
game_over_x = 60
game_over_y = 365  #game over界面下小鸟的位置

###加载所有图片###
background_image = pygame.image.load("bg_day.png")
land_image = pygame.image.load("land.png")
pipe_up_image = pygame.image.load("pipe_up.png")
pipe_down_image = pygame.image.load("pipe_down.png")
bird_0_image = pygame.image.load("bird_0.png")
bird_1_image = pygame.image.load("bird_1.png")
bird_2_image = pygame.image.load("bird_2.png")
num_0_image = pygame.image.load("num_0.png")  #显示在屏幕中央的分数图片
num_1_image = pygame.image.load("num_1.png")
num_2_image = pygame.image.load("num_2.png")
num_3_image = pygame.image.load("num_3.png")
num_4_image = pygame.image.load("num_4.png")
num_5_image = pygame.image.load("num_5.png")
num_6_image = pygame.image.load("num_6.png")
num_7_image = pygame.image.load("num_7.png")
num_8_image = pygame.image.load("num_8.png")
num_9_image = pygame.image.load("num_9.png")
score_0_image = pygame.image.load("score_0.png")  #显示在分数版上的分数图片
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

###全局变量初始化，由于小鸟在不同的游戏界面不一样，需要在函数内部设置局部变量
pipe_1 = Pipe_1()
pipe_2 = Pipe_2()
land = Land()
clock = pygame.time.Clock()  #非常重要，控制游戏速度，每一帧的时间间隔

###最开始的play界面###
def play_page():
     pygame.init()
     screen = pygame.display.set_mode([screen_width, screen_height])  #设置屏幕
     pygame.display.set_caption(gamename)  #设置顶栏名称
     bird = Bird(play_x, play_y, 0)
     while True:
          for event in pygame.event.get():
               if event.type == QUIT:
                    exit()
          mouse_x, mouse_y = pygame.mouse.get_pos()
          #判断是否在点击了play button，点击之后退出该状态，进入ready状态
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
          
###准备界面###
def ready_page():
     pygame.init()
     screen = pygame.display.set_mode([screen_width, screen_height])
     pygame.display.set_caption(gamename)
     bird = Bird(ready_x, ready_y, 0)
     while True:
          for event in pygame.event.get():
               if event.type == QUIT:
                    exit()
          #判断是否点击了鼠标，点击之后返回当前小鸟的位置和速度信息，使两界面之间的切换没有瑕疵
          if pygame.mouse.get_pressed()[0]:
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
          clock.tick(30)  #帧速最高不超过30ms/帧
          
###游戏界面，接收上一界面的信息，以保持画面不断帧###
def start_page(start_x, start_y, start_speed):
     pygame.init()
     collide_sound = pygame.mixer.Sound("collide_sound.wav")  #加载碰撞声
     pygame.mixer.music.load("bg_music.wav")  #加载并播放背景音乐，并且设置声音
     pygame.mixer.music.set_volume(0.5)
     pygame.mixer.music.play(-1)
     screen = pygame.display.set_mode([screen_width, screen_height])
     pygame.display.set_caption(gamename)
     bird = Bird(start_x, start_y, start_speed)
     pipe_1.__init__()  #一定要初始化，为以后重玩游戏做准备，否则重玩的时候柱子的初始位置是上一次结束时的位置
     pipe_2.__init__()
     score = Score()
     first_collide = 1
     while True:
          for event in pygame.event.get():
               if event.type == QUIT:
                    exit()
          screen.blit(background_image, (0, 0))
          if pipe_1.collide(bird.base) == 0 and pipe_2.collide(bird.base) ==0 and land.collide(bird.rect) == 0:  #正常飞行
               if pygame.mouse.get_pressed()[0]:
                    bird.soar(soar_speed)
               #pressed_keys = pygame.key.get_pressed() ##这段是通过空格键控制小鸟起飞，根据喜好设定
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
          elif (pipe_1.collide(bird.base) == 1 or pipe_2.collide(bird.base) ==1) and land.collide(bird.rect) == 0:  #碰到柱子坠落
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
          else:  #坠落到地面时的状态
               pipe_1.halt()
               pipe_1.draw(screen)
               pipe_2.halt()
               pipe_2.draw(screen)
               bird.die()
               bird.draw(screen)
               land.halt()
               land.draw(screen)
               score.draw(screen, bird.score)
               pygame.display.update()  #更新图像，否则显示不对
               return bird.score  #返回分数信息，给game over界面
               break  #一旦碰到地面就进入game over界面
          pygame.display.update()
          clock.tick(30)

###game over界面，接收上一界面的分数信息进行显示，接收以往的最高成绩，接收是否产生了新纪录###
def game_over_page(score, best, new):
     pygame.init()
     pygame.mixer.music.load("dead_sound.wav")  #加载并播放结束游戏音乐
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
          #判断是否点击开始按钮以重新开始
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
          #将分数按照位数进行分类，保证分数显示时的美观
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
          #最高成绩显示，同上
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

#开始游戏
if __name__ == "__main__":
    """ 0. PARSE ARGUMENTS """
    parser = argparse.ArgumentParser(description='BCI Workshop example 2')
    parser.add_argument('channels', metavar='N', type=int, nargs='*',
        default=[0, 1, 2, 3],
        help='channel number to use. If not specified, all the channels are used')

    args = parser.parse_args()

    """ 1. CONNECT TO EEG STREAM """

    # Search for active LSL stream
    print('Looking for an EEG stream...')
    streams = resolve_byprop('type', 'EEG', timeout=2)
    if len(streams) == 0:
        raise RuntimeError('Can\'t find EEG stream.')

    # Set active EEG stream to inlet and apply time correction
    print("Start acquiring data")
    inlet = StreamInlet(streams[0], max_chunklen=12)
#    eeg_time_correction = inlet.time_correction(10)

    # Get the stream info, description, sampling frequency, number of channels
    info = inlet.info()
    description = info.desc()
    fs = int(info.nominal_srate())
    n_channels = info.channel_count()

    # Get names of all channels
    ch = description.child('channels').first_child()
    ch_names = [ch.child_value('label')]
    for i in range(1, n_channels):
        ch = ch.next_sibling()
        ch_names.append(ch.child_value('label'))

    """ 2. SET EXPERIMENTAL PARAMETERS """

    # Length of the EEG data buffer (in seconds)
    # This buffer will hold last n seconds of data and be used for calculations
    buffer_length = 15

    # Length of the epochs used to compute the FFT (in seconds)
    epoch_length = 1

    # Amount of overlap between two consecutive epochs (in seconds)
    overlap_length = 0.8

    # Amount to 'shift' the start of each next consecutive epoch
    shift_length = epoch_length - overlap_length

    # Index of the channel (electrode) to be used
    # 0 = left ear, 1 = left forehead, 2 = right forehead, 3 = right ear
    index_channel = args.channels
    # Name of our channel for plotting purposes
    ch_names = [ch_names[i] for i in index_channel]
    n_channels = len(index_channel)

    # Get names of features
    # ex. ['delta - CH1', 'pwr-theta - CH1', 'pwr-alpha - CH1',...]
    feature_names = BCIw.get_feature_names(ch_names)

    # Number of seconds to collect training data for (one class)
    training_length = 20

    """ 3. RECORD TRAINING DATA """

    # Record data for mental activity 0
    winsound.Beep(600,1000)
    eeg_data0, timestamps0 = inlet.pull_chunk(
            timeout=training_length+1, max_samples=fs * training_length)#list类型
    eeg_data0 = np.array(eeg_data0)[:, index_channel]#int数组。取eeg_data的第index_channel列

    print('\nClose your eyes!\n')

    # Record data for mental activity 1
    winsound.Beep(600,1000)
    eeg_data1, timestamps1 = inlet.pull_chunk(
            timeout=training_length+1, max_samples=fs * training_length)
    eeg_data1 = np.array(eeg_data1)[:, index_channel]

    # Divide data into epochs三维数组，[220,4,96]，[220,4]为每一秒数据，移动0.2s后再来一个单元
    eeg_epochs0 = BCIw.epoch(eeg_data0, epoch_length * fs,
                             overlap_length * fs)
    eeg_epochs1 = BCIw.epoch(eeg_data1, epoch_length * fs,
                             overlap_length * fs)

    """ 4. COMPUTE FEATURES AND TRAIN CLASSIFIER """
#计算特征矩阵,大小为[16,]为4通道Delta, Theta, Alpha, meanBeta波段的平均功率谱密度
    feat_matrix0 = BCIw.compute_feature_matrix(eeg_epochs0, fs)
    feat_matrix1 = BCIw.compute_feature_matrix(eeg_epochs1, fs)
        
    [classifier, mu_ft, std_ft, score] = BCIw.train_classifier(
            feat_matrix0, feat_matrix1, 'SVM')

    print(str(score * 100) + '% correctly predicted')

    winsound.Beep(600,1000)

    """ 5. USE THE CLASSIFIER IN REAL-TIME"""

    # Initialize the buffers for storing raw EEG and decisions
    eeg_buffer = np.zeros((int(fs * buffer_length), n_channels))
    filter_state = None  # for use with the notch filter
    decision_buffer = np.zeros((30, 1))

#    plotter_decision = BCIw.DataPlotter(30, ['Decision'])

    # The try/except structure allows to quit the while loop by aborting the
    # script with <Ctrl-C>
    print('Press Ctrl-C in the console to break the while loop.')
    
    
    play_page()  #play界面
    restart = 1  #先将restart置1，否则无法开始游戏
    best = 0
    
    
    while restart:  #判断是否重新开始游戏
        new = 0  #是否产生了新纪录
        [start_x, start_y, start_speed] = ready_page()  #ready界面
        
        
        pygame.init()
        collide_sound = pygame.mixer.Sound("collide_sound.wav")  #加载碰撞声
        pygame.mixer.music.load("bg_music.wav")  #加载并播放背景音乐，并且设置声音
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        screen = pygame.display.set_mode([screen_width, screen_height])
        pygame.display.set_caption(gamename)
        bird = Bird(start_x, start_y, start_speed)
        pipe_1.__init__()  #一定要初始化，为以后重玩游戏做准备，否则重玩的时候柱子的初始位置是上一次结束时的位置
        pipe_2.__init__()
        score = Score()
        first_collide = 1
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
            screen.blit(background_image, (0, 0))
            if pipe_1.collide(bird.base) == 0 and pipe_2.collide(bird.base) ==0 and land.collide(bird.rect) == 0:  #正常飞行
                eeg_data, timestamp = inlet.pull_chunk(timeout=1, max_samples=int(shift_length * fs))

            # Only keep the channel we're interested in
                ch_data = np.array(eeg_data)[:, index_channel]

            # Update EEG buffer
                eeg_buffer, filter_state = BCIw.update_buffer(
                        eeg_buffer, ch_data, notch=True,
                        filter_state=filter_state)
                data_epoch = BCIw.get_last_data(eeg_buffer, epoch_length * fs)

            # Compute features
                feat_vector = BCIw.compute_feature_vector(data_epoch, fs)
                y_hat = BCIw.test_classifier(classifier, feat_vector.reshape(1, -1), mu_ft, std_ft)
                if y_hat==1:
                    bird.soar(soar_speed)
                print(y_hat)
                decision_buffer, _ = BCIw.update_buffer(decision_buffer,
                                                    np.reshape(y_hat, (-1, 1)))
               #pressed_keys = pygame.key.get_pressed() ##这段是通过空格键控制小鸟起飞，根据喜好设定
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
            elif (pipe_1.collide(bird.base) == 1 or pipe_2.collide(bird.base) ==1) and land.collide(bird.rect) == 0:  #碰到柱子坠落
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
            else:  #坠落到地面时的状态
                pipe_1.halt()
                pipe_1.draw(screen)
                pipe_2.halt()
                pipe_2.draw(screen)
                bird.die()
                bird.draw(screen)
                land.halt()
                land.draw(screen)
                score.draw(screen, bird.score)
                pygame.display.update()  #更新图像，否则显示不对
                score=bird.score
                break  #一旦碰到地面就进入game over界面
            pygame.display.update()
            clock.tick(30)
        
        if score > best:
            best = score
            new = 1
        restart = game_over_page(score, best, new)  #game over界面         

