# Docker 

### Learning Resources
- https://docker-curriculum.com
- https://youtu.be/pTFZFxd4hOI
- https://www.linkedin.com/learning/learning-docker-2018

### Key Concepts
- What is the Docker? Docker is a tool which is used to automate the deployment of applications in lightweight containers so that applications can work in different environments.
- In short, Docker enables users to bundle an application together with its preferred execution environment to be executed on a target machine
- Dockerfiles are small programs designed to describe how to build a Docker image.
- What is Docker Image? The Docker Image is a set of files and a combination of parameters will which allow creating the application instances and run them in separate containers
    - The template with instructions which is used to for creating Docker Containers
    - It is build using a file called a Docker File
    - They are stored in a Docker hub
- What is Docker Container? Docker container is a runtime which includes the application and all of its dependencies. It shares the kernel with other containers, running as isolated processes in user space on the host operating system.
- What is true about virtualization and containerization? 
    - Containers provide an isolated environment for running the application. Containers are an abstraction of the application layer. Each container is a different application. 
    - In virtualization hypervisors provide an entire virtual machine to the guest (including Kernel)


```shell
$ docker pull ubuntu
$ docker images
$ docker image ls
$
$ docker run -ti ubuntu:latest bash # ti = terminal interactive
$ # then change something in ubuntu
$ docker commit container_id new_image # after making the changes
$ 
$ docker run --rm -ti ubuntu # remove container after exit
$
$ docker run -d -ti ubuntu bash # run in a detached mode, background mode
$ docker ps # show all containers running
$ docker attach container_name # go back to container, detach again ctrl+p, ctrl+q
$ 
$ docker exec -ti container_name bash # start another process in existing container, reflects the changes
$ 
$ docker logs container_name
$ 
$ docker kill container_name # stops the container
$ docker kill container_name # stops the container, terminates the process
$ docker rm container_name # removes the container
$
$ docker port container_name # list port mappings or a specific mapping for the container
$ 
$
$
$
$
$
```

### Dockerfile
A [Dockerfile](https://docs.docker.com/engine/reference/builder/#from) is a simple text file that contains a list of commands that the Docker client calls while creating an image. 

We start with specifying our base image. Use the FROM keyword to do that 
```dockerfile
FROM python:3 
```
The next step usually is to write the commands of copying the files and installing the dependencies 
```dockerfile
# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt
```
Port number that needs to be exposed
```dockerfile
EXPOSE 5000
```
The last step is to write the command for running the application, which is simply - `python ./app.py`. We use the CMD command to do that 
```dockerfile
CMD ["python", "./app.py"]
```
To build image:
```shell
$ docker build -t rustamepam/image_name .
docker run -p 8888:5000 rustamepam/image_name
```