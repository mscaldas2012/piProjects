# !/usr/bin/env python
import RPi.GPIO as GPIO  # Import library that lets you control the Pi's GPIO pins from time import sleep
from time import sleep  # Import time for delays
import logging
from WiiRemote import WiiRemote
# Pin assignment - uses Physical numbering...
LED_RED = 7
LED_YELLOW = 11
LED_GREEN = 13
LED_BLUE = 15

LEDs = [LED_RED, LED_YELLOW, LED_GREEN, LED_BLUE]

BUTTON_TOGGLE = 16
BUTTON_RESET = 18

#  state - decides what LED should be on and off
#  initialize to 0 or all off
def init():
    GPIO.setwarnings(False)  # # Disables messages about GPIO pins already being in use
    GPIO.setmode(GPIO.BOARD)  # # Indicates which pin numbering configuration to use

    GPIO.setup(BUTTON_TOGGLE, GPIO.IN)  # # Tells it that pin 16 (button) will be giving input
    GPIO.setup(BUTTON_RESET,  GPIO.IN)  # # Tells it that pin 18 (button) will be giving input
    for led in LEDs:
        GPIO.setup(led, GPIO.OUT)
        GPIO.output(led,  GPIO.HIGH)
    logging.basicConfig(filename='example.log', level=logging.DEBUG)


def toggle(state):
    logging.info('button pressed...')
    i = 1
    for led in LEDs:
        GPIO.output(led, state >= i)
        i += 1
    sleep(0.2)  # # Wait 0.2 second before looking for another button input


def main():
    init()
    remote = WiiRemote()
    state = 0
    inc = 1

    # This while loop constantly looks for button input (presses)
    try:
        while True:
            # When state toggle button is pressed
            if GPIO.input(BUTTON_TOGGLE) or remote.buttonAPressed():
                # If increment is increasing, increase state by 1 each press
                if inc == 1:
                    state += 1
                # If increment is decreasing (0), decrease state by 1 each press
                else:
                    state -= 1

                # Reached the max state, time to decrease state
                if state == 4:
                    inc = 0
                # Reached the min state, time to increase state
                elif state == 0:
                    inc = 1
                toggle(state)
                # When reset button is pressed
            if GPIO.input(BUTTON_RESET) or remote.buttonBPressed():
                # logging.warning('reset Button pressed!')
                for led in LEDs:
                    GPIO.output(led, inc != 0)

                if inc == 1:  # If light are going on... set them all on
                    state = 5  # Change state to 3
                    inc = 0  # Change increment to decreasing
                    # If no LEDs are on
                else:  # lights are going off... set them all off!
                    state = 0  # Change state to 3
                    inc = 1  # Change increment to decreasing
                    # If all LEDs are on
                sleep(0.2)  # Wait 0.2 second before looking for another button input
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
