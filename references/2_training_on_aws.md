
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

#### Training with non-square images 
- For the rectangles 1080x1920, [--img-size 1920 --rect](https://github.com/ultralytics/yolov5/issues/700) 
- 

#### Start Instance and Docker

Start AWS deep learning image instance 
- specify `--instance-type`: `p3.2xlarge` or `g4dn.2xlarge` 
- (optional) `--instance-market-options` for spot instance. 
```
aws ec2 run-instances --image-id <AMI ID> --instance-type <either p3 or g4 instance> --associate-public-ip-address --key-name <key name> 
--instance-market-options file://spot-options.json 

```

Using Docker-Compose  
- [install awscli](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html#cliv2-linux-install)
```
# if missing, install awscli 
# sudo apt install -y awscli 
aws configure
# enter access key and secret key for s3://toylocator 

# CD to toylocator repo before starting the docker
git clone https://github.com/toylocator/toylocator.git
cd toylocator 
```

Using Docker-Compose
- [install docker-compose](https://docs.docker.com/compose/install/) 
```
# sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" > ~/docker-compose
# chmod +x ~/docker-compose 
# sudo mv ~/docker-compose /usr/local/bin/docker-compose

cd ~/toylocator/model

# use the following command only if needs to rebuild with fresh docker image 
# docker-compose build --no-cache
docker-compose up
```

Using Docker (if not using docker-compose)
```
docker build -t yolov5cloud -f Dockerfile.cloud.yolov5 .

docker run --ipc=host --name toydetector --rm --privileged --gpus all -v /tmp:/tmp -v $HOME/.aws:/root/.aws:rw -p 8888:8888 -p 6006:6006 -ti toydetector

./train_yolov5_model.sh
```

train_yolov5_model.sh (for debugging only)
```
# Copy data from S3 bucket
aws s3 cp s3://toylocator/data /data --recursive

# generate data.yaml and custom_yolov5s.yaml 
nc=$(cat /data/label_inventory.txt | wc -l)
mv /data/data.yaml /data/data.template
echo "names: [default]" > /data/data.yaml
echo "nc: $nc" >> /data/data.yaml
sed 1,2d /data/data.template >> /data/data.yaml
mv /data/custom_yolov5s.yaml /data/custom_yolov5s.template
echo "names: # parameters" > /data/custom_yolov5s.yaml
echo "nc: $nc" >> /data/custom_yolov5s.yaml
sed 1,2d /data/custom_yolov5s.template >> /data/custom_yolov5s.yaml

# sanity check (optional)
# python3 detect.py --weights yolov5s.pt --img 416 --conf 0.4 --source inference/images/

# (optional) smoke run for training 
python3 train.py --img 1920 --rect --batch 4 --epochs 5 --data '/data/data.yaml' --cfg /data/custom_yolov5s.yaml --weights '' --name yolov5s_results --cache

# full training  
python3 train.py --img 1920 --rect --batch 16 --epochs 100 --data '/data/data.yaml' --cfg /data/custom_yolov5s.yaml --weights '' --name yolov5s_results --cache

# inference on test images (optional)
cp -f runs/train/yolov5s_results/weights/last.pt /data
cp -f runs/train/yolov5s_results/weights/best.pt /data
python3 detect.py --weights runs/exp0_yolov5s_results/weights/last.pt --img 416 --conf 0.4 --source /data/test/images

# upload the model
model_dir=$(date +'%m-%d-%Y-%0l%p')
aws s3 cp runs/train/yolov5s_results/weights/last.pt s3://toylocator/model/last.pt
aws s3 cp runs/train/yolov5s_results s3://toylocator/model/$model_dir --recursive

# verify the result (optional)
# jupyter lab --ip=0.0.0.0 --no-browser
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


