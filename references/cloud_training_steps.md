## Training on AWS
Nvidia Deep Learning AMI: `ami-0384cb16509f0e03b`

#### Cloud environment set-up
Set up firewall rules
- change sg IDs accordingly
```
aws ec2 authorize-security-group-ingress --group-id sg-9*******4 --protocol tcp --port 22 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id sg-9*******4 --protocol tcp --port 8888 --cidr 0.0.0.0/0
```

Start a g4dn.2xlarge instance with Nvidia deep learning AMI and appropriate security group
- change key name and sg group accordingly
```
aws ec2 run-instances --image-id ami-0384cb16509f0e03b --instance-type g4dn.2xlarge --security-group-ids sg-9*******4 --associate-public-ip-address --key-name w251-oregon
```

Obtain server address
```
aws ec2 describe-instances | grep ec2
```

SSH into the cloud instance
- change server address accordingly
```
ssh -i "w251-oregon.pem" ubuntu@ec2-xx-xxx-xxx-xx.us-west-2.compute.amazonaws.com
```

Install AWS CLI if new instance
```
sudo apt install awscli
```

Copy data from S3 Bucket
- change S3 bucket address accordingly
- copy images from S3 to /data directory in EC2 (will later be mounted to docker)
- copy dockerfile from S3 to EC2 (will be used to build the image)
```
aws s3 cp s3://path/to/data/ ./data --recursive
aws s3 cp s3://path/to/Dockerfile.cloud.yolov5 .
```

Build docker image (if new instance)
```
docker build --tag yolov5cloud -f Dockerfile.cloud.yolov5 .
```

Run docker container
- we are mounting /data (local) to /data in docker: this directory, which contains all training images, will be used in the --data flag in the training command
-
```
docker run --ipc=host --name yolov5cloud --rm --privileged --gpus all -v $PWD/data:/data -v /tmp:/tmp -p 8888:8888 -p 6006:6006 -ti yolov5cloud
```

**Create custom model.yaml and data.yaml file** (if they haven't been updated already)
```sh
vim /data/data.yaml  # change train and validation image path in data.yaml to /data/train & /data/validate
cp models/yolov5s.yaml /data  # copy the model.yaml file from yolov5 repo to /data
vim /data/yolov5s.yaml    # change number of classes in the model.yaml file to match use case
mv /data/yolov5s.yaml /data/yolov5s_vehicle.yaml  # rename customized model.yaml file
```

Training  
- place data.yaml under the --data flag; this tells train.py where to find training images
- place customized model.yaml under --cfg flag; this specifies model configuration
- place pre-trained base weights under --weights flag; if training from scratch is preferred, use ' '
```
python3 train.py --img 416 --batch 16 --epochs 200 --data /data/data.yaml --cfg /data/custom_yolov5s.yaml --weights yolov5s.pt --name yolov5s_remote --cache
```

```
python3 train.py --img 416 --batch 16 --epochs 200 --data /data/data.yaml --cfg /data/custom_yolov5s.yaml --weights yolov5m.pt --name yolov5s_remote --cache
```

Output trained weights
- change path accordingly (using the 6th run in this example)
- copy the trained weights from yolo directory to our own data directory
```
cp -f runs/expx_xxx /data
cp -f runs/expx_xxx /data
```

Transfer trained weights from EC2 to S3
- exit the container `exit`
- change S3 bucket address accordingly
```
aws s3 sync . s3://path/to/data/
```

Inference
- start NX container
- change source accordingly to be file path or camera
```
python3 detect.py --weights /data/best.pt --img 416 --conf 0.4 --source /data/test/images
```
