import glob, shutil
import os
import pickle
import xml.etree.ElementTree as ET
from os import listdir, getcwd
from os.path import join
import numpy as np
import sys

"""
Reads images from raw data directory and prepares Yolo structure.
"""

input_path = '../../data/raw/'
output = '../../data/processed/'

# Read in latest class label from latest_label.txt
txt_file_path = input_path + 'latest_label.txt'
with open(txt_file_path, 'r') as file:
    obj = file.read()

# Append class label to existing inventory
inventory_path = output + 'label_inventory.txt'

# Create yolo folder structure - images folder
train_img_output_path = output + 'train/images/'
validate_img_output_path = output + 'validate/images/'

img_dir = [train_img_output_path, validate_img_output_path]
for dir in img_dir:
    if not os.path.exists(dir):
        os.makedirs(dir)

# Check if class label exists in inventory already
# If exits, inform and exit
# If not, proceed with appending the class label
try:
    with open(inventory_path, 'r+') as file:
        temp_set = set(file.read().splitlines())
        if obj in temp_set:
            print("We had annotated this object already:)")
        # If class label does not exit in inventory list, append to list
        else:
            file.write(obj + '\n')

# If inventory list does not exist, create one and append class label
except:
    with open(inventory_path, 'a') as file:
        file.write(obj + '\n')

# Read in inventory list to classes
with open(inventory_path, 'r') as file:
    classes = file.read().splitlines()

# raw image outputs from camera; input for auto-labeling
rawImage_dir = '../../data/raw/{}/'.format(obj)

dirs = ['train', 'validate']

# Function to obtain a list of .jpg images in directory
def getImagesInDir(dir_path):
    """
    Function to obtain a list of .jpg files in a directory.
    Parameters:
        - dir_path: directory for the training images (from camera output)
    """
    image_list = []

    for filename in glob.glob(dir_path + '/*.jpg'):
        image_list.append(filename)
    return image_list

def datasetSplit(img_lst):
    """
    Function to split the image_list to training/validation sets.
    Parameters:
        - img_list: list of images
    """
    num = len(img_lst)

    idx = np.random.permutation(num)
    train_lst = np.array(img_lst)[idx[:int(num * .8)]]   # 80/20 split
    validation_lst = np.array(img_lst)[idx[:int(num * .2)]]
    return train_lst, validation_lst

def convert(size=(640, 480)):
    """
    Function to generate YOLO bbox parameters.
    size: tuple containing width and height of raw image
    """

    image_paths = getImagesInDir(rawImage_dir)    

    dw = 1./(size[0])   # 1 / image width
    dh = 1./(size[1])   # 1 / image height

    
    # Read in bbox coordinate information from bbox_information.txt
    bbox_path = input_path + 'bbox_information.txt'
    with open(bbox_path, 'r') as file:
        content = file.read().splitlines()
        dimension_list = []
        for n in content:
            x = int(n.split()[0])+int(n.split()[2])/2
            y = int(n.split()[1])+int(n.split()[3])/2
            w = int(n.split()[2])
            h = int(n.split()[3])
            
            x = x*dw
            w = w*dw
            y = y*dh
            h = h*dh
          
            dimension_list.append((x,y,w,h))

    return dimension_list


def annotate(output_path, image_path):
    """
    Main function to create the annotation .txt files.
    parameters:
        - dir_path: directory of training or validation images
        - output_path: destination for annotated .txt files
        - image_path: directory to individual image
    """
    basename = os.path.basename(image_path)  # extract file name only
    basename_no_ext = os.path.splitext(basename)[0]   # extract file name without extension

    out_file = open(output_path + basename_no_ext + '.txt', 'w')   # write .txt file with same file name
    bb = convert()
    cls = obj
    cls_id = classes.index(cls)
    for item in bb:
        if int(basename_no_ext.split('_')[1]) == bb.index(item):
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in item]) + '\n')

# Execution
image_paths = getImagesInDir(rawImage_dir)
train_paths, validation_paths = datasetSplit(image_paths)
image_sets = [train_paths, validation_paths]

for i, image_paths in enumerate(image_sets):

    # output path to be either {$PWD}/train or {$PWD}/validate
    full_dir_path = output + dirs[i]

    # output path in the labels folder
    output_path = full_dir_path + '/labels/'

    # create label directory if not exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # copy train/validation images to images folder
    for file in image_paths:
        shutil.copy(file, full_dir_path + '/images')

    # generate annotation files to labels folder
    for path in image_paths:
        annotate(output_path, path)

num_train = len(train_paths)
num_validate = len(validation_paths)
# print("Processed {} training and {} validation".format(num_train, num_validate))
print("Process completed")
