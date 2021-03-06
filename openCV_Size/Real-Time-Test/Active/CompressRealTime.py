'''
    coding by

                    /$$$$$$                /$$   /$$ /$$ /$$$$$$$ 
                   /$$__  $$              | $$$ | $$| $/| $$__  $$
                  | $$  \ $$ /$$$$$$/$$$$ | $$$$| $$|_/ | $$  \ $$
                  |$$$$$$$$ | $$_  $$_  $$| $$ $$ $$    | $$  | $$
                  | $$__  $$| $$ \ $$ \ $$| $$  $$$$    | $$  | $$
                  | $$  | $$| $$ | $$ | $$| $$\  $$$    | $$  | $$
                  | $$  | $$| $$ | $$ | $$| $$ \  $$    | $$$$$$$/
                  |__/  |__/|__/ |__/ |__/|__/  \__/    |_______/ 
                                                
                         *!*!THIS PROGRAME IS COPYLEFT!*!*
     You can use anywhere. But please add this comment title or end of the code
                            [original code by Amn'D]

           Amn'D-LEGO Bean Size Check(Compress) release : v1.0.0 (May 26 2018)
        Amn'd-CV?X!Size is open source cleaning dictoray. This code made by AmN'D

                    FACEBOOK : https://facebook.com/insung.bahk
                      GITHUB : https://github.com/insung3511
                          EMAIL : insung3511@icloud.com
'''
# Okay, this print show ["Program Start!"]
print ("======<~+START+~>======")

# And this library make code doing well
from scipy.spatial import distance as dist
from imutils import perspective
from collections import deque
from imutils import contours
import numpy as np
import webbrowser
import argparse
import datetime
import logging
import imutils
import time
import csv
import cv2
import sys

# This function make dot.
# These dots, draw preview can usally.
def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

def TakePic():
	camera = cv2.VideoCapture(0)
	frame = camera.read()[1]
	cv2.imwrite(filename='ObjectPic.JPG', img=frame)

# main function M-A-I-N code.
# This code that measuring the size of LEGO beam by size.
def main():
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", required=True,
                help="path to the input image")
	ap.add_argument("-w", "--width", type=float, required=True,
                help="width of the left-most object in the image (in inches)")

	args = vars(ap.parse_args())

	# openCV image Setting
	image = cv2.imread("ObjectPic.jpg")
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5, 5), 0)

	# Here is also image setting
	edged = cv2.Canny(gray, 50, 80)
	edged = cv2.dilate(edged, None, iterations=1)
	edged = cv2.erode(edged, None, iterations=1)
	
	cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]

	(cnts, _) = contours.sort_contours(cnts)
	pixelsPerMetric = None

	# open save file dictory 
	# and create counting number
	objectCount = 0
	file = open('./Results/NAME_HERE!.csv', 'w')

	# Create 2beam ~ 9beam number
	# This number is used for lines 150 to 164.
	TwoBeam = 0
	FiveBeam = 0
	SevenBeam = 0
	NineBeam = 0

	# The annotations of this function are annotations written by Andrian. # 
	# Also part of the main function code is written by Andrian. #
	# 					*Thank to Andrian*						#
	
	# loop over the contours individually
	for c in cnts:
		# if the contour is not sufficiently large, ignore it
		if cv2.contourArea(c) < 100:
		    continue

		# compute the rotated bounding box of the contour
		orig = image.copy()
		box = cv2.minAreaRect(c)
		box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
		box = np.array(box, dtype="int")

		# order the points in the contour such that they appear
		# in top-left, top-right, bottom-right, and bottom-left
		# order, then draw the outline of the rotated bounding
		# box
		box = perspective.order_points(box)
		cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

		# loop over the original points and draw them
		for (x, y) in box:
			cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)
        
		# unpack the ordered bounding box, then compute the midpoint
		# between the top-left and top-right coordinates, followed by
		# the midpoint between bottom-left and bottom-right coordinates
		(tl, tr, br, bl) = box
		(tltrX, tltrY) = midpoint(tl, tr)
		(blbrX, blbrY) = midpoint(bl, br)

		# compute the midpoint between the top-left and top-right points,
		# followed by the midpoint between the top-righ and bottom-right
		(tlblX, tlblY) = midpoint(tl, bl)
		(trbrX, trbrY) = midpoint(tr, br)

		# draw the midpoints on the image
	 	cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
		cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
		cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
		cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

		# draw lines between the midpoint
		cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
			(255, 0, 255), 2)
		cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
			(255, 0, 255), 2)

		# compute the Euclidean distance between the midpoints
		dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
		dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

		if pixelsPerMetric is None:
			pixelsPerMetric = dB / args["width"]
    
		dimA = dA / pixelsPerMetric
		dimB = dB / pixelsPerMetric

		cv2.putText(orig, "{:.1f}in".format(dimA),
			(int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
			0.65, (255, 255, 255), 2)
		cv2.putText(orig, "{:.1f}in".format(dimB),
			(int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
			0.65, (255, 255, 255), 2)

		RounddimB = round(dimB, 1)
		objectCount = objectCount + 1
		print " "
		print "Conuting Result : ", objectCount
		print "Length(dimA) : ", dimA, "| Width(dimB) : ", dimB
		print "dimB Round Result : ", RounddimB

		# Part which distinguishes the length of Lego beam
		# 		*Translate by Google Translator*
		if RounddimB <= 1.4:
				print "This beam is 2beam"
				TwoBeam = TwoBeam + 1

		elif RounddimB <= 3.5:
				print "This beam is 5beam"
				FiveBeam = FiveBeam + 1

		elif RounddimB <= 4.9:
				print "This beam is 7beam"
				SevenBeam = SevenBeam + 1

		elif RounddimB <= 6.0:
				print "This beam is 9beam"
				NineBeam = NineBeam + 1

		Messages = 'Length : ' + str(dimA) + ' | Width : ' + str(dimB) + ' | Count Number : ' + str(objectCount) + '\n'
		file.write(Messages)

		cv2.imshow("Image", orig)
		cv2.waitKey(0)
		print " 		"

if __name__ == "__main__":
	TakePic()
	main()

# E-N-D Program.. 
print("======<~+-END-+~>======")
