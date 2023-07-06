#!/usr/bin/python3
import goesimages
import time

force_refresh = False
delay = 300 # Delay in seconds

while True:
    if goesimages.getjpgNumber() < goesimages.num_images / 2 or force_refresh == True:
        force_refresh = False
        print('Low number of buffer images... resetting.')
        goesimages.start()
    else:
        time.sleep(delay)
        goesimages.maintain()
