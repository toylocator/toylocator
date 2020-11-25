import glob, shutil
import os
#import pickle
#import xml.etree.ElementTree as ET
#from os import listdir, getcwd
#from os.path import join
import numpy as np
import sys

"""
Reads images from raw data directory and prepares Yolo structure.
"""

input_path = '/data/raw/'
output = '/data/processed/'

# Read in latest class label from latest_label.txt
txt_file_path = input_path + 'latest_label.txt'
with open(txt_file_path, 'r') as file:
    cls = file.read()

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
        if cls in temp_set:
            print("We had annotated this object already:)")
        # If class label does not exit in inventory list, append to list
        else:
            file.write(cls + '\n')

# If inventory list does not exist, create one and append class label
except:
    print("some exception")
    with open(inventory_path, 'a') as file:
        file.write(cls + '\n')

# Read in inventory list to classes
with open(inventory_path, 'r') as file:
    classes = file.read().splitlines()

# raw image outputs from camera; input for auto-labeling
rawImage_dir = '/data/raw/{}/'.format(cls)

dirs = ['train', 'validate']


# Function to obtain a list of .jpg images in directory
def get_lists_in_dir(dir_path):
    """
    Function to obtain a list of .jpg files in a directory.
    Parameters:
        - dir_path: directory for the training images (from camera output)
    """
    image_list = []

    for filename in glob.glob(dir_path + '/*.jpg'):
        image_list.append(filename)
    return image_list

def split_datasets(img_lst):
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


def read_annotation_yolov5(size=(640, 480)):
    """
    Function to generate YOLO bbox parameters.
    size: tuple containing width and height of raw image
    """

    # image_paths = get_lists_in_dir(rawImage_dir)

    dw = 1./(size[0])   # 1 / image width
    dh = 1./(size[1])   # 1 / image height

    # Read in bbox coordinate information from bbox_information.txt
    bbox_path = input_path + cls + '_annotations.txt'
    with open(bbox_path, 'r') as annotation_file:
        content = annotation_file.read().splitlines()
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
          
            dimension_list.append((x, y, w, h))

    return dimension_list


def generate_annotation(target, images):
    """
    Main function to create the annotation .txt files.
    parameters:
        - target: destination for annotated .txt files
        - images: paths to the images
    """
    bb = read_annotation_yolov5()
    for path in images:
        basename = os.path.basename(path)  # extract file name only (e.g., bear_013.jpg)
        basename_no_ext = os.path.splitext(basename)[0]   # extract file name (e.g., bear_013)

        label_filepath = target + basename_no_ext + '.txt'
        with open(label_filepath, 'w') as out_file:   # a label file is same as corresponding image file name
            cls_id = classes.index(cls)
            item = bb[int(basename_no_ext.split('_')[1])]  # e.g., 0.556, 0.6145, 0.3718, 0.5958
            out_file.write(f"{cls_id} {item[0]} {item[1]} {item[2]} {item[3]}")


# execution entry point
# image_dirs =
train_paths, validation_paths = split_datasets(get_lists_in_dir(rawImage_dir))
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
    generate_annotation(output_path, image_paths)


num_train = len(train_paths)
num_validate = len(validation_paths)
# print("Processed {} training and {} validation".format(num_train, num_validate))
print("Process completed")
