import pygame, sys
import RPi.GPIO as GPIO

import Consts

import sprites

import ButtonEncoder

from AlgorithmChooser import AlgorithmChooser

from random import randint

from algorithm import Algorithm
from algorithm import AlgorithmType

if __name__ == "__main__":   
    try:
        pygame.display.set_caption(Consts.TITLE)
        screen = pygame.display.set_mode((Consts.screen_width, Consts.screen_height), 0, 32)
        #screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, 32)

        fpsClock = pygame.time.Clock()
        GPIO.setmode(GPIO.BCM)
        
        #Sprites
        #all_sprites_list = pygame.sprite.Group()
        #wheel = sprites.Wheel()
        #wheel.rect.x = 200
        #wheel.rect.y = 200
        #all_sprites_list.add(wheel)
        
        background = pygame.transform.smoothscale(Consts.IMAGESDICT['board'], (Consts.screen_width, Consts.screen_height))
        screen.blit(background, [0, 0])

        cypher = Algorithm()
        algos = cypher.get_algo_list()
        
        current_color = Consts.BLUE
        
        chooser_1 = AlgorithmChooser(screen, Consts.R1_PIN, Consts.POS_LIST_1, algos, current_color)
        chooser_2 = AlgorithmChooser(screen, Consts.R2_PIN, Consts.POS_LIST_2, algos, current_color)
        chooser_3 = AlgorithmChooser(screen, Consts.R3_PIN, Consts.POS_LIST_3, algos, current_color)
        choosers = [chooser_1, chooser_2, chooser_3]

        for x in range(0, 3):
            choosers[x].activate(Consts.GLYPHES[0][x], randint(0, 5))
        
        switch_1 = ButtonEncoder.ButtonWorker(Consts.S1_PIN)
        
        
        #print("selected algorithms : " + str(algos[used_algo_id_1]) + " " + str(algos[used_algo_id_2]) + " " + str(algos[used_algo_id_3]))
        
        while True:
            # all_sprites_list.draw(screen)
            # current_color = Consts.BLUE GET from cthulu
            pygame.display.update()
            for id in range(0, 3):
                choosers[id].check(current_color)
            if (switch_1.check()):
                is_ok = True
                for id in range(0, 3):
                    chooser = choosers[id]
                    is_ok = is_ok and choosers[id].check(current_color)
                    print( "Chooser " + str(id) +" Selected Algo : " + str(chooser.position) + " - " + str(algos[chooser.position]) \
                          + " against used Algo : " + str(chooser.selected_algo_id) + " - " + str(chooser.algos[chooser.selected_algo_id]))
                print(" Is it OK for all : " + str(is_ok))

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