import numpy as np
import cv2
#import imutils 

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

LOCAL_MQTT_HOST="broker"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="IoT/motions"


# 1 should correspond to /dev/video1 , your USB camera. The 0 is reserved for the NX onboard camera
cap = cv2.VideoCapture(0)

fgbg = cv2.createBackgroundSubtractorMOG2()

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    ## implement the blur function with the kernel of 3,3
    frame = cv2.blur(frame, ksize=(3, 3) )
    fgmask = fgbg.apply(frame)
  
    img, cnts, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    ## display the frame
    cv2.imshow('frame', frame)

    #print(fgmask)

    #cv2.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
    #cv2.putText(frame, str(cap.get(cv2.CAP_PROP_POS_FRAMES)), (15, 15),
    #                           cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))


        #for (x,y,w,h) in faces:
        #    face = gray[y:y+h, x:x+w]
        #    rc,png = cv2.imencode('.png', face)
        #    if rc:
        #        msg = png.tobytes()
                #msg = "test_msg" 
        #        try:
        #            print("detected face: publishing an image")
        #            publish.single(LOCAL_MQTT_TOPIC, msg, hostname=LOCAL_MQTT_HOST, port=1883)
        #        except:
        #            print("unexpected error") 

        #    gray = cv2.rectangle(gray, (x, y), (x+w, y+h), (255,255,0), 5)
    # Display the resulting frame
    #cv2.imshow('frame', frame)
    cv2.imshow('FG Mask', fgmask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


