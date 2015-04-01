# !/usr/bin/env python
import RPi.GPIO as GPIO
from WiiRemote import WiiRemote
from PWMLed import PWMLed
import time

LED = 11
freq = 50
dutyCycle = 50

freqDelta = 5
dutyCycleDelta = 5

GPIO.setmode(GPIO.BOARD)
pwm = PWMLed(LED, freq, dutyCycle)
remote = WiiRemote()


try:
    while True:
        if remote.arrowUpPressed():
            pwm.increaseFreq(freqDelta)
        if remote.arrowDownPressed():
            pwm.decreaseFreq(freqDelta)
        if remote.arrowLeftPressed():
            pwm.decreaseDutyCycle(dutyCycleDelta)
        if remote.arrowRightPressed():
            pwm.increaseDutyCycle(dutyCycleDelta)
        time.sleep(0.2)
except KeyboardInterrupt:
    pass

GPIO.cleanup()
