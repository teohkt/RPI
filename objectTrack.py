'''
Work in Porgress
Reference: https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/

'''

from collections import deque #Deque is a list like data structure with fast appends and pops to maintain the list of past N(x,y) locations. This is for the trail of the object
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils #Collection of OpenCV functions made easier. Designed by Adrian from pyimagesearch.com
import time

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")

#--buffer tells us the mac size of the deque, which is the trail being displayed
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

#range of colours to track, this was identified through bgr_hsv_converter.py and tested with colorDetection.py
#HSV colour codes
lower_range = (50, 100, 100)
upper_range = (70, 255, 255)

#setting the trail
pts = deque(maxlen=args["buffer"])

#if video file not supplied, activate the webcam. Location of webcam was tested in simpleCamTest.py
if not args.get("video", False):
    vs = VideoStream(src=0).start() #VideoStream is from imutils.video
else:
    vs = cv2.VideoCapture(args["video"])
    
#allow the camera or video file to warm up    
time.sleep(2.0)

while True:
    '''
    grab the current frame. this is the read method of our camera pointer,
    which returns a tuple (grabbed,frame). The first entry is grabbed,
    which is a boolean for if the read was successful or not. The second, frame,
    is the video frame
    '''
    frame = vs.read()
    frame = cv2.flip(frame, -1) #this is to rotate the image 180 degrees because of my setup
    
    #handle the frame from VideoStream or VideoCapture
    frame = frame[1] if args.get("video", False) else frame
    
    #when viewing a video, when we reach the end, there will be no more frames. We would then need to break out
    if frame is None:
        break
    
    #resize the frame, smaller frame allows for faster processing
    frame = imutils.resize(frame, width = 1000)
    
    #Bluring the frame reduces high frequency noise to focus on the structural objects 
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    
    #convert to hsv
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    #construct a mask for the specified color. erode and dilate reduce any blobs that may be left within the mask
    mask = cv2.inRange(hsv, lower_range, upper_range)
    mask = cv2.erode(mask, None, iterations = 2)
    mask = cv2.dilate(mask, None, iterations = 2)
    
    #find the contour on the mask and initialize the current (x,y) center of the object
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None
    
    # only proceeds if at least one contour was found
    if len(cnts) > 0:
        #find the largest contour in the mask, then use it to communicate the minimum
        #enclosing circle and centroid
        c = max(cnts, key = cv2.contourArea)
        ((x,y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        
        #only proceed if the radius meets a minimum size
        if radius > 10:
            #draw the circle and centroid on the frame and update list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius), (255, 255, 0), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            
    #update the pointers queue
    pts.appendleft(center)
    '''
    #loop over the set of tracked points
    for i in range(1, len(pts)):
        #if either of the tracked points is None, ignore them
        if pts[i-1] is None or pts[i] is None:
            continue
        
        #otherwise, compute the thickenss of the line and draw the connecting lines
        thickness = int(np.sqrt(args["buffer"]/float(i+1)) * 2.5)
        cv2.line(frame, pts[i-1], pts[i], (0, 0 ,225), thickness)
    '''    
    #show the frame on our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
 
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
 
    # if we are not using a video file, stop the camera video stream
if not args.get("video", False):
    vs.stop()
 
# otherwise, release the camera
else:
    vs.release()
 
# close all windows
cv2.destroyAllWindows()    

    
            
            