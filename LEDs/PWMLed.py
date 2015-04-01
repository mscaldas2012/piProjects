__author__ = 'marcelo'

import RPi.GPIO as GPIO

class PWMLed:
    pin = -1
    freq = -1
    dc = -1

    pwm = None

    def __init__(self, pin, initialFreq, initialDc):
        GPIO.setup (pin, GPIO.OUT)
        freq = initialFreq
        dc = initialDc
        pwm = GPIO.PWM(pin, freq)
        pwm.start(dc)


    def changeFrequency(self, freq):
        self.pwm.ChangeFrequencyfreq)


    def changeDutyCycle(self, dutyCycle):
        self.pwm.ChangeDutyCycle(dutyCycle)

    def increaseFreq(self, delta):
        self.freq += delta
        print 'Freq changed to ' + str(self.freq)
        self.pwm.ChangeFrequency(self.freq)

    def decreaseFreq(self, delta):
        self.freq -= delta
        if self.freq <= 0:
            self.freq = 0.1
        print 'Freq changed to ' + str(self.freq)
        self.pwm.ChangeFrequency(self.freq)


    def increaseDutyCycle(self, delta):
        self.dc += delta
        if self.dc > 100:
            self.dc = 100
        print 'Duty Cycle changed to ' + str(self.dc)
        self.pwm.ChangeDutyCycle(self.dc)

    def decreaseDutyCycle(self, delta):
        self.dc -= delta
        if self.dc < 0:
            self.dc = 0
        print 'Duty Cycle changed to ' + str(self.dc)
        self.pwm.ChangeDutyCycle(self.dc)

    def __del__(self):
        self.pwm.stop()


