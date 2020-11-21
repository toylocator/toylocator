import numpy as np
import cv2
import random
import glob
import os
import sys


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


def rotate_image(image, angle, bb):
    
    # get image dimension
    img_width, img_height = 640, 480
    # get rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D(center = (img_width // 2, img_height // 2), angle = angle, scale = 1.0)
   
    # apply transformation (rotate image) 
    rotated_image = cv2.warpAffine(image, rotation_matrix, (img_width, img_height))
    
    # --- compute new bounding box ---
    # Apply same transformation to the four bounding box corners
    rotated_point_A = np.matmul(rotation_matrix, np.array([bb[0], bb[1], 1]).T)   
    rotated_point_B = np.matmul(rotation_matrix, np.array([bb[2], bb[1], 1]).T)   
    rotated_point_C = np.matmul(rotation_matrix, np.array([bb[2], bb[3], 1]).T)   
    rotated_point_D = np.matmul(rotation_matrix, np.array([bb[0], bb[3], 1]).T)   
    # Compute new bounding box, that is, the bounding box for rotated object
    x = np.array([rotated_point_A[0], rotated_point_B[0], rotated_point_C[0], rotated_point_D[0]])
    y = np.array([rotated_point_A[1], rotated_point_B[1], rotated_point_C[1], rotated_point_D[1]])
    new_boundingbox = [np.min(x).astype(int), np.min(y).astype(int), np.max(x).astype(int), np.max(y).astype(int)]
    
    return rotated_image, new_boundingbox


def width_shift_image(image, width_shift_range, bb):
    
    img_width, img_height = 640, 480
    factor = img_width * width_shift_range
    
    M = np.float32([[1,0,factor],[0,1,0]]) 
    shifted_image = cv2.warpAffine(image, M, (img_width, img_height))
    
    # compute new bounding box    
    shifted_point_A = np.matmul(M, np.array([bb[0], bb[1], 1]).T)   
    shifted_point_C = np.matmul(M, np.array([bb[2], bb[3], 1]).T)   
    
    new_boundingbox = [shifted_point_A[0].astype(int), shifted_point_A[1].astype(int), shifted_point_C[0].astype(int), shifted_point_C[1].astype(int) ]
    
    return shifted_image, new_boundingbox


def height_shift_image( image, height_shift_range, bb):
    
    img_width, img_height = 640, 480
    factor = height_shift_range * img_height
    
    M = np.float32([[1,0,0],[0,1,factor]]) 
    shifted_image = cv2.warpAffine(image, M, (img_width, img_height))
    
    # compute new bounding box    
    shifted_point_A = np.matmul(M, np.array([bb[0], bb[1], 1]).T)   
    shifted_point_C = np.matmul(M, np.array([bb[2], bb[3], 1]).T)   
    
    new_boundingbox = [shifted_point_A[0].astype(int), shifted_point_A[1].astype(int), shifted_point_C[0].astype(int), shifted_point_C[1].astype(int)]
    
    return shifted_image, new_boundingbox

def horizontal_flip(img, bb):
    img =  img[:,::-1,:]
    img = np.float32(img)
    img_width, img_height = 640, 480
    x_max = img_width - bb[0]
    x_min = img_width - bb[2]
    bb[0] = x_min
    bb[2] = x_max
        
    return img, bb

def scale_image(image, scale_factor, bb):

    img_width, img_height = 640, 480

    width = int(scale_factor * img_width)
    height = int(scale_factor * img_height)
    
    scaled_img = cv2.resize(image, (width,height))

    new_boundingbox = [np.float32((img_width-bb[2])*scale_factor), np.float32(bb[1]*scale_factor), np.float32((img_width-bb[0])*scale_factor), np.float32(bb[3]*scale_factor)]
      
    return scaled_img, new_boundingbox


def sp_noise(image,prob):
    '''
    Add salt and pepper noise to image
    prob: Probability of the noise
    '''
    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob 
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output


