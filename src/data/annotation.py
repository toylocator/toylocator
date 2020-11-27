import glob
import shutil
import os
import numpy as np


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
    validation_lst = np.array(img_lst)[idx[int(num * .8):int(num * .9)]]
    test_lst = np.array(img_lst)[idx[int(num * .9):]]
    return train_lst, validation_lst, test_lst


def read_annotation_yolov5(bbox_path):
    """
    Function to generate YOLO bbox parameters.
    size: tuple containing width and height of raw image
    """

    # image_paths = get_lists_in_dir(rawImage_dir)

    dw = 1./(camera_resolution[0])   # 1 / image width
    dh = 1./(camera_resolution[1])   # 1 / image height

    # Read in bbox coordinate information from bbox_information.txt
    dimension_list = []
    with open(bbox_path, 'r') as annotation_file:
        content = annotation_file.read().splitlines()

        for n in content:
            # x = int(n.split()[0])+int(n.split()[2])/2
            # y = int(n.split()[1])+int(n.split()[3])/2
            # w = int(n.split()[2])
            # h = int(n.split()[3])
            #
            # x = x*dw
            # w = w*dw
            # y = y*dh
            # h = h*dh

            bb = n.split()
            w = int(bb[2])
            h = int(bb[3])

            start_x = int(bb[0])
            start_y = int(bb[1])

            center_x = start_x + w / 2
            center_y = start_y + h / 2

            x = center_x * dw
            y = center_y * dh
            w = w * dw
            h = h * dh
          
            dimension_list.append((x, y, w, h))

    return dimension_list


def generate_annotation(target, images, bbox_path):
    """
    Main function to create the annotation .txt files.
    parameters:
        - target: destination for annotated .txt files
        - images: paths to the images
    """
    good_image_paths = []
    bad_image_paths = []
    bb = read_annotation_yolov5(bbox_path)
    for path in images:
        basename = os.path.basename(path)  # extract file name only (e.g., bear_013.jpg)
        basename_no_ext = os.path.splitext(basename)[0]   # extract file name (e.g., bear_013)

        label_filepath = os.path.join(target, f'{basename_no_ext}.txt')
        with open(label_filepath, 'w') as out_file:   # a label file is same as corresponding image file name
            cls_id = classes.index(cls)
            item = bb[int(basename_no_ext.split('_')[-1])]  # e.g., 0.556, 0.6145, 0.3718, 0.5958

            # validation that annotation is between 0 and 1.
            if item[0] <= 0 or item[1] <= 0 or item[2] <= 0 or item[3] <= 0 \
                or item[0] >= 1 or item[1] >= 1 or item[2] >= 1 or item[3] >= 1:
                print(f"{basename_no_ext} is potentially garage: {item[0]} {item[1]} {item[2]} {item[3]}")
                bad_image_paths.append(path)
                continue

            out_file.write(f"{cls_id} {item[0]} {item[1]} {item[2]} {item[3]}")
            good_image_paths.append(path)
            # print(f"{basename_no_ext:} {cls_id} {item[0]} {item[1]} {item[2]} {item[3]}")

    return good_image_paths, bad_image_paths

# execution entry point
if __name__ == '__main__':

    """
    Reads images from raw data directory and prepares Yolo structure.
    """
    # camera_resolution = (640, 480)
    camera_resolution = (1080, 1920)

    input_path = '/data/raw/'
    aug_path = '/data/augmented/'
    output = '/data/processed/'
    data_path = '/data/'

    # Read in latest class label from latest_label.txt
    txt_file_path = input_path + 'latest_label.txt'
    with open(txt_file_path, 'r') as file:
        cls = file.read()

    # Append class label to existing inventory
    inventory_path = os.path.join(data_path, 'label_inventory.txt')

    # Create yolo folder structure - images folder
    # noinspection DuplicatedCode
    train_img_output_path = os.path.join(output, 'train', 'images')
    validate_img_output_path = os.path.join(output, 'validate', 'images')

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
    augImage_dir = '/data/augmented/{}/'.format(cls)

    dirs = ['train', 'validate', 'test']

    image_paths = get_lists_in_dir(rawImage_dir)
    train_paths, validation_paths, test_paths = split_datasets(image_paths)

    aug_image_paths = get_lists_in_dir(augImage_dir)
    aug_train_paths, aug_validation_paths, aug_test_paths = split_datasets(aug_image_paths)
    image_sets = [train_paths, validation_paths, test_paths, aug_train_paths, aug_validation_paths, aug_test_paths]
    bbox_paths = [input_path + cls + '_annotations.txt', aug_path + 'aug_bbox_information.txt']

    for i, image_paths in enumerate(image_sets):

        # output path to be either {$PWD}/train or {$PWD}/validate
        # 0, 3 for train, 1, 4 for validate, and 2,5 for test
        full_dir_path = os.path.join(output, dirs[i%3])
        print(full_dir_path)

        # output path in the labels folder
        output_path = os.path.join(full_dir_path, 'labels')

        # create label directory if not exists
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        if not os.path.exists(os.path.join(full_dir_path, 'images')):
            os.makedirs(os.path.join(full_dir_path, 'images'))

        # generate annotation files to labels folder
        # 0, 1 for original (bbox_paths[0]) and 2, 3 for augmented (bbox_paths[1])
        annotated_image_paths, erroneous_image_paths = generate_annotation(output_path, image_paths, bbox_paths[i//3])

        # copy train/validation images to images folder
        for file in annotated_image_paths:
            shutil.copy(file, os.path.join(full_dir_path, 'images'))

        if len(erroneous_image_paths) > 0:
            error_output_path = os.path.join(output, 'error')
            if not os.path.exists(error_output_path):
                os.makedirs(error_output_path)

            for file in erroneous_image_paths:
                shutil.copy(file, error_output_path)

        print(bbox_paths[i//3])

    total_train = len(train_paths) + len(aug_train_paths)
    total_validate = len(validation_paths) + len(aug_validation_paths)
    total_validate = len(test_paths) + len(aug_test_paths)
    print(f"Processed {total_train} training, {total_validate} validation, {total_validate} test")
    print("Process completed")



