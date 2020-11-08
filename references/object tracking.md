

## Object tracking
We tried multiple appraoches described below and found 3rd approach as the most suitable approach. 

- approach 1: motion tracking lab (lab3) (dynamic background comparing to previous snap shot)
- approach 2: similar to 1, but comparing to static background (frist snap shot)
	- more sensitive than approach 1
- ***approach 3***: semi-automatic 
	- draw the rect and follow 

[TODO] finish up the code for approach 3
[TODO] create docker file (pythons, opencv)


#### Camera frame 
```
docker build -t detector -f Dockerfile.detector .

docker run --name detector --network nx_default --privileged --runtime nvidia --rm -v /data:/data -e DISPLAY -v /tmp:/tmp -v $PWD:/usr/src/app -ti detector 
```


#### Motion detection (WIP)

```
docker build -t detector -f Dockerfile.detector .

docker run --name detector --network nx_default --privileged --runtime nvidia --rm -v /data:/data -e DISPLAY -v /tmp:/tmp -v $PWD:/usr/src/app -ti detector 
```

https://docs.opencv.org/master/de/de1/group__video__motion.html



Mounting s3fs 

```
mv /.passwd-s3fs ~/.
chmod 600 ~/.passwd-s3fs

s3fs toylocator data/processed


-o url="https://s3-us-west-2.amazonaws.com"

```



