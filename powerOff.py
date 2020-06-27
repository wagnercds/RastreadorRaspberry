#!/usr/bin/env python

import time
import RPi.GPIO as GPIO
import os

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN, pull_up_down = GPIO.PUD_UP)

while True:
	if GPIO.input(17) == 0:
		time.sleep(5)
		if GPIO.input(17) == 0:
			os.system("init 0")
		

