__author__ = 'marcelo'

import RPi.GPIO as GPIO

RGB = [7, 11, 12]

GPIO.setmode(GPIO.BOARD)

for leg in RGB:
    GPIO.setup(leg, GPIO.OUT)
    GPIO.output(leg, 0)

try:
    while True:
        request = raw_input("RGB-->")
        if len(request) == 3:
            GPIO.output(RGB[0], int(request[0]))
            GPIO.output(RGB[1], int(request[1]))
            GPIO.output(RGB[2], int(request[2]))

except KeyboardInterrupt:
    pass

GPIO.cleanup()
