from time import sleep
from queue import Queue

import pygame, sys
import RPi.GPIO as GPIO

import Consts
import sprites

import RotaryEncoder
from algorithm import Algorithm
from algorithm import AlgorithmType

GPIO.setmode(GPIO.BCM)

pygame.display.set_caption('Arkana')
screen = pygame.display.set_mode((Consts.screen_width, Consts.screen_height), 0, 32)
background = pygame.transform.smoothscale(Consts.IMAGESDICT['board'], (Consts.screen_width, Consts.screen_height))
fpsClock = pygame.time.Clock()

all_sprites_list = pygame.sprite.Group()

wheel = sprites.Wheel()
wheel.rect.x = 200
wheel.rect.y = 200
all_sprites_list.add(wheel)

def terminate():
    pygame.quit()
    sys.exit()

def rotate(direction):
    print("turned - " + str(direction))
    screen.blit(Consts.IMAGESDICT['girl'], [200, 200])
    
def rotateGirl(direction):
    print("Rotate Girl - " + str(direction))
    wheel.rotate(direction)

def switchPressed():
    print("button pressed")

posx = 200
posy = 200

RotQueue = Queue()
encoder = RotaryEncoder.RotaryEncoderWorker(18, 17, 16, RotQueue)

def process():
    # this function can be called in order to decide what is happening with the switch
    while not(RotQueue.empty()):
        m = RotQueue.get_nowait()
        if m == RotaryEncoder.EventLeft:
            print ("Detected one turn to the left")
            wheel.rotate(-1)
        elif m == RotaryEncoder.EventRight:
            print ("Detected one turn to the right")
            wheel.rotate(1)
        elif m == RotaryEncoder.EventDown:
            print ("Detected press down")
        elif m == RotaryEncoder.EventUp:
            print ("Detected release up")
        RotQueue.task_done()

try:
    while True:
        sleep(0.1)
        #pygame.display.update()
        all_sprites_list.draw(screen)
        pygame.display.update()
        process()
        fpsClock.tick(Consts.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
finally:
    print ("ended")
    GPIO.cleanup()