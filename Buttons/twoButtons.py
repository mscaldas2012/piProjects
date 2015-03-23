import RPi.GPIO as GPIO ## Import library that lets you control the Pi's GPIO pins from time import sleep ## Import time for delays
from time import sleep ## Import time for delays
import logging
#
 
## Import the ISStreamer module
#from ISStreamer.Streamer import Streamer
 
## Streamer constructor, this will create a bucket called Double Button LED
## you'll be able to see this name in your list of logs on initialstate.com
## your access_key is a secret and is specific to you, don't share it!
#streamer = Streamer(bucket_name="Double Button LED", access_key="[Place Your Access Key Here]")
 
GPIO.setwarnings(False) ## Disables messages about GPIO pins already being in use
GPIO.setmode(GPIO.BOARD) ## Indicates which pin numbering configuration to use
 
GPIO.setup(16, GPIO.IN) ## Tells it that pin 16 (button) will be giving input
GPIO.setup(18, GPIO.IN) ## Tells it that pin 18 (button) will be giving input
 
GPIO.setup(7, GPIO.OUT) ## Tells it that pin 7 (LED) will be outputting
GPIO.setup(11, GPIO.OUT) ## Tells it that pin 11 (LED) will be outputting
GPIO.setup(13, GPIO.OUT) ## Tells it that pin 13 (LED) will be outputting
GPIO.output(7, GPIO.HIGH) ## Sets pin 7 (LED) to "HIGH" or off
GPIO.output(11, GPIO.HIGH) ## Sets pin 11 (LED) to "HIGH" or off
GPIO.output(13, GPIO.HIGH) ## Sets pin 13 (LED) to "HIGH" or off
 
## state - decides what LED should be on and off
## initialize to 0 or all off
state = 0
 
## increment - the direction of states
## initialize to 1 or increasing
inc = 1
 
## Set prev_input's initial value to 2
prev_input=2
 
## This while loop constantly looks for button input (presses)
while True:
 
    ## When state toggle button is pressed
    if ( GPIO.input(16) == True ):
        #logging.warning('button 1 pressed...')
        ## If increment is increasing, increase state by 1 each press
        if (inc == 1):
            state = state + 1;
            ## If increment is decreasing (0), decrease state by 1 each press
        else:
            state = state - 1;
 
        ## Reached the max state, time to decrease state
        if (state == 3):
            inc = 0
            prev_input=1 ## Keeps a reset button phrase from executing when state shifts down to 2
            #streamer.log("prev_input",prev_input) ## Stream prev_input when changed
            #streamer.log("increment", inc) ## Stream increment when changed; "stream name", value
        ## Reached the min state, time to increase state
        elif (state == 0):
            inc = 1
            prev_input=2 ## Makes all reset button phrases executable
            #streamer.log("prev_input",prev_input) ## Stream prev_input when changed
            #streamer.log("increment", inc) ## Stream increment when changed
 
        ## Define state 1
        if (state == 1):
            GPIO.output(7, GPIO.LOW) ## LED on
            GPIO.output(11, GPIO.HIGH) ## LED off
            GPIO.output(13, GPIO.HIGH) ## LED off
            prev_input=2 ## Makes all reset button phrases executable
            #streamer.log("state",state) ## Stream current state
            #streamer.log("increment",inc) ## Stream current increment
            #streamer.log("prev_input",prev_input) ## Stream current prev_input
        ## Define state 2
        elif (state == 2):
            GPIO.output(7, GPIO.LOW) ## LED on
            GPIO.output(11, GPIO.LOW) ## LED on
            GPIO.output(13, GPIO.HIGH) ## LED off
            prev_input=2 ## Makes all reset button phrases executable
            #streamer.log("state",state) ## Stream current state
            #streamer.log("increment",inc) ## Stream current increment
            #streamer.log("prev_input",prev_input) ## Stream current prev_input
        ## Define state 3
        elif (state == 3):
            GPIO.output(7, GPIO.LOW) ## LED on
            GPIO.output(11, GPIO.LOW) ## LED on
            GPIO.output(13, GPIO.LOW) ## LED on
            #streamer.log("state",state) ## Stream current state
            #streamer.log("increment",inc) ## Stream current increment
            #streamer.log("prev_input",prev_input) ## Stream current prev_input
        ## If the state equals anything other than 1, 2, or 3 (0)
        else:
            GPIO.output(7, GPIO.HIGH) ## LED off
            GPIO.output(11, GPIO.HIGH) ## LED off
            GPIO.output(13, GPIO.HIGH) ## LED off
            #streamer.log("state",state) ## Stream current state
            #streamer.log("increment",inc) ## Stream current increment
            #streamer.log("prev_input",prev_input) ## Stream current prev_input
 
            #streamer.log("button_1", "pressed") ## Stream which button was pressed
        sleep(0.2); ## Wait 0.2 second before looking for another button input
 
    ## When reset button is pressed
    if ( GPIO.input(18) == True ):
        #logging.warning('reset Button pressed!')
        ## If 1 or 2 LEDs are on
        if (state == 1 or 2 and prev_input!=1):
            GPIO.output(7, GPIO.LOW) ## LED on
            GPIO.output(11, GPIO.LOW) ## LED on
            GPIO.output(13, GPIO.LOW) ## LED on
            prev_input=1 ## Keeps this phrase from executing when all LEDs are already on
            state=3 ## Change state to 3
            inc=0 ## Change increment to decreasing
                #streamer.log("state",state) ## Stream current state
                #streamer.log("increment",inc) ## Stream current increment
                #streamer.log("prev_input",prev_input) ## Stream current prev_input
            #streamer.log("phrase",1) ## used to see when each phrase was executing
            ## If no LEDs are on
        elif (state == 0 and prev_input!=0):
            GPIO.output(7, GPIO.LOW) ## LED on
            GPIO.output(11, GPIO.LOW) ## LED on
            GPIO.output(13, GPIO.LOW) ## LED on
            prev_input=1 ## Keeps this phrase from executing immediately after the state is set to 0
            state=3 ## Change state to 3
            inc=0 ## Change increment to decreasing
                #streamer.log("state",state) ## Stream current state
                #streamer.log("increment",inc) ## Stream current increment
                #streamer.log("prev_input",prev_input) ## Stream current prev_input
            #streamer.log("phrase",2) ## used to see when each phrase was executing
            ## If all LEDs are on
        elif (state == 3 and prev_input!=0):
            GPIO.output(7, GPIO.HIGH) ## LED off
            GPIO.output(11, GPIO.HIGH) ## LED off
            GPIO.output(13, GPIO.HIGH) ## LED off
            prev_input=0 ## Keeps this phrase from executing immediately after the state is set to 3
            state=0 ## Change state to 0
            inc=1 ## Change increment to increasing
                #streamer.log("state",state) ## Stream current state
                #streamer.log("increment",inc) ## Stream current increment
                #streamer.log("prev_input",prev_input) ## Stream current prev_input
                #streamer.log("phrase",3) ## used to see when each phrase was executing
 
            #streamer.log("button_2(bullseye)", "pressed") ## Stream which button was pressed
        sleep(0.2); ## Wait 0.2 second before looking for another button input
            #streamer.close()
