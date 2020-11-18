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
	- Pros: 
2. (approach 2): static motion tracking similar to the approach 1, but comparing to static background (first snap shot)
	- more sensitive than approach 1
	- Cons:
	- Pros: 
3. (approach 3) segmentation, automatically label only if we can do segmentation without object detection   
	- Cons:
	- Pros: 
5. ***(approach 4)***: object tracking. semi-automatic 
	- Tracking the objects within the ROI area that is drawn by a user
	- Cons:
	- Pros:  
		- opencv-contrib-python: ([not supporting arm64](https://forums.developer.nvidia.com/t/how-to-install-opencv-contrib-python-on-xavier/76549) Need to build a package for ARM devices. See[building opencv-contrib-python on NX](build_opencv-contrib-python) for the workaround
1. (approach 5) convert to dataset without labeling. yolov5 dummy label that mark whole part of image as label
	- Cons:
	- Pros:  

#### Object Tracker (approach 4)
```
docker build -t tracker -f Dockerfile.tracker .

docker run --name tracker --privileged --runtime nvidia --rm -v /data:/data -e DISPLAY -v /tmp:/tmp -v $PWD:/usr/src/app -p 8888:8888 -ti tracker 

python3 object_track.py <toy name> 0 

python3 annotation.py

```

#### Validate Labelled Images 
Use the `validate_yolov5_dataset` jupyter noebook. 

#### pre-processing images
`WIP`

#### Upload annotated dataset
`WIP`

