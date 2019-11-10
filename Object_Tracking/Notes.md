# Testing out the Camera

I got errors from cv2.videocapture(0), 'VIDEOIO ERROR: V4L: can't open camera by index 0'. I tried changing to videocapture(-1), but then the error message was 'can't find camera device. The solution was to allow permissions to access the camera (ontop of Preferences > Raspberry Pi Configuration)

### sudo modprobe bcm2835-v4l2

I got errors from import cv2, 'ImportError: No module named 'cv2' although when I tested it in terminal, I could import cv2. Turns out, cv2.so needs to be exactly in /usr/local/lib/python3.5/site-packages/. You can gain root permission through 

### gksudo pcmanfm

# Capture an image:

### raspistill -o output.jpg

Captured an image of a highlighter cap.
Uploaded image to colorcodepicker.com to find the RBG code of it. This returned 36, 177, 41
After running python3 bgr_hsv_converter.py 36 177 41

Output:
Lower bound is:
[50, 100, 100]

Upper bount is:
[70, 255, 255]

We can test to see if our HSV numbers are correct by applying a mask that removes everything but these colours.
