import glob, shutil
import os
import pickle
import xml.etree.ElementTree as ET
from os import listdir, getcwd
from os.path import join
import numpy as np

"""
Reads images from raw data directory and prepares Yolo structure.
"""

# raw image outputs from camera; input for auto-labeling
rawImage_dir = './rawImages'

# Create yolo folder structure - images folder
img_dir = ['./train/images', './validate/images']
for dir in img_dir:
    if not os.path.exists(dir):
        os.makedirs(dir)

dirs = ['train', 'validate']
classes = ['iphone x']  # [TODO] Swap for user input  [TODO] will read in existing classes

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

def convert(size=(800, 600), box=(107.0, 694.0, 106.0, 493.0)):
    """
    Function to generate YOLO bbox parameters. The dimensions are hard-coded
    since our bounding box is fixed. We won't need this function in production.
    parameters:
        - size: tuple containing width and height of raw image
        - b: tuple containing bounding box xmin, ymin, xmax, ymax
    """
    dw = 1./(size[0])   # 1 / image width
    dh = 1./(size[1])   # 1 / image height

    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh

    return (x,y,w,h)


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
    cls = 'iphone x'  # [TODO] This needs to be swapped from user-input
    cls_id = classes.index(cls)  # [TODO] This classes will be read in from .txt file at beginning
    out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

# Execution
cwd = getcwd()
image_paths = getImagesInDir(rawImage_dir)
train_paths, validation_paths = datasetSplit(image_paths)
image_sets = [train_paths, validation_paths]

for i, image_paths in enumerate(image_sets):

    # output path to be either {$PWD}/train or {$PWD}/validate
    full_dir_path = cwd + '/' + dirs[i]

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
print("Processed {} training and {} validation".format(num_train, num_validate))


"""
Orignal .xml specs for our camera frame
<object>
	<name>iphone x</name>
	<pose>Unspecified</pose>
	<truncated>0</truncated>
	<difficult>0</difficult>
	<bndbox>
		<xmin>107</xmin>
		<ymin>106</ymin>
		<xmax>694</xmax>
		<ymax>493</ymax>
	</bndbox>
</object>
"""
