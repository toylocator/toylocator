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

1. option 1: motion tracking lab (lab3) (dynamic background comparing to previous snap shot)
2. option 2: similar to option 1, but comparing to static background (frist snap shot)
	- more sensitive than approach 1
3. ***approach 3***: object tracking. semi-automatic 
	- draw the rect and follow 
	- opencv-contrib-python (not supporting arm64: 
		- [workaround](https://github.com/AastaNV/JEP/blob/master/script/install_opencv4.3.0_Jetson.sh))
		- [docker image to try](https://hub.docker.com/r/mdegans/tegra-opencv/tags)
		- https://forums.developer.nvidia.com/t/installing-opencv-contrib-for-nano/73932
		- 
		```
		sudo docker run --user $(id -u):$(cut -d: -f3 < <(getent group video)) --runtime nvidia -it --rm mdegans/tegra-opencv:latest
		
		docker run --name tracker --privileged -v /data:/data -e DISPLAY -v /tmp:/tmp -v $PWD:/usr/src/app --runtime nvidia -it --rm mdegans/tegra-opencv:latest 

		```

#### Object tracking
We tried multiple appraoches described below and found 3rd approach as the most suitable approach. 



[TODO] finish up the code for approach 3
[TODO] create docker file (pythons, opencv)


#### Camera frame 
```
docker build -t detector -f Dockerfile.detector .

docker run --name detector --network nx_default --privileged --runtime nvidia --rm -v /data:/data -e DISPLAY -v /tmp:/tmp -v $PWD:/usr/src/app -ti detector 
```

#### Toy Tracker (WIP)
```

docker build -t tracker -f Dockerfile.detector .

docker build -t detector -f Dockerfile.detector .

docker run --name detector --network nx_default --privileged --runtime nvidia --rm -v /data:/data -e DISPLAY -v /tmp:/tmp -v $PWD:/usr/src/app -ti detector 



pip3 install opencv-contrib-python --upgrade 

```




https://docs.opencv.org/master/de/de1/group__video__motion.html



Mounting s3fs 

```
mv /.passwd-s3fs ~/.
chmod 600 ~/.passwd-s3fs

s3fs toylocator data/processed


-o url="https://s3-us-west-2.amazonaws.com"

```


