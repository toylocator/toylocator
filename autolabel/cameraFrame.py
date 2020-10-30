import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

# capture video from camera
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    x, y, w, h = 200, 100, 800, 600

    frame = cv.rectangle(frame, (x, y), (x + w, y + h), (255, 223, 0), 5)

    cv.imshow('img', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
