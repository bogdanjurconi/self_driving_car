#!/usr/bin/env python

import time
import robohat
import sys
import tty
import termios
import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('face_cascade.xml')
stop_cascade = cv2.CascadeClassifier('stop_cascade.xml')

cap = cv2.VideoCapture(0)

speed = 20

robohat.init()

initLineL = robohat.irLeftLine()
initLineR = robohat.irRightLine()

direction = 'forward'

is_started = False
is_stopped = False

i = 0

print('Powering up')

try:
	while True:
		print('Running')
		ret, img = cap.read()
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		
		# look for faces to start it
		if (is_started is False):
			faces = face_cascade.detectMultiScale(gray, 1.3, 5)
			print('Detecting faces')
			
			for (x,y,w,h) in faces:
				cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
				print('Starting up')
				is_started = True
				print('is_started is {}'.format(is_started))
		
		# look for stop sign when moving forward
		if (is_started is True and direction is 'forward'):
			print('Is started, looking for stops')
			stops = stop_cascade.detectMultiScale(gray, 1.3, 50)

			for (x,y,w,h) in stops:
				cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
				print('We are stopping')
				is_stopped = True
		
		# cv2.imwrite('images/image-{}.png'.format(str(i).zfill(5)), img)
		
		if (is_started is True and is_stopped is False):
			newLineL = robohat.irRightLine()
			print('Left is {}'.format(newLineL))

			newLineR = robohat.irLeftLine()
			print('Right is {}'.format(newLineR))

			if (newLineL is True and newLineR is True):
				direction = 'forward'

			if (newLineL is False and (direction is 'forward' or direction is 'spin-left')):
				print('Spinning left')
				direction = 'spin-left'
				robohat.spinLeft(65)

			if (newLineR is False  and (direction is 'forward' or direction is 'spin-right')):
				print('Spinning right')
				direction = 'spin-right'
				robohat.spinRight(65)

			if (direction is 'forward'):
				print('Moving forward')
				robohat.forward(speed)

		if (is_stopped is True):
			print('Stopping and exiting')
			break
		
		i += 1

except KeyboardInterrupt:
	print

finally:
	robohat.cleanup()
