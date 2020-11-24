#!/bin/sh

aws s3 cp s3://toylocator/data /data --recursive

python3 train.py --img 416 --batch 16 --epochs 100 --data '/data/data.yaml' --cfg /data/custom_yolov5s.yaml --weights '' --name yolov5s_results --cache

cp -f runs/exp0_yolov5s_results/weights/last.pt /data
cp -f runs/exp0_yolov5s_results/weights/best.pt /data

python3 detect.py --weights /data/best.pt --img 416 --conf 0.4 --source /data/5_toys.v2.yolov5pytorch/test/images

# aws s3 cp s3://toylocator/model/best.pt .

model_dir=$(date +'%m-%d-%Y-%0l%p')
aws s3 cp runs/exp0_yolov5s_results/weights/last.pt s3://toylocator/model/last.pt 
aws s3 cp runs/exp0_yolov5s_results s3://toylocator/model/$model_dir --recursive 

#jupyter lab --ip=0.0.0.0 --no-browser
