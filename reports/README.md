

#### v1 high resolution 

Training Data
- 2 ~ 8 classes 
- 1920 x 1080 resolution
- s3://toylocator/data/video/train
- model converge and high metrics with validation/test data but not on production inference


#### v2 [low resolution : 640 - minimum augmentation](https://wandb.ai/taeil/toydetector/runs)
- 2D 
- 50 frames 
2 clases
- no noise augmentation 
- Best: /data/model/2cls_300epcs_yolov5s/weights/best.pt 
- Source: /data/video/test/test_room_02.avi 
- scale: 0.5, 1.5

[w251 final project presentation](https://drive.google.com/file/d/1z1lx2MwpX9trL2hf0u54mgsu8XF7Yc_h/view)  

#### v3 [low resolution : 640 - increased augmentation]
- 3D 
- 100 frames 
- increased scale aug: 0.3, .6, 1.3, 1.7
- noise 
- Not so good on production
 
[9 classes 100epcs yolov5s](https://wandb.ai/taeil/toydetector/runs/2kxojrqv/overview?workspace=user-taeil)
- 9cls_100epcs_5s
- 9cls_100epcs_5l

#### v4 [low resolution : 640] 
- white background 
- increased training data collection 
- 2 shift, 4 scale, 4 rotate, flip
- 1 class:
	- [training performance](https://wandb.ai/taeil/v4/runs/1x5kymee?workspace=user-taeil) 
	- live inference: 
	![](live_inference_red_car_01.png)
	![](live_inference_red_car_02.png)
- 2 class: 
	- [training performance](https://wandb.ai/taeil/v4/runs/139mg8cb?workspace=user-taeil) 
	- live inference: 

#### v5 [low resolution : 640] 
- white background 
- increased training data collection 
- 4 scale, 4 rotate, flip
- 1 class: 
- 2 class: 

