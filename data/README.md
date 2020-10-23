## (Temp Name: Labeller) creating training dataset 

#### reference
- [w251/week08](https://github.com/MIDS-scaling-up/v2/tree/master/week08)
- [Toy Detector with Tensorflow](https://www.kdnuggets.com/2018/02/building-toy-detector-tensorflow-object-detection-api.html) 
- [roboflow](https://app.roboflow.com/)


1. parse video to images
	- ffmpeg 
		- https://hub.docker.com/r/jrottenberg/ffmpeg/ 
		- https://hub.docker.com/r/linuxserver/ffmpeg 
2. augment images
	- https://github.com/codebox/image_augmentor
	- robotflow 
3. create training datasets / test datasets 


#### Setup 
[TODO convert to docker-compose to simply]
```
cd labeller
docker build -t labeller -f Dockerfile.labeller .

```
