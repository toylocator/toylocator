## Manual Label
1. Manually label the images using [labelImg](https://github.com/tzutalin/labelImg))
	1. label new images 
	2. [TODO] merge with existing classes.txt and update class ID
	3. [TODO] validate label and image sizes
2. pre-processing images 

## Automatic label
Manual labelling images is not feasible options for actual real life scenario. 
Explore the following options 
- [TODO] option 1. convert to dataset without labeling. yolov5 dummy label that mark whole part of image as label
- [TODO] option 2. segmentation, automatically label. (potentially publishable)  
- [TODO] further research on automatic labelling 
- [TODO test option 1 of dataset creation how well it performs without labeling] 

#### Object tracking
We tried multiple appraoches described below and found 3rd approach as the most suitable approach. 

- approach 1: motion tracking lab (lab3) (dynamic background comparing to previous snap shot)
- approach 2: similar to 1, but comparing to static background (frist snap shot)
	- more sensitive than approach 1
- ***approach 3***: semi-automatic 
	- draw the rect and follow 

[TODO] finish up the code for approach 3
[TODO] create docker file (pythons, opencv)


#### Camera frame 
```
docker build -t detector -f Dockerfile.detector .

docker run --name detector --network nx_default --privileged --runtime nvidia --rm -v /data:/data -e DISPLAY -v /tmp:/tmp -v $PWD:/usr/src/app -ti detector 
```


#### Motion detection (WIP)

```
docker build -t detector -f Dockerfile.detector .

docker run --name detector --network nx_default --privileged --runtime nvidia --rm -v /data:/data -e DISPLAY -v /tmp:/tmp -v $PWD:/usr/src/app -ti detector 
```

https://docs.opencv.org/master/de/de1/group__video__motion.html



Mounting s3fs 

```
mv /.passwd-s3fs ~/.
chmod 600 ~/.passwd-s3fs

s3fs toylocator data/processed


-o url="https://s3-us-west-2.amazonaws.com"

```


