import cv2 as cv
import os
import sys
import time

# placeholder for object class
if len(sys.argv) < 2:
    print("Please enter the name for the object.")
    exit()

source = 0
if len(sys.argv) == 3:
    source = int(sys.argv[2])

obj = str(sys.argv[1])

cap = cv.VideoCapture(source)
#time.sleep(10)
cap.set(3, 640)
cap.set(4, 480)

# directry to output latest_label.txt file and raw images 
PATH = '../../data/raw/'

# create data folder for output frames
output_path = PATH + obj
if not os.path.exists(output_path):
    os.makedirs(output_path)
else:
    print("An obejct with the same name exists; please use a different name and try again:)")
    exit()

# write the class name to latest_label.txt
txt_file_path = PATH + 'latest_label.txt'
with open(txt_file_path, 'w') as file:
    file.write(obj)

# tracker = cv.TrackerMOSSE_create()
tracker = cv.TrackerCSRT_create()
# tracker = cv.TrackerGOTURN_create()
# read initial frame for customized bounding box
ret, frame = cap.read()
bbox = cv.selectROI('Tracking', frame, False)
initial_txt = 'Please draw a bounding box'
cv.putText(frame, initial_txt, (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv.LINE_AA)

# initialzie tracker using the bounding box
tracker.init(frame, bbox)

def drawBbox(frame, bbox):
    """
    A function that draws boudning box on a frame based on the bbox dimensions.
    """
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv.rectangle(frame, (x, y), ((x + w), (y+h)), (255, 0, 0), 2, 1)

i = 0
while True:
    # read frame
    ret, frame = cap.read()
    # get bbox and updates tracker
    ret, bbox = tracker.update(frame)
    if ret:
        # draw bbox if traking succeeded
        drawBbox(frame, bbox)
    else:
        # print missing if not
        cv.putText(frame, 'lost', (100, 145), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv.LINE_AA)
    # display status
    txt = 'Capturing training samples'
    cv.putText(frame, txt, (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv.LINE_AA)
    
    ##### ADD IMAGE CAPTURE and annotation CODE HERE ######
    #######################################################
    cv.imwrite(output_path+"/"+obj+"_"+str(i)+".jpg",frame)
    i += 1    
    
    # append the bbox coordinate to bbox_information.txt
    bbox_coordinate = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    bbox_path = PATH + 'bbox_information.txt'
    with open(bbox_path, 'a') as file:
        file.write(" ".join([str(a) for a in bbox_coordinate]) + '\n')


    #######################################################
    cv.imshow('tracking', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
