#!usr/bin/python

import cv2 as cv
import os
import sys

cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 680)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 680)

# placeholder for object class
if len(sys.argv) == 1:
    print("Please enter the name for the object.")
    exit()

object = str(sys.argv[1])

# create data folder for output frames
output_path = '../../data/raw/{}/'.format(object)
if not os.path.exists(output_path):
    os.makedirs(output_path)
else:
    print("An obejct with the same name exists; please use a different name and try again:)")
    exit()

# Preparation countdown
countdown = 110

i = 0
# capture video from camera
while(True):

    # Capture frame-by-frame
    ret, frame = cap.read()

    # just a note, we can make this adaptive to the resolution above!
    x, y, w, h = 100, 100, 600, 400

    if countdown > 0:
        color = (255, 0, 0)
        frame = cv.rectangle(frame, (x, y), (x + w, y + h), color, 5)
        countdown -= 1
    else:
        color = (255, 223, 0)
        frame = cv.rectangle(frame, (x, y), (x + w, y + h), color, 5)
        cv.imwrite(output_path+"/"+object+"_"+str(i)+".jpg",frame)
        i += 1

    cv.imshow('output_', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
