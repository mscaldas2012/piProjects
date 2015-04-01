# Controlling a RGB LED with built in PWM.
# Mostly copied from GPIO PWM example:
# http://code.google.com/p/raspberry-gpio-python/wiki/PWM

import time
import RPi.GPIO as GPIO
import math
# # Import the ISStreamer module
from ISStreamer.Streamer import Streamer

# # Streamer constructor, this will create a bucket called Double Button LED
# # you'll be able to see this name in your list of logs on initialstate.com
# # your access_key is a secret and is specific to you, don't share it!
streamer = Streamer(bucket_name="RGB-LED w PWM ", access_key="NOwR5LCsHTSnZalwI5HA5MQosgztjA8d")


GPIO.setmode(GPIO.BOARD)
red = 7
green = 11
blue = 12

GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

Freq = 100  # Hz

# setup all the colours
RED = GPIO.PWM(red, Freq)  # Pin, frequency
RED.start(0)  # Initial duty cycle of 0, so off
GREEN = GPIO.PWM(green, Freq)
GREEN.start(0)
BLUE = GPIO.PWM(blue, Freq)
BLUE.start(0)


def colour(r, g, b, on_time):
    # colour brightness range is 0-100
    RED.ChangeDutyCycle(r)
    GREEN.ChangeDutyCycle(g)
    BLUE.ChangeDutyCycle(b)
    streamer.log("red", r)
    streamer.log("green", g)
    streamer.log("blue", b)

    time.sleep(on_time)

    # turn everything off
    RED.ChangeDutyCycle(0)
    GREEN.ChangeDutyCycle(0)
    BLUE.ChangeDutyCycle(0)


def PosSinWave(amplitude, angle, frequency):
    # angle in degrees
    # creates a positive sin wave between 0 and amplitude*2
    return amplitude + (amplitude * math.sin(math.radians(angle) * frequency))


try:

    while True:
        for i in range(0, 720, 5):
            colour(PosSinWave(50, i, 0.5),
                   PosSinWave(50, i, 1),
                   PosSinWave(50, i, 2),
                   0.1)

except KeyboardInterrupt:
    pass

    # Stop all the PWM objects
RED.stop()
GREEN.stop()
BLUE.stop()

# Tidy up and remaining connections.
GPIO.cleanup()