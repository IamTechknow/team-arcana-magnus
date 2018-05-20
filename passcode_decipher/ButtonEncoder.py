import RPi.GPIO as GPIO

EventClick = 'C'

class ButtonWorker(object):
    def __init__(self, pin, Q):
        self.gpio = GPIO
        self.gpio.setwarnings(False)
        self.queue = Q
        
        self.pin = pin
        
        self.gpio.setmode(GPIO.BCM)
        
        self.gpio.setup(self.pin, self.gpio.IN, pull_up_down=self.gpio.PUD_UP)
        self.gpio.add_event_detect(self.pin, GPIO.RISING, callback = self.call, bouncetime = 50)
        
    def call(self):
        state = self.gpio.input(self.pin)
        self.queue.put(EventClick)
        
    def process(self):
        result = False
        while not (self.queue.empty()):
            m = self.queue.get_nowait()
            if m == ButtonEncoder.EventClick:
                print ("Clicked")
                result =  True
            self.queue.task_done()
        return result