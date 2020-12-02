#!/bin/sh

version=$1
epoch=$2
batch=$3
yolov5_pt=$4

# Copy data from S3 bucket

# training only 2 classes
# aws s3 sync s3://toylocator/data_5cls_bk /data --exclude "video/*"
aws s3 sync s3://toylocator/data/${version} /data --exclude "video/*"

nc=$(cat /data/label_inventory.txt | wc -l)
cp models/yolov${yolov5_pt}.yaml /data
mv /data/yolov${yolov5_pt}.yaml /data/custom_yolov5.template
echo "# parameters" > /data/custom_yolov5.yaml
echo "nc: $nc" >> /data/custom_yolov5.yaml
sed 1,2d /data/custom_yolov5.template >> /data/custom_yolov5.yaml
rm /data/*.template

# generate data.yaml and custom_yolov5s.yaml
# python3 ../toy/src/models/gen_yolov5_yaml.py
python3 gen_yolov5_yaml.py

# (optional) smoke run for yolov5 pre-trained model
# python3 detect.py --weights yolov5s.pt --img-size 1920 --conf 0.4 --source data/images

# (optional) smoke run for training
# Out of memory if batch size is bigger than 16 so far. Hope to find bigger instance or reduce the image resolution.
# python3 train.py --img-size 1920 --rect --batch 16 --epochs 1 --data '/data/data.yaml' --cfg /data/custom_yolov5s.yaml --weights yolov5s.pt --name smoke_24_1epcs --cache

# full training

python3 train.py --img 640 --batch $batch --epochs $epoch --data '/data/data.yaml' --cfg /data/custom_yolov5.yaml --weights yolov${yolov5_pt}.pt --name ${nc}cls_${epoch}epcs_${yolov5_pt} --cache --log-imgs 100 --project ${version}

# upload the model
aws s3 cp ${version}/${nc}cls_${epoch}epcs_${yolov5_pt}/weights/best.pt s3://toylocator/model/best.pt
aws s3 cp ${version}/${nc}cls_${epoch}epcs_${yolov5_pt} s3://toylocator/model/${version}/${nc}cls_${epoch}epcs_${yolov5_pt} --recursive

# Test the model
# iou=0.4
# python3 test.py --img-size 1920 --batch $batch --data '/data/data.yaml' --weights runs/train/${nc}cls_${epoch}epcs_${yolov5_pt}/weights/best.pt --name ${nc}cls_${epoch}epcs_${yolov5_pt} --iou-thres ${iou} --task test

# Run inference on test images (optional)
# python3 detect.py --weights runs/train/${nc}cls_${epoch}epcs_${yolov5_pt}/weights/last.pt --img-size 1920 --conf 0.4 --source /data/test/images

# verify the result (optional)
# jupyter lab --ip=0.0.0.0 --no-browser