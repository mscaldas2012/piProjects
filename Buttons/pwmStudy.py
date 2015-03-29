# !/usr/bin/env python
import RPi.GPIO as GPIO
from WiiRemote import WiiRemote
import time

LED = 11
freq = 50
dutyCycle = 50

freqDelta = 5
dutyCycleDelta = 5

GPIO.setmode(GPIO.BOARD)
GPIO.setup (LED, GPIO.OUT)
pwm = GPIO.PWM(LED, freq)
pwm.start(dutyCycle)

remote = WiiRemote()


def changeFreq(newFreq):
    print 'Freq changed to ' + str(newFreq)
    pwm.ChangeFrequency(newFreq)


def changeDutyCycle(newDC):
    print 'Duty Cycle changed to ' + str(newDC)
    pwm.ChangeDutyCycle(newDC)

try:
    while True:
        if remote.arrowUpPressed():
            freq += freqDelta
            changeFreq(freq)
        if remote.arrowDownPressed():
            freq -= freqDelta
            if freq <= 0:
                freq = 1
            changeFreq(freq)
        if remote.arrowLeftPressed():
            dutyCycle -= dutyCycleDelta
            if dutyCycle < 0:
                dutyCycle = 0
            changeDutyCycle(dutyCycle)
        if remote.arrowRightPressed():
            dutyCycle += dutyCycleDelta
            if dutyCycle > 100:
                dutyCycle = 100
            changeDutyCycle(dutyCycle)
        time.sleep(0.2)
except KeyboardInterrupt:
    pass

pwm.stop()
GPIO.cleanup()
