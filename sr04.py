import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

class Sr04():
    def __init__(self, pins):
        self.pins = pins
        for pinpair in self.pins:
            GPIO.setup(pinpair[0], GPIO.OUT)
            GPIO.setup(pinpair[1], GPIO.IN)
    
    def get_distance(self):
        results = []
        StartTime = time.time()
        StopTime = time.time()
        for pinpair in self.pins:
            GPIO.output(pinpair[0], True)         # pulse to start a reading 
            time.sleep(0.00001)
            GPIO.output(pinpair[0], False)
    
            while GPIO.input(pinpair[1]) == 0:       # catch time until state changes
                StartTime = time.time()
            while GPIO.input(pinpair[1]) == 1:
                StopTime = time.time()
            TimeElapsed = StopTime - StartTime      # calculate time
            distance = (TimeElapsed * 34300) / 2    # 34300 cm/s round trip - halve to get distance to target

            results.append(distance)
            #time.sleep(.25)
        return results
        
x = Sr04(((16,24),(18,32),(19,36),(21,38),(22,40)))
while True:
    results = x.get_distance()
    print(results)