def save_image_with_annotation(img, bb, cls, img_idx):
    """
    helper funtion: write an augmented image and annotation file
    img: image to save
    bb: bounding box information
    cls: object class
    img_idx: unique image numbers for the class
    """
    cv2.rectangle(img, (bb[0], bb[1]), (bb[2], bb[3]), (255, 0, 0), 2, 1)
    cv2.imwrite(os.path.join(data_path, "augmented", cls, f"{cls}_aug_{img_idx:04}.jpg"), img)

    aug_bbox = int(bb[0]), int(bb[1]), int(bb[2]) - int(bb[0]), int(bb[3]) - int(bb[1])
    aug_bbox_path = os.path.join(data_path, 'augmented', 'aug_bbox_information.txt')
    with open(aug_bbox_path, 'a') as file:
        file.write(f"{int(bb[0])} {int(bb[1])} {int(bb[2]) - int(bb[0])} {int(bb[3]) - int(bb[1])}\n")

    # TODO handle failure when image writing was successful while label was not.

    return img_idx + 1


# execution entry point

if len(sys.argv) < 2:
    print("At least one augmentation type should be defined.\n e.g., python3 augmentation.py rotate shift scale noise")
    exit()

data_path = "../../data"

with open(os.path.join(data_path, "raw", "latest_label.txt"), 'r') as file:
    cls = file.read()

rawImage_dir = os.path.join(data_path, "raw", cls)
augImage_dir = os.path.join(data_path, "augmented", cls)

if not os.path.exists(augImage_dir):
    os.makedirs(augImage_dir)
else:
    print("An object with the same name exists; please use a different name and try again :)")
    exit()

rotation_angles = []
shifts = []
scales = []
noises = []

for i in range(1, len(sys.argv)):
    aug_type = str(sys.argv[i])
    if aug_type == "rotate":
        rotation_angles = [30, 60, 90]
    if aug_type == "shift":
        shifts = [0.2, 0.4]
    if aug_type == "scale":
        scales = [.5, 1.5]
    if aug_type == "noise":
        noises = [0.1]

image_paths = get_lists_in_dir(rawImage_dir)
image_list = os.listdir(rawImage_dir)

bbox_path = os.path.join(data_path, "raw", f"{cls}_annotations.txt")

with open(bbox_path, 'r') as file:
    content = file.read().splitlines()
    dimension_list = []
    for n in content:
        x1 = int(n.split()[0])
        y1 = int(n.split()[1])
        x2 = int(n.split()[0]) + int(n.split()[2])
        y2 = int(n.split()[1]) + int(n.split()[3])
        
        dimension_list.append([x1, y1, x2, y2])

img_idx = 0
for n in range(len(image_paths)):
    original_image = cv2.imread(image_paths[n], cv2.IMREAD_COLOR)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

    for angle in rotation_angles:
        img, bb = rotate_image(original_image, angle, dimension_list[int(image_paths[n].split('_')[1].split('.')[0])])
        img_idx = save_image_with_annotation(img, bb, cls, img_idx)

    for ratio in shifts:
        img, bb = width_shift_image(original_image, ratio, dimension_list[int(image_paths[n].split('_')[1].split('.')[0])])
        img_idx = save_image_with_annotation(img, bb, cls, img_idx)

        img, bb = height_shift_image(original_image, ratio, dimension_list[int(image_paths[n].split('_')[1].split('.')[0])])
        img_idx = save_image_with_annotation(img, bb, cls, img_idx)

    img, bb = horizontal_flip(original_image, dimension_list[int(image_paths[n].split('_')[1].split('.')[0])])
    img_idx = save_image_with_annotation(img, bb, cls, img_idx)

    for scale in scales:
        img, bb = scale_image(original_image, scale, dimension_list[int(image_paths[n].split('_')[1].split('.')[0])])
        img_idx = save_image_with_annotation(img, bb, cls, img_idx)

    # img = sp_noise(original_image, 0.1)
    img_idx = save_image_with_annotation(img, bb, cls, img_idx)



