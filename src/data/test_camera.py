import cv2 as cv
import os
import sys
import time

# placeholder for object class
if len(sys.argv) < 2:
    print("Please enter the source camera index")
    exit()

use_pi_cam = False
source = 0
if len(sys.argv) >= 2:
    source_str = str(sys.argv[1])
    if source_str == "file":
        source = str(sys.argv[2])
        print("video from file:", source)
    else:
        source = int(source_str)
        print("source:", source)

        for i in range(1, len(sys.argv)):
            optional_param = str(sys.argv[i])
            if optional_param == "pi-cam":
                use_pi_cam = True

# override source if raspberry camera
if use_pi_cam:
    print("---\nraspberri camera\n----")
    source = f"nvarguscamerasrc sensor-id={source} ! video/x-raw(memory:NVMM), width=3820," \
             " height=2464, framerate=21/1, format=NV12 !" \
             " nvvidconv flip-method=2 !" \
             " video/x-raw, width=800, height=600, format=BGRx !" \
             " videoconvert ! video/x-raw, format=BGR ! appsink"

cap = cv.VideoCapture(source)

# does not seem to work for video
cap.set(3, 640)
cap.set(4, 480)

print("hello")

while True:
    _, frame = cap.read()
    cv.imshow('myCam', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()