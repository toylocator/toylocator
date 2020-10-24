## (Temp Name: Labeller) creating training dataset 

#### reference
- [w251/week08](https://github.com/MIDS-scaling-up/v2/tree/master/week08)
- [Toy Detector with Tensorflow](https://www.kdnuggets.com/2018/02/building-toy-detector-tensorflow-object-detection-api.html) 
- [roboflow](https://app.roboflow.com/)


1. parse video to images
	- ffmpeg 
		- https://hub.docker.com/r/jrottenberg/ffmpeg/ 
		- https://hub.docker.com/r/linuxserver/ffmpeg 
2. label images 
	- [labelImg](https://github.com/tzutalin/labelImg)
3. augment images
	- [image_augmentor](https://github.com/codebox/image_augmentor)
4. create training datasets / test datasets 
5. 


#### Setup 
[TODO convert to docker-compose to simply]

[TODO create our own docker with ffmpeg and labelimg] 

```
docker run -ti -v $PWD:/images/data ryandejana/lab8:v1 bash

#docker build -t labeller -f data/Dockerfile.labeller .
```

Dockerless 
```
mkdir 2234
ffmpeg -i video/IMG_2234.MOV -frames:v 100 -r 2 images/2234/extract%03d.jpg

```

Label the images 
