/*
 * tuxx.c:
 *	https://projects.drogon.net/raspberry-pi/gpio-examples/
 *
 *	Copyright (c) 2012 Gordon Henderson
 *********************************************************************************
 *
 *   This program is free software: you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation, either version 3 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 ***********************************************************************
 *
 *	Tux Crossing. A variant on the UK "Pelican" crossing for
 *	pedestrians going over roads.
 *
 *	There is a set of Red, Yellow (sometimes called amber) and
 *	Green traffic lights to control the traffic, and a "Red Man"
 *	and "Green Man" indicators for pedestrians, and a button for
 *	them to push.
 *
 *	Push the button and the lights cycle to Red, then the Green Man
 *	comes on (often with a beeping sound), then afte a short while
 *	the Green man starts to flash, meaning to not start crossing,
 *	and the Yellow traffic light flashes too - meaning that if the
 *	crossing is clear, traffic can pass... Then after a few more seconds
 *	the flashing stops and it revers to Go for traffic and Stop for
 *	pedestrians.
 *
 ***********************************************************************
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <wiringPi.h>

// Our lamps:
//	(These are wiringPi pin numbers)

#define	RED		0
#define	YELLOW		1
#define	GREEN		2
#define	RED_MAN		3
#define	GREEN_MAN	4

// The input button

#define	BUTTON		8


/*
 * setup:
 *	Program the GPIO correctly and initialise the lamps
 ***********************************************************************
 */

void setup (void)
{
  int i ;

  if (geteuid () != 0)
  {
    fprintf (stderr, "tuxx: Need to be root to run (sudo?)\n") ;
    exit (0) ;
  }

  if (wiringPiSetup () == -1)
    exit (1) ;

  printf ("Setup ... ") ; fflush (stdout) ;
  for (i = 0 ; i < 5 ; ++i)
  {
    pinMode (i, OUTPUT) ;
    digitalWrite (i, 0) ;
  }
  digitalWrite (GREEN, 1) ;
  digitalWrite (RED_MAN, 1) ;
  pinMode (BUTTON, INPUT) ;

  printf ("OK\n") ;
}

/*
 * waitButton:
 *	Wait for the button to be pressed. Because we have the GPIO
 *	pin pulled high, we wait for it to go low to indicate a push.
 ***********************************************************************
 */

void waitButton (void)
{
  printf ("Waiting for button ... ") ; fflush (stdout) ;
  while (digitalRead (BUTTON) == HIGH)
    delay (100) ;
  printf ("Got it\n") ;
}

/*
 * stopTraffic:
 *	Cycle the traffic lights from Green to Red
 ***********************************************************************
 */

void stopTraffic ()
{
  printf ("Stopping traffic ... ") ; fflush (stdout) ;
  digitalWrite (GREEN,  0) ;
  digitalWrite (YELLOW, 1) ;
  delay (2000) ;
  digitalWrite (YELLOW, 0) ;
  digitalWrite (RED,    1) ;
  delay (2000) ;
  printf ("Stopped\n") ;
}

/*
 * walk:
 *	Signal the red/green man to walk and when time is up,
 *	start the traffic light sequence to let the traffic move again
 ***********************************************************************
 */

void walk ()
{
  printf ("Walk now ... ") ; fflush (stdout) ;

  digitalWrite (RED_MAN,   0) ;
  digitalWrite (GREEN_MAN, 1) ;
  delay (10000) ;
  digitalWrite (RED,    0) ;
  digitalWrite (YELLOW, 1) ;

  printf ("Walked\n") ;
}

/*
 * graceTime:
 *	This is the time when the green man is flashing, and the yellow
 *	traffic light is also flashing - to signal to pedestrians to not
 *	start to cross and to drivers that they can move on if the 
 *	crossing is clear.
 ***********************************************************************
 */

void graceTime ()
{
  int i ;

  printf ("Grace time ... ") ; fflush (stdout) ;

  for (i = 0 ; i < 8 ; ++i)
  {
    delay (500) ;
    digitalWrite (GREEN_MAN, 0) ;
    digitalWrite (YELLOW,    0) ;
    delay (500) ;
    digitalWrite (GREEN_MAN, 1) ;
    digitalWrite (YELLOW,    1) ;
  }
  printf ("time up!\n") ;
}

/*
 * startTraffic:
 *	Back to the Red Man and Green traffic light
 ***********************************************************************
 */

void startTraffic ()
{
  printf ("Starting traffic ... ") ; fflush (stdout) ;

  digitalWrite (GREEN_MAN, 0) ;
  digitalWrite (RED_MAN,   1) ;
  delay (500) ;
  digitalWrite (YELLOW, 0) ;
  digitalWrite (GREEN,  1) ;

  printf ("Going\n") ;
}


/*
 ***********************************************************************
 * The main program
 *	Call our setup routing once, then sit in a loop, waiting for
 *	the button to be pressed then executing the sequence.
 ***********************************************************************
 */

int main (void)
{
  setup () ;
  for (;;)
  {
    waitButton   () ;
    stopTraffic  () ;
    walk         () ;
    graceTime    () ;
    startTraffic () ;
  }
}
