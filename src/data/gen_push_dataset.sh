#!/bin/sh

rm -rf /data/augmented
rm -rf /data/processed

# rotate shift scale noise are optional but at least one of them needs to be specified 
python3 src/data/augmentation.py rotate shift flip scale noise

# download the latest label inventory 
aws s3 cp s3://toylocator/data/label_inventory.txt /data/label_inventory.txt

# convert annotation format
python3 src/data/annotation.py

# upload dataset to repository
aws s3 cp /data/processed/train s3://toylocator/data/train --recursive
aws s3 cp /data/processed/validate s3://toylocator/data/validate --recursive
aws s3 cp /data/processed/test s3://toylocator/data/test --recursive
aws s3 cp /data/processed/error s3://toylocator/error/images --recursive
aws s3 cp /data/label_inventory.txt s3://toylocator/data/label_inventory.txt
