from queue import Queue
import pygame, sys
import RPi.GPIO as GPIO

import Consts

import sprites

import RotaryEncoder
import ButtonEncoder

from AlgorithmChooser import AlgorithmChooser

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
    #all_sprites_list = pygame.sprite.Group()

    #wheel = sprites.Wheel()
    #wheel.rect.x = 200
    #wheel.rect.y = 200
    #all_sprites_list.add(wheel)
    background = pygame.transform.smoothscale(Consts.IMAGESDICT['board'], (Consts.screen_width, Consts.screen_height))
    fpsClock = pygame.time.Clock()
    

    cypher = Algorithm()
    algos = cypher.get_algo_list()
    
    chooser_1 = AlgorithmChooser(screen, Consts.R1_PIN, Consts.POS_LIST_1, algos)
    chooser_2 = AlgorithmChooser(screen, Consts.R2_PIN, Consts.POS_LIST_2, algos)
    chooser_3 = AlgorithmChooser(screen, Consts.R3_PIN, Consts.POS_LIST_3, algos)

    switch_1_queue = Queue()
    switch_1 = ButtonEncoder.ButtonWorker(Consts.S1_PIN, switch_1_queue)
    
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
        global cur_sel_algo
        used_algo_id = randint(0, 5)
        print("selected algorithm : " + str(used_algo_id) + " - " + str(algos[used_algo_id]) )
        current_glyph = 0
        while True:
            # pygame.display.update()
            # all_sprites_list.draw(screen)
            pygame.display.update()
            chooser_1.update()
            chooser_2.update()
            chooser_3.update()
            if (processBtnQueue(switch_1_queue)):
                print("Selected Algo1 : " + str(chooser_1.position) + " - " + str(algos[chooser_1.position]) \
                      + " against used Algo1 : " + str(used_algo_id) + " - " + str(algos[used_algo_id]))
                print("Selected Algo2 : " + str(chooser_2.position) + " - " + str(algos[chooser_2.position]) \
                      + " against used Algo2 : " + str(used_algo_id) + " - " + str(algos[used_algo_id]))
                print("Selected Algo3 : " + str(chooser_3.position) + " - " + str(algos[chooser_3.position]) \
                      + " against used Algo3 : " + str(used_algo_id) + " - " + str(algos[used_algo_id]))
            
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