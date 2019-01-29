import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

class Sr04():
    def __init__(self, trigger_pin, echo_pin):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.countup = 0
        self.countdown = 0
        self.distance = 0
        self.starttime = 0.0
        self.stoptime = 0.0
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        print("Setting interrupt on pin ",self.echo_pin)
        GPIO.add_event_detect(self.echo_pin, GPIO.BOTH, callback=self.trap_state)
    
    def read_distance(self):
        # Callbacks are weird: https://raspberrypi.stackexchange.com/questions/27939/using-a-class-function-as-callback
        GPIO.output(self.trigger_pin, True)           # pulse to start a reading 
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin, False)
        # finish the process of getting the reading in callback when pin goes high

    def trap_state(self, channel):
        n = GPIO.input(self.echo_pin)
        if n == 1:
            self.starttime = time.time()
            self.countup +=1
        elif n == 0:
            self.stoptime = time.time()
            elapsed = self.stoptime - self.starttime      # calculate elapsed time
            self.distance = (elapsed * 34300) / 2         # 34300 cm/s round trip - halve to get distance to target
            self.countdown +=1

    def __str__(self):
        return str(self.distance)
        
        
a = Sr04(16,24)
for x in range(100):
    a.read_distance()
    print(a)
    print(a.countup, a.countdown)

GPIO.cleanup()
