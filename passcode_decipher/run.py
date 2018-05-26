import pygame, sys
import RPi.GPIO as GPIO

import Consts

import sprites

import ButtonEncoder

from AlgorithmChooser import AlgorithmChooser

from random import randint

from algorithm import Algorithm
from algorithm import AlgorithmType

import paho.mqtt.client as mqtt

if __name__ == "__main__":
    portal_level = 0
    def on_message(client, userdata, message):
        print(message)
    try:
        pygame.display.set_caption(Consts.TITLE)
        screen = pygame.display.set_mode((Consts.screen_width, Consts.screen_height), 0, 32)
        #screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, 32)

        fpsClock = pygame.time.Clock()
        GPIO.setmode(GPIO.BCM)
        
        background = pygame.transform.smoothscale(Consts.IMAGESDICT['board'], (Consts.screen_width, Consts.screen_height))
        

        cypher = Algorithm()
        
        current_color = Consts.BLUE
        
        chooser_1 = AlgorithmChooser(screen, Consts.R1_PIN, Consts.POS_LIST_1, current_color)
        chooser_2 = AlgorithmChooser(screen, Consts.R2_PIN, Consts.POS_LIST_2, current_color)
        chooser_3 = AlgorithmChooser(screen, Consts.R3_PIN, Consts.POS_LIST_3, current_color)
        choosers = [chooser_1, chooser_2, chooser_3]

        client = mqtt.Client("Tecthulhu")
        client.on_message=on_message
        #client.connect(Consts.MQTT_SERVER, Consts.MQTT_PORT, 60)
        #client.subscribe("portal/levelChange")
        #client.subscribe("portal/factionChange")
        switch_1 = ButtonEncoder.ButtonWorker(Consts.S1_PIN)
        client.loop(2)
        
        #print("selected algorithms : " + str(algos[used_algo_id_1]) + " " + str(algos[used_algo_id_2]) + " " + str(algos[used_algo_id_3]))
        state = Consts.STATE_STARTING
        current = 0
        nb_tries = 0
        while True:
            fpsClock.tick(Consts.FPS)
            client.loop(0.1)
            if (state == Consts.STATE_STARTING):
                screen.blit(background, [0, 0])
                p = 0
                for s in Consts.STARTUP_TEXTS:
                    label = Consts.MESSAGE_FONT.render(s, 1, current_color)
                    screen.blit(label, (Consts.STARTUP_TEXT_POSITION_X, Consts.STARTUP_TEXT_POSITION_Y + p))
                    p = p + 50
                #display start message
                state = Consts.STATE_DESCRIPTION
            # all_sprites_list.draw(screen)
            # current_color = Consts.BLUE GET from cthulu
            pygame.display.update()
            if (state == Consts.STATE_PLAY) :
                for id in range(0, 3):
                    choosers[id].check(current_color)
            if (switch_1.check()):
                if (state == Consts.STATE_DESCRIPTION):
                    current = 0
                    nb_tries = 4
                    screen.blit(background, [0, 0])
                    for x in range(0, 3):
                        choosers[x].activate(Consts.GLYPHES[current][x], cypher.get_algo_list(portal_level), randint(0, 5))
                    label = Consts.MESSAGE_FONT.render(Consts.HELP_TEXT, 1, Consts.RED)
                    screen.blit(label, (20, Consts.HELP_TEXT_POSITION_Y))
                    state = Consts.STATE_PLAY
                elif (state == Consts.STATE_PLAY) :
                    is_ok = True
                    for id in range(0, 3):
                        chooser = choosers[id]
                        is_ok = is_ok and choosers[id].check(current_color)
                    if (is_ok):
                        state = Consts.STATE_FOUND
                    else:
                        nb_tries = nb_tries - 1
                        if (nb_tries == 0):
                            state = Consts.STATE_STARTING
                    print(" Is it OK for all : " + str(is_ok))
                elif (state == Consts.STATE_WIN_DISPLAY):
                    stqte = Consts.STATE_STARTING
            if (state == Consts.STATE_FOUND):
                screen.blit(background, [0, 0])
                if(current == 1):
                    state = Consts.STATE_WIN_DISPLAY
                    p = 0
                    for s in Consts.WON_TEXTS:
                        label = Consts.MESSAGE_FONT.render(s, 1, current_color)
                        screen.blit(label, (Consts.WON_TEXT_POSITION_X, Consts.WON_TEXT_POSITION_Y + p))
                        p = p + 50
                else:
                    current = 1
                    nb_tries = 4
                    screen.blit(background, [0, 0])
                    for x in range(0, 3):
                        choosers[x].activate(Consts.GLYPHES[current][x], cypher.get_algo_list(portal_level), randint(0, 5))
                        state = Consts.STATE_PLAY
            
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