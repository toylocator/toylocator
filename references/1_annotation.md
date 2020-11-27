## Manual Label
Manual labelling images is only good for determining the model.  
1. Manually label the images using [labelImg](https://github.com/tzutalin/labelImg))
	1. label new images 
	2. Manually merge with existing classes.txt and update class ID
	3. validate label and image sizes

## Automatic label
Manual labelling images is not feasible options for actual real life scenario. 
The following options are considered and selected the approach tracking an object. 

1. (approach 1) dynamic motion tracking (dynamic background comparing to previous snap shot)
	- Cons: 
		- Camera must stay still during the image capturing process, otherwise, the entire frame becomes the delta (relative to the initial snap shot).
		- Sensitive to light condiiton. Parameters can be adjusted to mitigate noise but not scalble to all environemnts with varying lighting condiitons. 
	- Pros: 
		- Works well under the set-up where the camera is fixed at a point and the object rotates on a turn-table with shadowless lighting. 
		- Bounding box adjusts well to all angles of the obejct. 
2. (approach 2): static motion tracking similar to the approach 1, but comparing to static background (first snap shot)
	- Cons: 
		- Can be very sensitive and creates unnecessary noise. 
	- Pros: 
		- Camera does not need to stay still since it's masking foreground (moving object) from the bakground dynamically in real-time. 
		- Bounding box adjusts well to all angles of the obejct. 
3. (approach 3) segmentation, automatically label only if we can do segmentation without object detection   
	- Cons:
	- Pros: 
5. ***(approach 4)***: object tracking. semi-automatic 
	- Tracking the objects within the ROI area that is drawn by a user
	- Cons:
		- Bounding box does not adjust well to the object when view angle or dimension changes. 
	- Pros:  
		- opencv-contrib-python: ([not supporting arm64](https://forums.developer.nvidia.com/t/how-to-install-opencv-contrib-python-on-xavier/76549) Need to build a package for ARM devices. See[building opencv-contrib-python on NX](0_build_opencv-contrib-python) for the workaround
1. (approach 5) convert to dataset without labeling. yolov5 dummy label that mark whole part of image as label
	- Cons:
	- Pros:  

#### Object Tracker (approach 4)
```
# configure to have access to s3 where dataset will be uploaded
# access key and secret key for s3://toylocator should be provided

docker build -t tracker -f Dockerfile.tracker .

# stable tracker
docker run --name tracker --privileged --runtime nvidia --rm -e DISPLAY -v /tmp:/tmp -v $HOME/.aws:/root/.aws:rw -ti tracker

# mount local version 
docker run --name tracker --privileged --runtime nvidia --rm -e DISPLAY -v /tmp:/tmp -v /data:/data -v $PWD:/usr/src/app -v $HOME/.aws:/root/.aws:rw -p 8888:8888 -ti tracker 
chmod +x src/data/gen_push_dataset.sh

# inside of the docker 
# from video files (video file name will be used as toy name)
aws s3 cp s3://toylocator/data/video /data/video --recursive
python3 src/data/object_track.py file /data/video/train/<video file name>

# from web camera 
# python3 src/data/object_track.py <toy name> 0 
```

#### (optional) Validate Labelled Images 
Use the jupyter noebook.  

#### Pre-processing Images and Upload to Dataset Repository  
Run shell script
```
src/data/gen_push_dataset.sh
```

gen_push_data.sh (for debugging only)
```
rm -rf /data/augmented
rm -rf /data/processed

# rotate shift scale noise are optional but at least one of them needs to be specified
python3 src/data/augmentation.py rotate shift flip noise

# download the latest label inventory
aws s3 cp s3://toylocator/data/label_inventory.txt /data/label_inventory.txt

# convert annotation format
python3 src/data/annotation.py

# upload dataset to repository
aws s3 cp /data/processed/train s3://toylocator/data/train --recursive
aws s3 cp /data/processed/validate s3://toylocator/data/validate --recursive
aws s3 cp /data/processed/error s3://toylocator/error/images --recursive
aws s3 cp /data/label_inventory.txt s3://toylocator/data/label_inventory.txt
```

