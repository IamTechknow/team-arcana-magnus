from time import sleep
from queue import Queue

import pygame, sys
import RPi.GPIO as GPIO

import Consts
import sprites
import RotaryEncoder
from algorithm import Algorithm
from algorithm import AlgorithmType

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)

    pygame.display.set_caption(Consts.TITLE)
    #screen = pygame.display.set_mode((Consts.screen_width, Consts.screen_height), 0, 32)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, 32)
    background = pygame.transform.smoothscale(Consts.IMAGESDICT['board'], (Consts.screen_width, Consts.screen_height))
    fpsClock = pygame.time.Clock()

    all_sprites_list = pygame.sprite.Group()

    wheel = sprites.Wheel()
    wheel.rect.x = 200
    wheel.rect.y = 200
    all_sprites_list.add(wheel)
    posx = 200
    posy = 200
    rotary_1_queue = Queue()
    rotary_1 = RotaryEncoder.RotaryEncoderWorker(Consts.R1_PIN[0], Consts.R1_PIN[1], Consts.R1_PIN[2], rotary_1_queue)

    cypher = Algorithm()

    def process():
        # this function can be called in order to decide what is happening with the switch
        while not(rotary_1_queue.empty()):
            m = rotary_1_queue.get_nowait()
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
            rotary_1_queue.task_done()

    try:
        while True:
            sleep(0.1)
            #pygame.display.update()
            all_sprites_list.draw(screen)
            pygame.display.update()
            process()
            fpsClock.tick(Consts.FPS)
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    sys.exit()    
    finally:
        print ("ended")
        GPIO.cleanup()
        pygame.quit()