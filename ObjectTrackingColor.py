import cv2
import numpy as np

frame_width = 640
frame_height = 480

capture = cv2.VideoCapture(1)
capture.set(3, frame_width)
capture.set(4, frame_height)
dz = 1000
global image_counter

def empty(a):
    pass

cv2.namedWindow("HSV")
cv2.resizeWindow("HSV",640,240)
#UI Trackbars
cv2.createTrackbar("HUE Min", "HSV", 19,179,empty)
cv2.createTrackbar("HUE Max", "HSV", 35,179,empty)
cv2.createTrackbar("SAT Min", "HSV", 107,255,empty)
cv2.createTrackbar("SAT Max", "HSV", 255,255,empty)
cv2.createTrackbar("VALUE Min", "HSV", 89,255,empty)
cv2.createTrackbar("VALUE Max", "HSV", 255,255,empty)

#UI Trackbars
cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 640,240)
cv2.createTrackbar("Threshold1", "Parameters", 166,255,empty)
cv2.createTrackbar("Threshold2", "Parameters", 171,255,empty)
cv2.createTrackbar("Area", "Parameters", 3750,30000,empty)

#Def to stack images on UI
def imageStack(scale, image_arr):
    rows = len(image_arr)
    cols = len(image_arr[0])
    rows_avail = isinstance(image_arr[0], list)
    width = image_arr[0][0].shape[1]
    height = image_arr[0][0].shape[0]
    if rows_avail:
        for x in range(0, rows):
            for y in range(0, cols):
                if image_arr[x][y].shape[:2] == image_arr[0][0].shape[:2]:
                    image_arr[x][y] = cv2.resize(image_arr[x][y], (0, 0), None, scale, scale)
                else:
                    image_arr[x][y] = cv2.resize(image_arr[x][y], (image_arr[0][0].shape[1], image_arr[0][0].shape[0], None, scale, scale))
                if len(image_arr[x][y].shape) == 2: image_arr[x][y] = cv2.cvtColor(image_arr[x][y], cv2.COLOR_GRAY2BGR)
        image_blank = np.zeros((height, width, 3), np.uint8)
        hor = [image_blank]*rows
        hor_con = [image_blank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(image_arr[x])
        version = np.vstack(hor)
    else:
        for x in range(0, rows):
            if image_arr[x].shape[:2] == image_arr[0].shape[:2]:
                image_arr[x] = cv2.resize(image_arr[x], (0, 0), None, scale, scale)
            else:
                image_arr[x] = cv2.resize(image_arr[x], (image_arr[0].shape[1], image_arr[0], None, scale, scale))
            if len(image_arr[x].shape) == 2: image_arr[x] = cv2.cvtColor(image_arr[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(image_arr)
        version = hor
    return version

def getContours(image, image_countour):
    contours, hierarchy = cv2.findContours