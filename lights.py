#!/usr/bin/python

from __future__ import print_function
from fadelib3 import FadeLIB
import time
import random
import argparse
import sys

COLORS = None
NUM_LEDS = 46

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b",
        "--brightness",
        help="Set the brightness from 0 to 100",
        default=100,
        type=int
    )
    parser.add_argument(
        "-i",
        "--immediate",
        help="Immediately change colors (no transition)",
        default=False,
        action="store_true"
    )
    parser.add_argument(
        "-d",
        "--delay",
        help="Delay time between color changes in seconds.",
        default=5,
        type=float
    )
    parser.add_argument(
        "theme",
        help="Set the theme to display.  Options are: christmas, independence, halloween, usmc"
    )

    args = parser.parse_args()

    brightness = args.brightness
    brightness /= 100

    f = FadeLIB(BRIGHTNESS=brightness, NUM_LEDS=NUM_LEDS)

    if not f.THEME.get(args.theme):
        print("Theme {} does not exist.".format(args.theme))
        sys.exit(1)

    #f.PIXELS = f.fill_solid('WHITE')
    while True:
        f.transition2(f.theme(args.theme), duration=args.delay, immediate=args.immediate)

        #f.transition2(f.theme('christmas'),DURATION=10)

        #f.PIXELS = f.theme('christmas')
        #f.update()
        #f.update()
        #Need to issue 2 rapid updates, otherwise the lights try to do a slow transition

        #time.sleep(10)
        #f.PIXELS = f.theme('usmc')
        #f.PIXELS = f.fill_rainbow()
        #f.PIXELS = f.fill_solid('ORANGE')
        #f.fill_rainbow()
        
        #f.transition2(f.theme('christmas'), duration=1)
        #f.roll('christmas')

        f.update()
        f.update()

        secondsDelay = 0 

        if secondsDelay > 0:
            delay = random.randrange(secondsDelay * 1000)
            time.sleep(float(delay)/float(1000))

def countdown(secs):
    for sec in range(secs):
        print(secs-sec)
        time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nKeyboardInterrupt caught.')
        fc = FadeLIB(BRIGHTNESS=1.0)
        fc.blackout()


