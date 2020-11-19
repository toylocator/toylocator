Toy Locator
==============================

Deep Learning application to locate a toy at a household

## :fearful: Challenge 
- labelling automatically
- detecting 3 dimensional objects (computer vision, object detection)
- incremental training (overcoming catastropic forgetting)
- training on edge device (minimum computing resources)

## :weary: Overall Architecture / Flow 
1. Collect: images from camera 
2. Label: automaticallly with the minimum input by the user (select area at the beginning and enter the name) with yolov5 format
4. Process: augmentation 
5. Train: 
6. Deploy: Download the model on the device and detect the object real time
7. Display
	1. Show on the screen the location of the specific object 
	2. Announce the location of the toy

![](references/overall_arch_cloud.png)

## (Toy Registration) creating (additional) dataset

#### 1. Collect and Label Images from camera 
- ***input***: webcam
- ***output***: labelled images 
- Using Deep SORT mechanism to track the image once labelled. 
- See more on [different approaches to annotate toys](annotation)

#### 2. Process Images
- ***input***: labelled images 
- ***output***: dataset
 augment, split dataset and creat data.yaml 
1. Resize to similar to camera 
2. Augment annotated images
	1.  augment (rotate, noise, flip, etc) images using [image_augmentor](https://github.com/codebox/image_augmentor)
	2.  handling annotation during the processing images :question:

#### 3. Train the model 
- ***input***: dataset
- ***output***: models (best.pt) 
1. Pre-trained model (e.g., yolov5)
2. Train model and test (determine if the model is good enough to be distributed
See more on [training on the AWS](training)

#### 4. Inference 
- ***input***: live feed from camera 
- ***input***: object name (e.g., blue dump truck)
- ***input***: trained models 
- ***output***: rectangular on the image or display
- See more on [inference from images or camera](inferences)
- simplification: live video -> image of scene 
- testing prep: manually label objects from scenes

## Problem 

> Leo (4 years old): Mommy, have you seen my spiderman?
>
> Mom: No. I saw it yesterday from the bathroom. 
>
> (after 10 mins) 
>
> Dad: Honey, have you seen my key?
>
> Mom: You ask everyday. Can you put it in the bowl next to the entrace where it should be? 
>
> Dad: That is not the answer I was looking for. 
>
> (silence) 

2 years Later

> Leo (6 years old): Hey toy locator, where is the blue Ironman. 
>
> Toy Locator: The blue Ironman is at bedroom number 2 right below the red chair on the left side of the room.
>
> Leo: Thanks Toy Locator!
>
> Toy Locator: You are welcome! 




<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
