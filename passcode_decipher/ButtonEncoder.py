import RPi.GPIO as GPIO
from queue import Queue

EventClick = 'C'

class ButtonWorker(object):
    def __init__(self, pin):
        self.gpio = GPIO
        self.gpio.setwarnings(False)
        self.queue = Queue()
        
        self.pin = pin
        
        self.gpio.setmode(GPIO.BCM)
        
        self.gpio.setup(self.pin, self.gpio.IN, pull_up_down=self.gpio.PUD_UP)
        self.gpio.add_event_detect(self.pin, GPIO.RISING, callback=self.Call, bouncetime=500)
        
    def Call(self, pin):
        state = self.gpio.input(pin)
        self.queue.put(EventClick)
        
    def check(self):
        result = False
        while not (self.queue.empty()):
            m = self.queue.get_nowait()
            if m == EventClick:
                print ("Clicked")
                result =  True
            self.queue.task_done()
        return result