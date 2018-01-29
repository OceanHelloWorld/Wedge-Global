# import the necessary packages
from scipy.spatial import distance as dist
from time import sleep
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import sys

PY3 = sys.version_info[0] == 3
if PY3:
    xrange = range
# !!! need to be deleted
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())

# lower and upper boundaries of colors
# yoko is red in HSV, dock is blue in HSV
yokoLower = (140, 100, 100)
yokoUpper = (180, 255, 255)
dockLower = (60, 100, 100)
dockUpper = (120, 255, 255)
# pts = deque(maxlen=args["buffer"])

# count
yoko_error_counter = 0;
dock_error_counter = 0;

def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])

# keep looping
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
        break

    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct a mask_yoko for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask_yoko
    mask_yoko = cv2.inRange(hsv, yokoLower, yokoUpper)
    mask_yoko = cv2.erode(mask_yoko, None, iterations=2)
    mask_yoko = cv2.dilate(mask_yoko, None, iterations=2)
    mask_dock = cv2.inRange(hsv, dockLower, dockUpper)
    mask_dock = cv2.erode(mask_dock, None, iterations=2)
    mask_dock = cv2.dilate(mask_dock, None, iterations=2)


    # find contours in the  and initialize the current
    # (x, y) center of the ball
    cnts_yoko = cv2.findContours(mask_yoko.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnts_dock = cv2.findContours(mask_dock.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]

    center_yoko = None
    center_dock = None
    # only proceed if at least one contour was found
    if len(cnts_yoko) > 0:
        # find the largest contour in the mask_yoko, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c_yoko = max(cnts_yoko, key=cv2.contourArea)
        ((x_yoko, y_yoko), radius_yoko) = cv2.minEnclosingCircle(c_yoko)
        M_yoko = cv2.moments(c_yoko)
        center_yoko = (int(M_yoko["m10"] / M_yoko["m00"]), int(M_yoko["m01"] / M_yoko["m00"]))
        # only proceed if the radius meets a minimum size
        if radius_yoko > 40 and radius_yoko < 150:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x_yoko), int(y_yoko)), int(radius_yoko),
                (0, 255, 255), 2)
            cv2.circle(frame, center_yoko, 5, (0, 0, 255), -1)
            yoko_error_counter = 0
            sleep(0.1)
        else:
            yoko_error_counter += 1
            print("yoko out", yoko_error_counter)
            if dock_error_counter > 20 and yoko_error_counter > 20:
                print("Yoko is out, contact the supervisor")
            sleep(0.1)

    if len(cnts_dock) > 0:
        # find the largest contour in the mask_yoko, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c_dock = max(cnts_dock, key=cv2.contourArea)

        ((x_dock, y_dock), radius_dock) = cv2.minEnclosingCircle(c_dock)

        M_dock = cv2.moments(c_dock)

        center_dock = (int(M_dock["m10"] / M_dock["m00"]), int(M_dock["m01"] / M_dock["m00"]))
        # only proceed if the radius meets a minimum size
        if radius_dock > 40 and radius_dock < 250:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x_dock), int(y_dock)), int(radius_dock),
                (100, 100, 255), 2)
            cv2.circle(frame, center_dock, 5, (0, 200, 55), -1)
            sleep(0.1)
            dock_error_counter = 0
            if radius_yoko > 40 and radius_yoko < 150:
                cv2.line(frame, (int(x_dock), int(y_dock)), (int(x_yoko), int(y_yoko)), (0, 0, 00), 4)
                distance = dist.euclidean((x_dock, y_dock), (x_yoko, y_yoko))
                (x_middle, y_middle) = midpoint((x_dock, y_dock), (x_yoko, y_yoko))
                cv2.putText(frame, "{:.1f}centimeters".format(distance), (int(x_middle), int(y_middle - 10)),cv2.FONT_HERSHEY_SIMPLEX, 0.55, (100, 200, 20), 2)
        else:
            dock_error_counter += 1
            print("dock out", dock_error_counter)
            if dock_error_counter > 20 and yoko_error_counter > 20:
                print("Yoko is out, contact the supervisor")
            sleep(0.1)

    # update the points queue
    # pts.appendleft(center_yoko)
    # pts.appendleft(center_dock)
    # ???
    # loop over the set of tracked points
    '''
    for i in xrange(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue
        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
    '''
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
