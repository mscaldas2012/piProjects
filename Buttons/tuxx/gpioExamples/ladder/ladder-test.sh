#!/bin/bash

setup ()
{
  echo Setup
  for i in 0 1 2 3 4 5 6 7 10 11 12 13 ; do gpio mode  $i out ; done
}

setup
while true; do
  for i in 0 1 2 3 4 5 6 7 10 11 12 13 ; do
    gpio write $i   0
    sleep 0.1
  done
  for i in 0 1 2 3 4 5 6 7 10 11 12 13 ; do
    gpio write $i   1
    sleep 0.1
  done
done
