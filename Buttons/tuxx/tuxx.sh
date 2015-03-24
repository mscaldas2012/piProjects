#!/bin/bash

# tuxx:
#	Tux Crossing. A variant on the UK "Pelican" crossing for
#	pedestrians going over roads.
#
#	There is a set of Red, Yellow (sometimes called amber) and
#	Green traffic lights to control the traffic, and a "Red Man"
#	and "Green Man" indicators for pedestrians, and a button for
#	them to push.
#	Push the button and the lights cycle to Red, then the Green Man
#	comes on (often with a beeping sound), then afte a short while
#	the Green man starts to flash, meaning to not start crossing,
#	and the Yellow traffic light flashes too - meaning that if the
#	crossing is clear, traffic can pass... Then after a few more seconds
#	the flashing stops and it revers to Go for traffic and Stop for
#	pedestrians.
#
#	Gordon Henderson, June 2012

# Our lamps:
#	(These are wiringPi pin numbers)

     red=0
  yellow=1
   green=2
  redMan=3
greenMan=4

# The input button

button=8


# setup:
#	Program the GPIO correctly and initialise the lamps
#######################################################################

setup ()
{
  echo Setup
  for i in $red $yellow $green $redMan $greenMan ; do gpio mode  $i out ; done
  for i in $red $yellow $green $redMan $greenMan ; do gpio write $i   0 ; done
  gpio write $green  1
  gpio write $redMan 1
  gpio mode  $button in
}

# waitButton:
#	Wait for the button to be pressed. Because we have the GPIO
#	pin pulled high, we wait for it to go low to indicate a push.
#######################################################################

waitButton ()
{
  echo -n "Waiting for button ... "
  while [ `gpio read $button` = 1 ]; do
    sleep 0.1
  done
  echo "Got it"
}

# stopTraffic:
#	Cycle the traffic lights from Green to Red
#######################################################################

stopTraffic ()
{
  echo -n "Stopping traffic ... "
  gpio write $green  0
  gpio write $yellow 1
  sleep 2
  gpio write $yellow 0
  gpio write $red    1
  sleep 2
  echo "Stopped"
}

# walk:
#	Signal the red/green man to walk and when time is up,
#	start the traffic light sequence to let the traffic move again
#######################################################################

walk ()
{
  echo "Walk now ... "
  gpio write $redMan   0
  gpio write $greenMan 1
  sleep 10
  gpio write $red    0
  gpio write $yellow 1
  echo "Walked"
}

# graceTime:
#	This is the time when the green man is flashing, and the yellow
#	traffic light is also flashing - to signal to pedestrians to not
#	start to cross and to drivers that they can move on if the 
#	crossing is clear.
#######################################################################

graceTime ()
{
  echo "Grace time ... "
  for i in `seq 0 7` ; do
    sleep 0.5
    gpio write $greenMan 0
    gpio write $yellow   0
    sleep 0.5
    gpio write $greenMan 1
    gpio write $yellow   1
  done
  echo "time up!"
}

# startTraffic:
#	Back to the Red Man and Green traffic light
#######################################################################

startTraffic ()
{
  echo "Starting traffic ... "
  gpio write $greenMan 0
  gpio write $redMan   1
  sleep 0.5
  gpio write $yellow 0
  gpio write $green  1
  echo "Going"
}


#######################################################################
# The main program
#	Call our setup routing once, then sit in a loop, waiting for
#	the button to be pressed then executing the sequence.
#######################################################################

setup
while true; do
  waitButton
  stopTraffic
  walk
  graceTime
  startTraffic
done
