# Toy Locator

> Leo (4 years old): Mommy, have you seen my spiderman?

> Mom: No. I saw it yesterday from the bathroom. 

> (after 10 mins) 

> Dad: Honey, have you seen my key?

> Mom: You ask everyday. Can you put it next to the door where it should be? 

> Dad: That is not the answer I was looking for. 

> (silence) 

#### after 2 years

> Leo (6 years old): Hey toy locator, where is the blue Ironman. 

> Toy Locator: The blue Ironman is at bedroom number 2 right below the red chair on the left side of the room.

> Leo: Thanks Toy Locator. 

> Toy Locator: You are welcome. 


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
