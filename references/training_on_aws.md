
# Training On AWS

#### System Requirements 
- file storag: s3, EFS, or aws s3 copy  
	- EFS cannot be mounted on NX (does it matter?)
	- can s3 mounted everywhere? (s3fs)
- Instance type
	- p3.2xlarge
	- ***g4dn.2xlarge***
- AMI used (either one is good)
	- ***Nvidia Deep Learning AMI***:  `ami-0384cb16509f0e03b`
	- AWS Deep Learning AMI
- firewall rules (22 AND 8888)
- Yolov5 docker 
	- [Dockerfile](Dockerfile.cloud.yolov5) based on [Yolov5-based docker](https://github.com/ultralytics/yolov5/blob/master/Dockerfile)
	- [Containers: nvidia:pytorch](https://ngc.nvidia.com/catalog/containers/nvidia:pytorch/layers)
https://github.com/ultralytics/yolov5/issues/58
	- [TODO] fix warning 
NOTE: MOFED driver for multi-node communication was not detected.
      Multi-node communication performance may be reduced.
	- [TODO] --runttime nvidia vs --gpus all


#### Start Instance and Docker

Start AWS deep learning image instance 
- specify `--instance-type`: `p3.2xlarge` or `g4dn.2xlarge` 
- (optional) `--instance-market-options` for spot instance. 
```
aws ec2 run-instances --image-id <AMI ID> --instance-type <either p3 or g4 instance> --associate-public-ip-address --key-name <key name> 
--instance-market-options file://spot-options.json 

```

Build docker image  
```
docker build -t yolov5cloud -f Dockerfile.cloud.yolov5 .

# CD to toylocator repo before starting the docker
git clone https://github.com/toylocator/toylocator.git
cd toylocator 

docker run --ipc=host --name toylocator --rm --privileged --gpus all -v $PWD/data:/data -v /tmp:/tmp -p 8888:8888 -p 6006:6006 -ti yolov5cloud

# sanity check (optional)
# python3 detect.py --weights yolov5s.pt --img 416 --conf 0.4 --source inference/images/
```

#### Copy Dataset and Create Yolov5 YAML (WIP)

1. Install AWS CLI
```
sudo apt install awscli
```
2. Copy data from S3 bucket
```
aws s3 cp s3://your/bucket/address/data/ ./data --recursive
aws s3 cp s3://your/bucket/address/Dockerfile.cloud.yolov5 .
```
3. /data/data.yaml
```
train: /data/processed/train/images
val: /data/processed/validate/images
nc: 1
names: ['bunny']
```
4. /data/yolov5s.yaml
```
# parameters
nc: 1  # number of classes
depth_multiple: 0.33  # model depth multiple
width_multiple: 0.50  # layer channel multiple

# anchors
anchors:
  - [10,13, 16,30, 33,23]  # P3/8
  - [30,61, 62,45, 59,119]  # P4/16
  - [116,90, 156,198, 373,326]  # P5/32

# YOLOv5 backbone
backbone:
  # [from, number, module, args]
  [[-1, 1, Focus, [64, 3]],  # 0-P1/2
   [-1, 1, Conv, [128, 3, 2]],  # 1-P2/4
   [-1, 3, BottleneckCSP, [128]],
   [-1, 1, Conv, [256, 3, 2]],  # 3-P3/8
   [-1, 9, BottleneckCSP, [256]],
   [-1, 1, Conv, [512, 3, 2]],  # 5-P4/16
   [-1, 9, BottleneckCSP, [512]],
   [-1, 1, Conv, [1024, 3, 2]],  # 7-P5/32
   [-1, 1, SPP, [1024, [5, 9, 13]]],
   [-1, 3, BottleneckCSP, [1024, False]],  # 9
  ]

# YOLOv5 head
head:
  [[-1, 1, Conv, [512, 1, 1]],
   [-1, 1, nn.Upsample, [None, 2, 'nearest']],
   [[-1, 6], 1, Concat, [1]],  # cat backbone P4
   [-1, 3, BottleneckCSP, [512, False]],  # 13

   [-1, 1, Conv, [256, 1, 1]],
   [-1, 1, nn.Upsample, [None, 2, 'nearest']],
   [[-1, 4], 1, Concat, [1]],  # cat backbone P3
   [-1, 3, BottleneckCSP, [256, False]],  # 17 (P3/8-small)

   [-1, 1, Conv, [256, 3, 2]],
   [[-1, 14], 1, Concat, [1]],  # cat head P4
   [-1, 3, BottleneckCSP, [512, False]],  # 20 (P4/16-medium)

   [-1, 1, Conv, [512, 3, 2]],
   [[-1, 10], 1, Concat, [1]],  # cat head P5
   [-1, 3, BottleneckCSP, [1024, False]],  # 23 (P5/32-large)

   [[17, 20, 23], 1, Detect, [nc, anchors]],  # Detect(P3, P4, P5)
  ]
```

#### Training 
Train and verify the result 
```
# (optional) smoke run for training 
python3 train.py --img 416 --batch 4 --epochs 5 --data '/data/5_toys.v2.yolov5pytorch/data.yaml' --cfg /data/custom_yolov5s.yaml --weights '' --name yolov5s_results --cache

# full training  
python3 train.py --img 416 --batch 16 --epochs 100 --data '/data/5_toys.v2.yolov5pytorch/data.yaml' --cfg /data/custom_yolov5s.yaml --weights '' --name yolov5s_results --cache

# save models 
cp -f runs/exp1_yolov5s_results/weights/last.pt /data
cp -f runs/exp1_yolov5s_results/weights/best.pt /data

# inference on test images 
python3 detect.py --weights /data/best.pt --img 416 --conf 0.4 --source /data/5_toys.v2.yolov5pytorch/test/images

# verify the result (optional)
jupyter lab --ip=0.0.0.0 --no-browser
```

Grab trained models from S3 and moved them to the directory where detect.py is located
```
aws s3 cp s3://your/bucket/address/data/best.pt .
aws s3 cp s3://your/bucket/address/data/last.pt .
```

#### Other Things That Was Not Working
Using [Yolov5 docker](https://github.com/ultralytics/yolov5/wiki/Docker-Quickstart)  This does not work. Some issue maybe related to pytorch version compatibility. 
```
sudo docker pull ultralytics/yolov5:latest
sudo docker run --ipc=host --gpus all -it ultralytics/yolov5:latest
sudo docker run --ipc=host --runtime nvidia --gpus all -it ultralytics/yolov5:latest

docker run --name toylocator --rm --privileged --gpus all --runtime nvidia -v $PWD/data:/usr/src/app/data -v /tmp:/tmp -p 8888:8888 -p 6006:6006 -ti yolov5cloud

sudo docker run --ipc=host --gpus all -p 8888:8888 -p 6006:6006 -it ultralytics/yolov5:latest

```


