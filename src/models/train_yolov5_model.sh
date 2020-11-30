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

epoch = 300
batch = 16
yolov5_pt = yolov5m
python3 train.py --img-size 1920 --rect --batch $batch --epochs $epoch --data '/data/data.yaml' --cfg /data/custom_yolov5s.yaml --weights ${yolov5_pt}.pt --name ${nc}cls_${epoch}epcs_${yolov5_pt} --cache

# upload the model
model_dir=$(date +'%m-%d-%Y')
aws s3 cp runs/train/${nc}cls_${epoch}epcs_${yolov5_pt}/weights/last.pt s3://toylocator/model/last.pt
aws s3 cp runs/train/${nc}cls_${epoch}epcs_${yolov5_pt} s3://toylocator/model/${nc}cls_${epoch}epcs_${yolov5_pt}/$model_dir --recursive

# Test the model
python3 test.py --img-size 1920 --batch $batch --data '/data/data.yaml' --weights runs/train/${nc}cls_${epoch}epcs_${yolov5_pt}/weights/last.pt --name ${nc}cls_${epoch}epcs_${yolov5_pt} --iou-thres ${iou} --task test

# Run inference on test images (optional)
# python3 detect.py --weights runs/train/${nc}cls_${epoch}epcs_${yolov5_pt}/weights/last.pt --img-size 1920 --conf 0.4 --source /data/test/images

# verify the result (optional)
# jupyter lab --ip=0.0.0.0 --no-browser