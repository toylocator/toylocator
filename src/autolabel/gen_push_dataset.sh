#!/bin/sh


rm -rf ../../data/augmented/
rm -rf ../../data/processed/

python3 augmentation.py rotate shift scale flip 

aws s3 cp s3://toylocator/data/label_inventory.txt ../../data/label_inventory.txt

python3 aug_annotation.py

aws s3 cp ../../data/processed/train s3://toylocator/data/train --recursive
aws s3 cp ../../data/processed/validate s3://toylocator/data/validate --recursive
aws s3 cp ../../data/label_inventory.txt s3://toylocator/data/label_inventory.txt 

