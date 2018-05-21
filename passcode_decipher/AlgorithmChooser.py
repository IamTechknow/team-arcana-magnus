import RotaryEncoder
import Consts
from queue import Queue

class AlgorithmChooser(object):
    def __init__(self, screen, pins, positions, algos, color):
        self.queue = Queue()
        self.rotary = RotaryEncoder.RotaryEncoderWorker(pins[0], pins[1], pins[2], self.queue)
        self.position = 0
        self.screen = screen
        self.positions = positions
        self.algos = algos
        self.current_color = color
        
        label = Consts.FONT.render(self.algos[0].value, 1, Consts.RED)
        screen.blit(label, self.positions[0])
        self.text = ""
        self.selected_algo_id = -1
            
        for x in range(1, 6):
            label = Consts.FONT.render(self.algos[x].value, 1, Consts.WHITE)
            screen.blit(label, self.positions[x])
            
    
    def activate(self, text, algo_id):
        self.text = text
        self.selected_algo_id = algo_id
        
        label = Consts.FONT.render(self.text, 1, self.current_color)
        self.screen.blit(label, self.positions[6])
        
    
    def check(self, color):
        # this function can be called in order to decide what is happening with the switch
        self.current_color = color
        
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
        return (self.selected_algo_id == self.position)
    
    def change_colored(self, direction):
        label = Consts.FONT.render(self.algos[self.position].value, 1, Consts.RED)
        self.screen.blit(label, self.positions[self.position])

        if (direction == 1):
            prev = (self.position - 1) % 6
        else:
            prev = (self.position + 1) % 6
        label = Consts.FONT.render(self.algos[prev].value, 1, Consts.WHITE)
        self.screen.blit(label, self.positions[prev])        