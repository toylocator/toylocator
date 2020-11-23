import cv2 as cv
import os
import sys
import time

def drawBbox(frame, bbox):
    """
    A function that draws bounding box on a frame based on the bbox dimensions.
    """
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv.rectangle(frame, (x, y), ((x + w), (y+h)), (255, 0, 0), 2, 1)


# placeholder for object class
if len(sys.argv) < 2:
    print("Please enter the name for the object.")
    exit()

source = 0
if len(sys.argv) == 3:
    source = int(sys.argv[2])

cls = str(sys.argv[1])

cap = cv.VideoCapture(source)
# time.sleep(10)
cap.set(3, 640)
cap.set(4, 480)

# directry to output latest_label.txt file and raw images
raw_data_dir = '../../data/raw/'

# create data folder for output frames
output_path = raw_data_dir + cls
if not os.path.exists(output_path):
    os.makedirs(output_path)
else:
    print("An obejct with the same name exists; please use a different name and try again:)")
    exit()

# write the class name to latest_label.txt
txt_file_path = raw_data_dir + 'latest_label.txt'
with open(txt_file_path, 'w') as file:
    file.write(cls)

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

# timestamps used for fps calculation
prev_frame_time = 0
new_frame_time = 0

# training samples stats and countdown
target_sample_num = 50
collected_num = 0
countdown = 5

i = 0
while True:
    # read frame
    ret, frame = cap.read()
    # get bbox and updates tracker
    ret, bbox = tracker.update(frame)

    # fps calculation
    new_frame_time = time.time()
    fps = 1.0/(new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    fps = int(fps)

    if ret:
        # draw bbox if tracking succeeded
        drawBbox(frame, bbox)
    else:
        # print missing if not
        cv.putText(frame, 'lost', (100, 145), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv.LINE_AA)

    # display status
    headline_txt = f'Capturing training samples...'
    fpd_txt = f'Camera feed @ ~{fps} fps'
    status_txt = f'Collection Status: {collected_num}/{target_sample_num}'

    cv.putText(frame, headline_txt, (30, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv.LINE_AA)
    cv.putText(frame, fpd_txt, (30, 40), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv.LINE_AA)
    cv.putText(frame, status_txt, (30, 60), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv.LINE_AA)

    ##### IMAGE CAPTURE and ANNOTATION  ######
    #######################################################
    if i % 5 == 0 and collected_num < target_sample_num:
        cv.imwrite(f"{output_path}/{cls}_{i:03}.jpg", frame)

        # append the bbox coordinate to bbox_information.txt
        bbox_coordinate = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        bbox_path = output_path + '_annotations.txt'
        with open(bbox_path, 'a') as file:
            file.write(" ".join([str(a) for a in bbox_coordinate]) + '\n')
            collected_num += 1

    if collected_num >= target_sample_num:
        exit_txt = f'Session ending in {countdown}'
        cv.putText(frame, exit_txt, (30, 80), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv.LINE_AA)
        if i % 10 == 0:
            countdown -= 1

    if countdown < 0:
        break

    i += 1
    #######################################################
    cv.imshow('tracking', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
