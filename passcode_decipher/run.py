from queue import Queue
import pygame, sys
import RPi.GPIO as GPIO

import Consts

import sprites

import RotaryEncoder
import ButtonEncoder

from random import randint

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
    
    switch_1_queue = Queue()
    switch_1 = ButtonEncoder.ButtonWorker(Consts.S1_PIN, switch_1_queue)

    cypher = Algorithm()
    algos = cypher.get_algo_list()

    # Initialise Texts
    label = Consts.FONT.render(algos[0].value, 1, Consts.RED)
    screen.blit(label, Consts.POS_LIST[0])
    for x in range(1, 6):
        label = Consts.FONT.render(algos[x].value, 1, Consts.WHITE)
        screen.blit(label, Consts.POS_LIST[x])
    
    

    def change_colored(i, direction):
        label = Consts.FONT.render(algos[i].value, 1, Consts.RED)
        screen.blit(label, Consts.POS_LIST[i])
        
        if (direction == 1):
            prev = (i - 1) % 6
        else:
            prev = (i + 1) % 6
        label = Consts.FONT.render(algos[prev].value, 1, Consts.WHITE)
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

    def processBtnQueue(btn_queue):
        result = False
        while not (btn_queue.empty()):
            m = btn_queue.get_nowait()
            if m == ButtonEncoder.EventClick:
                print ("Clicked")
                result =  True
            btn_queue.task_done()
        return result
   
    try:
        global current_selected_1
        used_algo_id = randint(0, 5)
        print("selected algorithm : " + str(used_algo_id) + " - " + str(algos[used_algo_id]) )
        current_selected_1 = 0
        #change_colored(current_selected_1, 1)
        while True:
            # sleep(0.1)
            # pygame.display.update()
            # all_sprites_list.draw(screen)
            pygame.display.update()
            current_selected_1 = process(current_selected_1)
            if (processBtnQueue(switch_1_queue)):
                print("Selected Algo" + str(current_selected_1) + " - " + str(algos[current_selected_1]) \
                      + " against used Algo  : " + str(used_algo_id) + " - " + str(algos[used_algo_id]))
            
            fpsClock.tick(Consts.FPS)
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    sys.exit()
                elif (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_ESCAPE):
                        sys.exit()                               
                
    finally:
        print ("ended")
        GPIO.cleanup()
        pygame.quit()