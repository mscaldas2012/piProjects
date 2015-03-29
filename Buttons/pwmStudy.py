# !/usr/bin/env python
import RPi.GPIO as GPIO
from WiiRemote import WiiRemote

LED = 7
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
            changeFreq(freq)
        if remote.arrowLeftPressed():
            dutyCycle -= dutyCycleDelta
            changeDutyCycle(dutyCycle)
        if remote.arrowRightPressed():
            dutyCycle += dutyCycleDelta
            changeDutyCycle(dutyCycle)

except KeyboardInterrupt:
    pass

pwm.stop()
GPIO.cleanup()
