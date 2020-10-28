
# Training On AWS Cloud

#### System 
- file storag: s3 vs EFS
	- EFS cannot be mounted on NX (does it matter?)
	- can s3 mounted everywhere? (s3fs)
- p3.2xlarge vs g4dn.2xlarge
	- Spot instance pricing on p3.2xlarge or g4dn.2xlarge
	```
	aws --region=us-west-2 ec2 describe-spot-price-history --instance-types  p3.2xlarge --start-time=$(date +%s) --product-descriptions="Linux/UNIX" --query 'SpotPriceHistory[*].{az:AvailabilityZone, price:SpotPrice}'

	aws --region=us-west-2 ec2 describe-spot-price-history --instance-types  g4dn.2xlarge --start-time=$(date +%s) --product-descriptions="Linux/UNIX" --query 'SpotPriceHistory[*].{az:AvailabilityZone, price:SpotPrice}'
	```
- AMI: Nvidia Deep Learning AMI vs AWS Deep Learning AMI 
```
aws ec2 describe-images  --filters  Name=name,Values='Deep*Learning*Ubuntu*18.04*32*'

aws ec2 describe-images  --filters  Name=name,Values='Nvidia*Deep*Learning*'
```

Deep Learning AMI: `ami-0e462c84403994d6e`
- conda based ubuntu... not sure if it is good. yolov5 docker doesn't seem to be compatible. 
	```
	Traceback (most recent call last):
  File "detect.py", line 7, in <module>
    import cv2
  File "/opt/conda/lib/python3.6/site-packages/cv2/__init__.py", line 5, in <module>
    from .cv2 import *
ImportError: libGL.so.1: cannot open shared object file: No such file or directory
	```

#### Setup

Make sure firewall rules
```
aws ec2 authorize-security-group-ingress --group-id  sg-9c7e77b4   --protocol tcp --port 22 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id  sg-9c7e77b4  --protocol tcp --port 8888 --cidr 0.0.0.0/0
```

Start spot instance for AWS deep learning image
```
aws ec2 run-instances --image-id ami-0e462c84403994d6e --instance-type p3.2xlarge  --associate-public-ip-address --instance-market-options file://spot-options.json --key-name cal-ec2-west2
```

Start on-demand instance for Nvidia image (better image for docker)
```
aws ec2 run-instances --image-id ami-0384cb16509f0e03b --instance-type g4dn.2xlarge --associate-public-ip-address --key-name cal-ec2-west2
```

ami-050717f7d89c1247b



Using [Yolov5 docker](https://github.com/ultralytics/yolov5/wiki/Docker-Quickstart) 
```
sudo docker pull ultralytics/yolov5:latest
sudo docker run --ipc=host --gpus all -it ultralytics/yolov5:latest
sudo docker run --ipc=host --runtime nvidia --gpus all -it ultralytics/yolov5:latest
```

Building [Yolov5-based docker](https://github.com/ultralytics/yolov5/blob/master/Dockerfile)


SSH into the system
```
jupyter notebook --ip=0.0.0.0 --no-browser
```


To run yolov5 docker, 
```
# CD to toylocator repo before starting the docker

docker run --name toylocator --rm --privileged --runtime nvidia -v $PWD/modeling/pretrained:/toy_pt -v $PWD/data:/data -v /tmp:/tmp -p 8888:8888 -p 6006:6006 -ti ultralytics/yolov5

```

To train
```
# I removed --cache parameter in case. 

# optino 1
python3 train.py --img 416 --batch 16 --epochs 100 --data '/data/5_toys.v2.yolov5pytorch/data.yaml' --cfg /data/custom_yolov5s.yaml --weights '' --name yolov5s_results 

# option 2
python3 train.py --img 416 --batch 16 --epochs 100 --data '/data/5_toys.v2.yolov5pytorch/data.yaml' --cfg /data/custom_yolov5s.yaml --weights yolov5s.pt --cache

```


