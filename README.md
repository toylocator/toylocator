# Toy Locator

## Problem 

> Leo (4 years old): Mommy, have you seen my spiderman?
>
> Mom: No. I saw it yesterday from the bathroom. 
>
> (after 10 mins) 
>
> Dad: Honey, have you seen my key?
>
> Mom: You ask everyday. Can you put it next to the door where it should be? 
>
> Dad: That is not the answer I was looking for. 
>
> (silence) 

2 years Later

> Leo (6 years old): Hey toy locator, where is the blue Ironman. 
>
> Toy Locator: The blue Ironman is at bedroom number 2 right below the red chair on the left side of the room.
>
> Leo: Thanks Toy Locator. 
>
> Toy Locator: You are welcome. 

## overall architecture / flow 

#### (Temp Name: Labeller) creating training dataset 
- simplification: mobile phone -> nx camera -> raw input video file
- input prep: create video manually
- input: video 
- output: datasets forr single object 
- parse images, augment 
 - create training datasets / test datasets 

#### Training the model 
- input: dataset 
- output: model 
- (todo): how well it performs without labeling 
1. Pre-trained model (imagenet, yolov5, googlenet)
2. train model and test 
 
#### Inteferece 
- simplification: live video -> image of scene 
- testing prep: manually label objects from scenes
- input: image of scene, object name (e.g., blue spiderman)
- output: rectangular on the image 

#### Broker  
- something to think about 
- each device needs to update the model the central device 
- federated learning? 


## set up 


## Phase 1 
#### Training (transfer learning or embedding) on mobile phone or NX or Raspberry Pi
1. Pre-trained model (imagenet, yolov5, googlenet) 
2. Load them 
3. Capturing video 
4. Augment to increase training set 
5. Create training set (separate out test set) 

#### Testing Phase 1  
1. Test against (separate out test set)

#### Testing Phase 2
1. Show set of images that has toy or objects alones

#### Testing Phase 3 
- Input
	- scenes of rooms (one or multiple of them has the object)
- Output
	- detect objects with probability 
