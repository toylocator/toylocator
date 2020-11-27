## YOLOV5 Inference 

#### Inference from images
- start NX container
- change source accordingly to be file path or camera

#### inference from the camera, 
```
# must run this command on NX terminal (not SSH)
xhost +

aws s3 cp s3://toylocator/model/best.pt /data/model/best.pt

docker run --name toylocator --privileged -e DISPLAY=$DISPLAY --runtime nvidia -v /data:/data -v /tmp:/tmp -p 8888:8888 -p 6006:6006 -ti yolov5

# from video file
python3 detect.py --weights /data/model/best.pt --img-size 1920 --conf 0.4 --source /data/video/test/test_room_01.avi 

# generic detection for sanity check (please change to 0)
python3 detect.py --source 1 --weights yolov5s.pt --conf 0.4

# run toy detection with camera (please change to 0)
python3 detect.py --source 1 --weights /data/model/best.pt --conf 0.4

```

To run inference on test dataset
```
!python3 detect.py --weights /data/model/best.pt --img-size 1920 --conf 0.4 --source /data/test/images
```
