## YOLOV5 Inference 

Transfer trained weights from EC2 to S3
- exit the container `exit`
- change S3 bucket address accordingly
```
aws s3 sync . s3://path/to/data/
```

#### Inference from images
- start NX container
- change source accordingly to be file path or camera
```
python3 detect.py --weights /data/best.pt --img 416 --conf 0.4 --source /data/test/images
```

To run inference on test dataset
```
!python3 detect.py --weights toy/modeling/pretrained/best_v1024_5toys.pt --img 416 --conf 0.4 --source "toy/data/4 toys.v2.yolov5pytorch/test/images"
```

#### inference from the camera, 
```
# must run this command on NX terminal (not SSH)
xhost +

docker run --name toylocator --privileged -e DISPLAY=$DISPLAY --runtime nvidia -v $PWD/modeling/pretrained:/toy_pt -v $PWD/data:/data -v /tmp:/tmp -p 8888:8888 -p 6006:6006 -ti yolov5

# generic detection for sanity check (please change to 0)
python3 detect.py --source 1 --weights yolov5s.pt --conf 0.4

# run toy detection with camera (please change to 0)
python3 detect.py --source 1 --weights /toy_pt/best_v1026_5toys.pt --conf 0.4

```
