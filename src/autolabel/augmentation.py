import numpy as np
import cv2
import utils as u
import random
import glob
import os

raw_path = "../../data/raw/"
input_path = "../../data/augmented/"

txt_file_path = raw_path + 'latest_label.txt'
with open(txt_file_path, 'r') as file:
    obj = file.read()

rawImage_dir = '../../data/raw/{}/'.format(obj)
augImage_dir = '../../data/augmented/{}/'.format(obj)

if not os.path.exists(augImage_dir):
    os.makedirs(augImage_dir)
else:
    print("An obejct with the same name exists; please use a different name and try again:)")
    exit()

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

image_paths = get_lists_in_dir(rawImage_dir)
image_list = os.listdir(rawImage_dir)

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

bbox_path = raw_path + obj + '_annotations.txt'
with open(bbox_path, 'r') as file:
    content = file.read().splitlines()
    dimension_list = []
    for n in content:
        x1 = int(n.split()[0])
        y1 = int(n.split()[1])
        x2 = int(n.split()[0]) + int(n.split()[2])
        y2 = int(n.split()[1]) + int(n.split()[3])
        
        dimension_list.append([x1,y1,x2,y2])

i = 0
for n in range(len(image_paths)):
    original_image = cv2.imread(image_paths[n], cv2.IMREAD_COLOR)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    img, bb = rotate_image(original_image, 30, dimension_list[int(image_paths[n].split('_')[1].split('.')[0])])
    cv2.rectangle(img, (bb[0], bb[1]), (bb[2], bb[3]) , (255, 0, 0), 2, 1)
    cv2.imwrite(input_path+obj+"/"+obj+"_"+"aug"+"_"+str(i)+".jpg", img)
    i += 1
       
    aug_bbox = int(bb[0]), int(bb[1]), int(bb[2]) - int(bb[0]), int(bb[3]) - int(bb[1])
    aug_bbox_path = input_path + 'aug_bbox_information.txt'
    with open(aug_bbox_path, 'a') as file:
        file.write(" ".join([str(a) for a in aug_bbox]) + '\n')

    img, bb = rotate_image(original_image, 60, dimension_list[int(image_paths[n].split('_')[1].split('.')[0])])
    cv2.rectangle(img, (bb[0], bb[1]), (bb[2], bb[3]) , (255, 0, 0), 2, 1)
    cv2.imwrite(input_path+obj+"/"+obj+"_"+"aug"+"_"+str(i)+".jpg", img)
    i += 1
    
    aug_bbox = int(bb[0]), int(bb[1]), int(bb[2]) - int(bb[0]), int(bb[3]) - int(bb[1])
    with open(aug_bbox_path, 'a') as file:
        file.write(" ".join([str(a) for a in aug_bbox]) + '\n')

    img, bb = rotate_image(original_image, 90, dimension_list[int(image_paths[n].split('_')[1].split('.')[0])])
    cv2.rectangle(img, (bb[0], bb[1]), (bb[2], bb[3]) , (255, 0, 0), 2, 1)
    cv2.imwrite(input_path+obj+"/"+obj+"_"+"aug"+"_"+str(i)+".jpg", img)
    i += 1

    aug_bbox = int(bb[0]), int(bb[1]), int(bb[2]) - int(bb[0]), int(bb[3]) - int(bb[1])
    with open(aug_bbox_path, 'a') as file:
        file.write(" ".join([str(a) for a in aug_bbox]) + '\n')

    img, bb = width_shift_image(original_image, 0.2, dimension_list[int(image_paths[n].split('_')[1].split('.')[0])])
    cv2.rectangle(img, (bb[0], bb[1]), (bb[2], bb[3]) , (255, 0, 0), 2, 1)
    cv2.imwrite(input_path+obj+"/"+obj+"_"+"aug"+"_"+str(i)+".jpg", img)
    i += 1

    aug_bbox = int(bb[0]), int(bb[1]), int(bb[2]) - int(bb[0]), int(bb[3]) - int(bb[1])
    with open(aug_bbox_path, 'a') as file:
        file.write(" ".join([str(a) for a in aug_bbox]) + '\n')

    img, bb = width_shift_image(original_image, 0.4, dimension_list[int(image_paths[n].split('_')[1].split('.')[0])])
    cv2.rectangle(img, (bb[0], bb[1]), (bb[2], bb[3]) , (255, 0, 0), 2, 1)
    cv2.imwrite(input_path+obj+"/"+obj+"_"+"aug"+"_"+str(i)+".jpg", img)
    i += 1
    
    aug_bbox = int(bb[0]), int(bb[1]), int(bb[2]) - int(bb[0]), int(bb[3]) - int(bb[1])
    with open(aug_bbox_path, 'a') as file:
        file.write(" ".join([str(a) for a in aug_bbox]) + '\n')

    img, bb = height_shift_image(original_image, 0.2, dimension_list[int(image_paths[n].split('_')[1].split('.')[0])])
    cv2.rectangle(img, (bb[0], bb[1]), (bb[2], bb[3]) , (255, 0, 0), 2, 1)
    cv2.imwrite(input_path+obj+"/"+obj+"_"+"aug"+"_"+str(i)+".jpg", img)
    i += 1
 
    aug_bbox = int(bb[0]), int(bb[1]), int(bb[2]) - int(bb[0]), int(bb[3]) - int(bb[1])
    with open(aug_bbox_path, 'a') as file:
        file.write(" ".join([str(a) for a in aug_bbox]) + '\n')

    img, bb = height_shift_image(original_image, 0.4, dimension_list[int(image_paths[n].split('_')[1].split('.')[0])])
    cv2.rectangle(img, (bb[0], bb[1]), (bb[2], bb[3]) , (255, 0, 0), 2, 1)
    cv2.imwrite(input_path+obj+"/"+obj+"_"+"aug"+"_"+str(i)+".jpg", img)
    i += 1

    aug_bbox = int(bb[0]), int(bb[1]), int(bb[2]) - int(bb[0]), int(bb[3]) - int(bb[1])
    with open(aug_bbox_path, 'a') as file:
        file.write(" ".join([str(a) for a in aug_bbox]) + '\n')

    img, bb = horizontal_flip(original_image, dimension_list[int(image_paths[n].split('_')[1].split('.')[0])])
    cv2.rectangle(img, (bb[0], bb[1]), (bb[2], bb[3]) , (255, 0, 0), 2, 1)
    cv2.imwrite(input_path+obj+"/"+obj+"_"+"aug"+"_"+str(i)+".jpg", img)
    i += 1

    aug_bbox = int(bb[0]), int(bb[1]), int(bb[2]) - int(bb[0]), int(bb[3]) - int(bb[1])
    with open(aug_bbox_path, 'a') as file:
        file.write(" ".join([str(a) for a in aug_bbox]) + '\n')

    img, bb = scale_image(original_image, 0.5, dimension_list[int(image_paths[n].split('_')[1].split('.')[0])])
    cv2.rectangle(img, (bb[0], bb[1]), (bb[2], bb[3]) , (255, 0, 0), 2, 1)
    cv2.imwrite(input_path+obj+"/"+obj+"_"+"aug"+"_"+str(i)+".jpg", img)
    i += 1

    aug_bbox = int(bb[0]), int(bb[1]), int(bb[2]) - int(bb[0]), int(bb[3]) - int(bb[1])
    with open(aug_bbox_path, 'a') as file:
        file.write(" ".join([str(a) for a in aug_bbox]) + '\n')

    img, bb = scale_image(original_image, 1.5, dimension_list[int(image_paths[n].split('_')[1].split('.')[0])])
    cv2.rectangle(img, (bb[0], bb[1]), (bb[2], bb[3]) , (255, 0, 0), 2, 1)
    cv2.imwrite(input_path+obj+"/"+obj+"_"+"aug"+"_"+str(i)+".jpg", img)
    i += 1

    aug_bbox = int(bb[0]), int(bb[1]), int(bb[2]) - int(bb[0]), int(bb[3]) - int(bb[1])
    with open(aug_bbox_path, 'a') as file:
        file.write(" ".join([str(a) for a in aug_bbox]) + '\n')

    img = sp_noise(original_image,0.1)
    cv2.imwrite(input_path+obj+"/"+obj+"_"+"aug"+"_"+str(i)+".jpg", img)
    i += 1

    aug_bbox = int(bb[0]), int(bb[1]), int(bb[2]) - int(bb[0]), int(bb[3]) - int(bb[1])
    with open(aug_bbox_path, 'a') as file:
        file.write(" ".join([str(a) for a in aug_bbox]) + '\n')







