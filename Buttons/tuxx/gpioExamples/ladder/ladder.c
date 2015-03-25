/*
 * ladder.c:
 *	ladder - Capacitor charging simulation - ladder climb game
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
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <math.h>

#include <wiringPi.h>

#ifndef	TRUE
#  define	TRUE	(1==1)
#  define	FALSE	(1==2)
#endif

#undef	DEBUG

// The input button

#define	BUTTON		8


// Map the LEDs to the hardware pins
//	using wiringPi pin numbers here

const int ledMap [12] =
{
  13, 12, 11, 10, 7, 6, 5, 4, 3, 2, 1, 0
} ;


// Some constants for our circuit simulation

const double vBatt      =      9.0 ;	// Volts (ie. a PP3)
const double capacitor  =      0.001 ;	// 1000uF
const double rCharge    =   2200.0 ;	// ohms
const double rDischarge =  68000.0 ;	// ohms
const double timeInc    =      0.01 ;	// Seconds

double vCharge, vCap, vCapLast ;



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
    fprintf (stderr, "ladder: Need to be root to run (sudo?)\n") ;
    exit (0) ;
  }

  if (wiringPiSetup () == -1)
    exit (1) ;

  for (i = 0 ; i < 12 ; ++i)
  {
    digitalWrite (ledMap [i], 0) ;
    pinMode (ledMap [i], OUTPUT) ;
  }

  pinMode (BUTTON, INPUT) ;

// Calculate the actual charging voltage - standard calculation of
//	vCharge = r2 / (r1 + r2) * vBatt
//
//
//   -----+--- vBatt
//        |
//        R1
//        |
//        +---+---- vCharge
//        |   |
//        R2  C
//        |   |
//   -----+---+-----

  vCharge = rDischarge / (rCharge + rDischarge) * vBatt ;

// Start with no charge

  vCap    = vCapLast = 0.0 ;
}


/*
 * introLeds
 *	Put a little pattern on the LEDs to start with
 *********************************************************************************
 */

void introLeds (void)
{
  int i, j ;


  printf ("Pi Ladder\n") ;
  printf ("=========\n\n") ;
  printf ("       vBatt: %6.2f volts\n", vBatt) ;
  printf ("     rCharge: %6.0f ohms\n", rCharge) ;
  printf ("  rDischarge: %6.0f ohms\n", rDischarge) ;
  printf ("     vCharge: %6.2f volts\n", vCharge) ;
  printf ("   capacitor: %6.0f uF\n", capacitor * 1000.0) ;

// Flash 3 times:

  for (j = 0 ; j < 3 ; ++j)
  {
    for (i = 0 ; i < 12 ; ++i)
      digitalWrite (ledMap [i], 1) ;
    delay (500) ;
    for (i = 0 ; i < 12 ; ++i)
      digitalWrite (ledMap [i], 0) ;
    delay (100) ;
  }

// All On

  for (i = 0 ; i < 12 ; ++i)
    digitalWrite (ledMap [i], 1) ;
  delay (500) ;

// Countdown...

  for (i = 11 ; i >= 0 ; --i)
  {
    digitalWrite (ledMap [i], 0) ;
    delay (100) ;
  }
  delay (500) ;
}


/*
 * winningLeds
 *	Put a little pattern on the LEDs to start with
 *********************************************************************************
 */

void winningLeds (void)
{
  int i, j ;

// Flash 3 times:

  for (j = 0 ; j < 3 ; ++j)
  {
    for (i = 0 ; i < 12 ; ++i)
      digitalWrite (ledMap [i], 1) ;
    delay (500) ;
    for (i = 0 ; i < 12 ; ++i)
      digitalWrite (ledMap [i], 0) ;
    delay (100) ;
  }

// All On

  for (i = 0 ; i < 12 ; ++i)
    digitalWrite (ledMap [i], 1) ;
  delay (500) ;

// Countup...

  for (i = 0 ; i < 12 ; ++i)
  {
    digitalWrite (ledMap [i], 0) ;
    delay (100) ;
  }
  delay (500) ;
}


/*
 * chargeCapacitor: dischargeCapacitor:
 *	Add or remove charge to the capacitor.
 *	Standard capacitor formulae.
 *********************************************************************************
 */

void chargeCapacitor (void)
{
  vCap = (vCapLast - vCharge) *
	exp (- timeInc / (rCharge * capacitor)) + vCharge ;

#ifdef	DEBUG
  printf ("+vCap: %7.4f\n", vCap) ;
#endif

  vCapLast = vCap ;
}

void dischargeCapacitor (void)
{
  vCap = vCapLast *
	exp (- timeInc / (rDischarge * capacitor)) ;

#ifdef	DEBUG
  printf ("-vCap: %7.4f\n", vCap) ;
#endif

  vCapLast = vCap ;
}


/*
 * ledBargraph:
 *	Output the supplied number as a bargraph on the LEDs
 *********************************************************************************
 */

void ledBargraph (double value, int topLedOn)
{
  int topLed = (int)floor (value / vCharge * 12.0) + 1 ;
  int i ;

  if (topLed > 12)
    topLed = 12 ;

  if (!topLedOn)
    --topLed ;

  for (i = 0 ; i < topLed ; ++i)
    digitalWrite (ledMap [i], 1) ;

  for (i = topLed ; i < 12 ; ++i)
    digitalWrite (ledMap [i], 0) ;
}


/*
 * ledOnAction:
 *	Make sure the leading LED is on and check the button
 *********************************************************************************
 */

void ledOnAction (void)
{
  if (digitalRead (BUTTON) == LOW)
  {
    chargeCapacitor () ;
    ledBargraph (vCap, TRUE) ;
  }
}


/*
 * ledOffAction:
 *	Make sure the leading LED is off and check the button
 *********************************************************************************
 */

void ledOffAction (void)
{
  dischargeCapacitor () ;

// Are we still pushing the button?

  if (digitalRead (BUTTON) == LOW)
  {
    vCap = vCapLast = 0.0 ;
    ledBargraph (vCap, FALSE) ;

// Wait until we release the button

    while (digitalRead (BUTTON) == LOW)
      delay (10) ;
  }
}


/*
 ***********************************************************************
 * The main program
 ***********************************************************************
 */

int main (void)
{
  unsigned int then, ledOnTime, ledOffTime ;
  unsigned int ourDelay = (int)(1000.0 * timeInc) ;
  
  setup     () ;
  introLeds () ;

// Setup the LED times - TODO reduce the ON time as the game progresses

  ledOnTime  = 1000 ;
  ledOffTime = 1000 ;

// This is our Gate/Squarewave loop

  for (;;)
  {

// LED ON:

    (void)ledBargraph (vCap, TRUE) ;
    then = millis () + ledOnTime ;
    while (millis () < then)
    {
      ledOnAction () ;
      delay       (ourDelay) ;
    }

// Have we won yet?
//	We need vCap to be in the top 12th of the vCharge

    if (vCap > (11.0 / 12.0 * vCharge))	// Woo hoo!
    {
      winningLeds () ;
      while (digitalRead (BUTTON) == HIGH)
	delay (10) ;
      while (digitalRead (BUTTON) == LOW)
	delay (10) ;
      vCap = vCapLast = 0.0 ;
    }

// LED OFF:

    (void)ledBargraph (vCap, FALSE) ;
    then = millis () + ledOffTime ;
    while (millis () < then)
    {
      ledOffAction () ;
      delay        (ourDelay) ;
    }

  }

  return 0 ;
}
