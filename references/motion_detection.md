## Motion detector setup (WIP)

```
docker build -t detector -f Dockerfile.detector .

docker run --name detector --network nx_default --privileged --runtime nvidia --rm -v /data:/data -e DISPLAY -v /tmp:/tmp -v $PWD:/usr/src/app -ti detector 
```

https://docs.opencv.org/master/de/de1/group__video__motion.html