1. Execute object_track.py to create captured images, label, and bbox dimensions 
```python object_track.py toy1```

2. Execute annotation.py to change the bbox dimensions into yolov5 structure
```python annotation.py```

3. Training on AWS

- Set up firewall rules
```
aws ec2 authorize-security-group-ingress --group-id sg-******** --protocol tcp --port 22 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id sg-******** --protocol tcp --port 8888 --cidr 0.0.0.0/0
```

- Start a g4dn.2xlarge instance with Nvidia deep learning AMI and appropriate security group
```
aws ec2 run-instances --image-id ami-0384cb16509f0e03b --instance-type g4dn.2xlarge --security-group-ids sg-9*******4 --associate-public-ip-address --key-name w251-oregon
```
- SSH into the cloud instance
```
ssh -i "w251-project.pem" ubuntu@ec2-*****.****.compute.amazonaws.com
```

- Install AWS CLI
```
sudo apt install awscli
```

- Upload data folder and Dockerfile.cloud.yolov5 to S3 bucket
- Copy data from S3 bucket
```
aws s3 cp s3://your/bucket/address/data/ ./data --recursive
aws s3 cp s3://your/bucket/address/Dockerfile.cloud.yolov5 .
```

- Build docker image
```
docker build --tag yolov5cloud -f Dockerfile.cloud.yolov5 .
```

- Run docker container
```
docker run --ipc=host --name yolov5cloud --rm --privileged --gpus all -v $PWD/data:/data -v /tmp:/tmp -p 8888:8888 -p 6006:6006 -ti yolov5cloud
```

vim /data/data.yaml
```
train: /data/processed/train/images
val: /data/processed/validate/images
nc: 1
names: ['bunny']
```
vim /data/yolov5s.yaml
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

- Training  
```
python3 train.py --img 416 --batch 16 --epochs 100 --data /data/data.yaml --cfg /data/yolov5s.yaml --weights yolov5s.pt --name yolov5s --cache
```

- Output trained weights
```
cp -f runs/train/yolov5s/weights/last.pt /data
cp -f runs/train/yolov5s/weights/best.pt /data
```

- Transfer trained weights from EC2 to S3
- exit the container `exit`
- change S3 bucket address accordingly
```
aws s3 sync . s3://your/bucket/address/data/
```

- Grab trained models from S3 and moved them to the directory where detect.py is located
```
aws s3 cp s3://your/bucket/address/data/best.pt .
aws s3 cp s3://your/bucket/address/data/last.pt .
```


- Inference
- I connected usb cam to mac, so the source is 1
```
python3 detect.py --weights /data/best.pt --img 416 --conf 0.4 --source 1
```
