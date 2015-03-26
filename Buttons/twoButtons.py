# !/usr/bin/env python
import RPi.GPIO as GPIO  # Import library that lets you control the Pi's GPIO pins from time import sleep
import cwiid  # wii remote stuff
from time import sleep  # Import time for delays
import logging


# # Import the ISStreamer module
# from ISStreamer.Streamer import Streamer

# # Streamer constructor, this will create a bucket called Double Button LED
# # you'll be able to see this name in your list of logs on initialstate.com
# # your access_key is a secret and is specific to you, don't share it!
# streamer = Streamer(bucket_name="Double Button LED", access_key="[Place Your Access Key Here]")



# Pin assignment - uses Physical numbering...
LED_RED = 7
LED_YELLOW = 11
LED_GREEN = 13
LED_BLUE = 15

LEDs = [LED_RED, LED_YELLOW, LED_GREEN, LED_BLUE]

BUTTON_TOGGLE = 16
BUTTON_RESET = 18


def initWiiMote():
    print 'Press button 1 + 2 on your Wii Remote...'
    sleep(1)

    wm = cwiid.Wiimote()
    print 'Wii Remote connected...'
    print '\nPress the PLUS button to disconnect the Wii and end the application'
    sleep(1)

    #    Rumble = False
    wm.rpt_mode = cwiid.RPT_BTN

    return wm


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

    #  increment - the direction of states
    #  initialize to 1 or increasing
    logging.basicConfig(filename='example.log', level=logging.DEBUG)


def toggle(state):
    logging.info('button pressed...')
    i = 1
    for led in LEDs:
        GPIO.output(led, state >= i)
        i += 1
    # GPIO.output(LED_RED, state >= 1)
    # GPIO.output(LED_YELLOW, state >= 2)
    # GPIO.output(LED_GREEN, state >= 3)
    # GPIO.output(LED_BLUE, state >= 4)

    # streamer.log("state",state) # Stream current state
    # streamer.log("increment",inc) # Stream current increment
    # streamer.log("prev_input",prev_input) # Stream current prev_input

    # streamer.log("button_1", "pressed") # Stream which button was pressed
    sleep(0.2)  # # Wait 0.2 second before looking for another button input


def main():
    init()
    wm = initWiiMote()
    state = 0
    inc = 1
    # This while loop constantly looks for button input (presses)
    try:
        while True:
            # When state toggle button is pressed
            if GPIO.input(BUTTON_TOGGLE) or wm.state['buttons'] == 8:
                # If increment is increasing, increase state by 1 each press
                if inc == 1:
                    state += 1
                # If increment is decreasing (0), decrease state by 1 each press
                else:
                    state -= 1

                # Reached the max state, time to decrease state
                if state == 4:
                    inc = 0
                    # streamer.log("prev_input",prev_input) # Stream prev_input when changed
                    # streamer.log("increment", inc) # Stream increment when changed; "stream name", value
                # Reached the min state, time to increase state
                elif state == 0:
                    inc = 1
                    # streamer.log("prev_input",prev_input) # Stream prev_input when changed
                    # streamer.log("increment", inc) # Stream increment when changed

                toggle(state)
                # When reset button is pressed
            if GPIO.input(BUTTON_RESET):
                # logging.warning('reset Button pressed!')
                for led in LEDs:
                    GPIO.output(led, inc == 0)
                # GPIO.output(LED_YELLOW, inc == 0)
                # GPIO.output(LED_GREEN, inc == 0)
                # GPIO.output(LED_BLUE, inc == 0)

                if inc == 1:  # If light are going on... set them all on
                    state = 4  # Change state to 3
                    inc = 0  # Change increment to decreasing
                    # streamer.log("state",state) # Stream current state
                    # streamer.log("increment",inc) # Stream current increment
                    # streamer.log("prev_input",prev_input) # Stream current prev_input
                    # streamer.log("phrase",1) # used to see when each phrase was executing
                    # If no LEDs are on
                else:  # lights are going off... set them all off!
                    state = 0  # Change state to 3
                    inc = 1  # Change increment to decreasing
                    # streamer.log("state",state) # Stream current state
                    # streamer.log("increment",inc) # Stream current increment
                    # streamer.log("prev_input",prev_input) # Stream current prev_input
                    # streamer.log("phrase",2) # used to see when each phrase was executing
                    # If all LEDs are on
                    # streamer.log("button_2(bullseye)", "pressed") # Stream which button was pressed
                sleep(0.2)  # Wait 0.2 second before looking for another button input
                # streamer.close()
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
