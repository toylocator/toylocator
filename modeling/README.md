
# Training On AWS Cloud

#### System Requirements 
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

#### Setup
![Dockerfile](Dockerfile.cloud.yolov5) based on [Yolov5-based docker](https://github.com/ultralytics/yolov5/blob/master/Dockerfile)

[Containers: nvidia:pytorch](https://ngc.nvidia.com/catalog/containers/nvidia:pytorch/layers)

[TODO] fix warning 
NOTE: MOFED driver for multi-node communication was not detected.
      Multi-node communication performance may be reduced.
[TODO] --runttime nvidia vs --gpus all

Build Docker 
```
docker build -t yolov5cloud -f Dockerfile.cloud.yolov5 .

# CD to toylocator repo before starting the docker
git clone https://github.com/taeil/toylocator.git
cd toylocator 

docker run --ipc=host --name toylocator --rm --privileged --gpus all -v $PWD/data:/data -v /tmp:/tmp -p 8888:8888 -p 6006:6006 -ti yolov5cloud

# sanity check 
python3 detect.py --weights yolov5s.pt --img 416 --conf 0.4 --source inference/images/
```

Training 
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


#### Other Things Tried But Did Not Work 
Using [Yolov5 docker](https://github.com/ultralytics/yolov5/wiki/Docker-Quickstart) 
This does not work. Some issue maybe related to pytorch version compatibility. 
```
sudo docker pull ultralytics/yolov5:latest
sudo docker run --ipc=host --gpus all -it ultralytics/yolov5:latest
sudo docker run --ipc=host --runtime nvidia --gpus all -it ultralytics/yolov5:latest

docker run --name toylocator --rm --privileged --gpus all --runtime nvidia -v $PWD/data:/usr/src/app/data -v /tmp:/tmp -p 8888:8888 -p 6006:6006 -ti yolov5cloud

sudo docker run --ipc=host --gpus all -p 8888:8888 -p 6006:6006 -it ultralytics/yolov5:latest

```


