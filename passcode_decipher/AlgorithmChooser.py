import RotaryEncoder
import Consts
from queue import Queue

class AlgorithmChooser(object):
    def __init__(self, screen, pins, positions, algos):
        self.queue = Queue()
        self.rotary = RotaryEncoder.RotaryEncoderWorker(pins[0], pins[1], pins[2], self.queue)
        self.position = 0
        self.screen = screen
        self.postions = positions
        self.algos = algos
        
        label = Consts.FONT.render(self.algos[0].value, 1, Consts.RED)
        screen.blit(label, self.postions[0])
        for x in range(1, 6):
            label = Consts.FONT.render(self.algos[x].value, 1, Consts.WHITE)
            screen.blit(label, self.postions[x])
        
    def update(self):
        # this function can be called in order to decide what is happening with the switch
        while not(self.queue.empty()):
            m = self.queue.get_nowait()
            if m == RotaryEncoder.EventLeft:
                # wheel.rotate(-1)
                self.position = (self.position + 1) % 6
                self.change_colored(1)
                print ("Detected one turn to the left " + str(self.position))
            elif m == RotaryEncoder.EventRight:
                # wheel.rotate(1)
                self.position = (self.position - 1) % 6
                self.change_colored(-1)
                print ("Detected one turn to the right " + str(self.position))
            elif m == RotaryEncoder.EventDown:
                print ("Detected press down")
            elif m == RotaryEncoder.EventUp:
                print ("Detected release up")
            self.queue.task_done()
    
    def change_colored(self, direction):
        label = Consts.FONT.render(self.algos[self.position].value, 1, Consts.RED)
        self.screen.blit(label, Consts.POS_LIST_1[self.position])
        
        if (direction == 1):
            prev = (self.position - 1) % 6
        else:
            prev = (self.position + 1) % 6
        label = Consts.FONT.render(self.algos[prev].value, 1, Consts.WHITE)
        self.screen.blit(label, Consts.POS_LIST_1[prev])
        
        