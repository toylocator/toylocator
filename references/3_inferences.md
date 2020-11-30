## YOLOV5 Inference 

#### Inference from images
- start NX container
- change source accordingly to be file path or camera

#### inference from the camera, 
```
# must run this command on NX terminal (not SSH)
xhost +

sudo aws s3 cp s3://toylocator/model/best.pt /data/model/best.pt

docker run --name -rm yolov5nx --privileged -e DISPLAY=$DISPLAY --runtime nvidia -v /data:/data -v /tmp:/tmp -p 8888:8888 -p 6006:6006 -ti yolov5

# from video file
python3 detect.py --weights /data/model/best.pt --img-size 1920 --conf 0.4 --source /data/video/test/test_room_02.avi 

# generic detection for sanity check (please change to 0)
python3 detect.py --source 1 --weights yolov5s.pt --conf 0.4

# run toy detection with camera (please change to 0)
python3 detect.py --img-size 1920 --source 1 --weights /data/model/best.pt --iou-thres 0.1

```

To run inference on test dataset
```
!python3 detect.py --weights /data/model/best.pt --img-size 1920 --conf 0.4 --source /data/test/images
```


option 1: fix the docker to run the inference on the video files 
option 2: run the inference on the video files (video -> images) 
option 3: run the inferecne on the test image set 
option 4: collect from the camera and run the inference on the camera 


Taeil: to focus on clean dataset 
Chenlin and Hongsuk: inference video 
Everyone: cloud training with high AUC (high precision/recall) and explore wandb 

checkin again for nice to have items  
- add more classes
- add more test video 
- test on live cameras 