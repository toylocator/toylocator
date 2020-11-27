#!/bin/sh


# Copy data from S3 bucket
aws s3 cp s3://toylocator/data /data --recursive --exclude "video/*"

nc=$(cat /data/label_inventory.txt | wc -l)
mv /data/custom_yolov5s.yaml /data/custom_yolov5s.template
echo "# parameters" > /data/custom_yolov5s.yaml
echo "nc: $nc" >> /data/custom_yolov5s.yaml
sed 1,2d /data/custom_yolov5s.template >> /data/custom_yolov5s.yaml
rm /data/*.template

# generate data.yaml and custom_yolov5s.yaml 
python3 gen_yolov5_yaml.py

python3 train.py --img 1920 --rect --batch 16 --epochs 100 --data '/data/data.yaml' --cfg /data/custom_yolov5s.yaml --weights '' --name yolov5s_results --cache

model_dir=$(date +'%m-%d-%Y-%0l%p')
aws s3 cp runs/train/yolov5s_results/weights/last.pt s3://toylocator/model/last.pt
aws s3 cp runs/train/yolov5s_results s3://toylocator/model/$model_dir --recursive

#jupyter lab --ip=0.0.0.0 --no-browser
