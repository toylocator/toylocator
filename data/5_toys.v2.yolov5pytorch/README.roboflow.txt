
4 toys - v2 2020-10-24 11:26am
==============================

This dataset was exported via roboflow.ai on October 24, 2020 at 6:27 PM GMT

It includes 395 images.
Toys are annotated in YOLO v5 PyTorch format.

The following pre-processing was applied to each image:
* Auto-orientation of pixel data (with EXIF-orientation stripping)
* Resize to 416x416 (Stretch)

The following augmentation was applied to create 3 versions of each source image:
* Equal probability of one of the following 90-degree rotations: none, clockwise, counter-clockwise
* Random rotation of between -15 and +15 degrees
* Salt and pepper noise was applied to 5 percent of pixels


