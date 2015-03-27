# !/usr/bin/env python

__author__ = "Marcelo Caldas"

import RPi.GPIO as GPIO
import time

LED_RED = 7
LED_YELLOW = 11
LED_GREEN = 13
LED_BLUE = 15
LEDs = [LED_RED, LED_YELLOW, LED_GREEN, LED_BLUE]
pwm =[]

GPIO.setmode(GPIO.BOARD)

for led in LEDs:
    GPIO.setup (led, GPIO.OUT)
    p = GPIO.PWM(led, 60)
    pwm.append(p)
    p.start(0)
   
try:
    while True:
        for i in range(100):
            for p in pwm:
                p.ChangeDutyCycle(i)
            time.sleep(0.02)
        for i in range(100):
            for p in pwm:
                p.ChangeDutyCycle(100-i)
            time.sleep(0.02)

except KeyboardInterrupt:
    pass

for p in pwm:
    p.stop()
GPIO.cleanup()
