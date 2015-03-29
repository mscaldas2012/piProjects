# !/usr/bin/env python
__author__ = 'marcelo'

import RPi.GPIO as GPIO
import time

class Tuxx:
    LED_RED = 11
    LED_YELLOW = 12
    LED_GREEN = 13

    LED_REDMAN = 15
    LED_GREENMAN = 16

    LED_CARS = [LED_RED, LED_YELLOW, LED_GREEN]
    LED_PEDESTRIAN = [LED_REDMAN, LED_GREENMAN]

    BUTTON_REQUEST_X = 3

    def setup(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.BUTTON_REQUEST_X, GPIO.IN)
        for led in self.LED_CARS:
            GPIO.setup(led, GPIO.OUT)
            GPIO.output(led, GPIO.LOW)

        for led in self.LED_PEDESTRIAN:
            GPIO.setup(led, GPIO.OUT)
            GPIO.output(led, GPIO.LOW)

        # start with Cars moving:
        GPIO.output(self.LED_GREEN, GPIO.HIGH)
        GPIO.output(self.LED_REDMAN, GPIO.LOW)

    def stopTraffic(self):
        print 'Stopping traffic...'
        GPIO.output(self.LED_GREEN, GPIO.LOW)
        GPIO.output(self.LED_YELLOW, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(self.LED_YELLOW, GPIO.LOW)
        GPIO.output(self.LED_RED, GPIO.HIGH)
        time.sleep(1)
        print 'Traffic stopped'

    def walk(self):
        print 'Walk now...'
        GPIO.output(self.LED_REDMAN, GPIO.LOW)
        GPIO.output(self.LED_GREENMAN, GPIO.HIGH)
        time.sleep(8)
        GPIO.output(self.LED_RED, GPIO.LOW)
        GPIO.output(self.LED_YELLOW, GPIO.HIGH)
        print 'Walked...'


    def graceTime(self):
        print 'Grace time...'
        for i in range(0, 7):
            time.sleep(0.5)
            GPIO.output(self.LED_GREENMAN, GPIO.LOW)
            GPIO.output(self.LED_YELLOW, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(self.LED_GREENMAN, GPIO.HIGH)
            GPIO.output(self.LED_YELLOW, GPIO.LOW)
        print 'Time is up!'

    def startTraffic(self):
        print 'Starting traffic ...'
        GPIO.output(self.LED_GREENMAN, GPIO.LOW)
        GPIO.output(self.LED_REDMAN, GPIO.HIGH)
        time.sleep(0.3)
        GPIO.output(self.LED_YELLOW, GPIO.LOW)
        GPIO.output(self.LED_GREEN, GPIO.HIGH)
        print 'Traffic moving...'

    def pedestrianWantsToWalk(self):
       print 'Waiting for button '
       while GPIO.input(self.BUTTON_REQUEST_X) == 1:
           time.sleep(0.1)
       print 'Got request...'


    def startProcess(self):
        self.setup()
        while True:
            self.pedestrianWantsToWalk() 
	    self.stopTraffic ()
            self.walk()
            self.graceTime()
            self.startTraffic()


if __name__ == '__main__':
    tuxx = Tuxx()
    try :
        tuxx.startProcess() 
    except KeyboardInterrupt:
        GPIO.cleanup()

