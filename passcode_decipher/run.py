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
    pygame.display.set_caption(Consts.TITLE)
    screen = pygame.display.set_mode((Consts.screen_width, Consts.screen_height), 0, 32)
    #screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, 32)
    background = pygame.transform.smoothscale(Consts.IMAGESDICT['board'], (Consts.screen_width, Consts.screen_height))
    fpsClock = pygame.time.Clock()
    GPIO.setmode(GPIO.BCM)
    
    #Sprites
    all_sprites_list = pygame.sprite.Group()

    wheel = sprites.Wheel()
    wheel.rect.x = 200
    wheel.rect.y = 200
    all_sprites_list.add(wheel)
    background = pygame.transform.smoothscale(Consts.IMAGESDICT['board'], (Consts.screen_width, Consts.screen_height))
    fpsClock = pygame.time.Clock()
    rotary_1_queue = Queue()
    rotary_1 = RotaryEncoder.RotaryEncoderWorker(Consts.R1_PIN[0], Consts.R1_PIN[1], Consts.R1_PIN[2], rotary_1_queue)

    cypher = Algorithm()

    # Initialise Texts
    label = Consts.FONT.render(cypher.get_algo_list()[0].value, 1, Consts.RED)
    screen.blit(label, Consts.POS_LIST[0])
    for x in range(1, 6):
        label = Consts.FONT.render(cypher.get_algo_list()[x].value, 1, Consts.WHITE)
        screen.blit(label, Consts.POS_LIST[x])
    
    

    def change_colored(i, direction):
        label = Consts.FONT.render(cypher.get_algo_list()[i].value, 1, Consts.RED)
        screen.blit(label, Consts.POS_LIST[i])
        
        if (direction == 1):
            prev = (i - 1) % 6
        else:
            prev = (i + 1) % 6
        label = Consts.FONT.render(cypher.get_algo_list()[prev].value, 1, Consts.WHITE)
        screen.blit(label, Consts.POS_LIST[prev])
            
    def process(current):
        # this function can be called in order to decide what is happening with the switch
        new = current
        while not(rotary_1_queue.empty()):
            m = rotary_1_queue.get_nowait()
            if m == RotaryEncoder.EventLeft:
                # wheel.rotate(-1)
                new = (current + 1) % 6
                change_colored(new, 1)
                print ("Detected one turn to the left " + str(new))
            elif m == RotaryEncoder.EventRight:
                # wheel.rotate(1)
                new = (current - 1) % 6
                change_colored(new, -1)
                print ("Detected one turn to the right " + str(new))
            elif m == RotaryEncoder.EventDown:
                print ("Detected press down")
            elif m == RotaryEncoder.EventUp:
                print ("Detected release up")
            rotary_1_queue.task_done()
        return new

    try:
        global current_selected_1
        current_selected_1 = 0
        #change_colored(current_selected_1, 1)
        while True:
            # sleep(0.1)
            # pygame.display.update()
            # all_sprites_list.draw(screen)
            pygame.display.update()
            current_selected_1 = process(current_selected_1)
            fpsClock.tick(Consts.FPS)
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    sys.exit()    
    finally:
        print ("ended")
        GPIO.cleanup()
        pygame.quit()