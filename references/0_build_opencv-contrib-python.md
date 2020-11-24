#### Building opencv-contrib-python
- [build script](https://github.com/AastaNV/JEP/blob/master/script/install_opencv4.3.0_Jetson.sh))
- [NVIDIA forum](https://forums.developer.nvidia.com/t/how-to-install-opencv-contrib-python-on-xavier/76549)

- once compiled, ``````
```
./install_opencv4.3.0_Jetson.sh /usr/lib

tar -zcvf my-opencv-4.3.0.tar.gz /usr/lib/opencv-4.3.0

```


#### Using opencv docker (not working for some reason)
[using opencv docker](https://hub.docker.com/r/mdegans/tegra-opencv/tags)
- https://forums.developer.nvidia.com/t/installing-opencv-contrib-for-nano/73932