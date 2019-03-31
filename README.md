## SSH Metric Monitoring
Simple client-server ssh login attempt monitoring based on python3 and socket module to communicate between alphaclient and alphaserver. The app will build and packaged in the docker container, and for the basic infrastructure like networking managed via docker-compose file to automate the deployment.

## Prerequisite
Before we go we need the following application installed on the system  
- [docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/) 
- [docker-compose](https://docs.docker.com/compose/install/)

**Note:**

This readme guideline created base on Ubuntu 18.04.2 LTS with the following `docker` and `docker-compose` versions:

- Docker version 18.09.4, build d14af54266
- docker-compose version 1.24.0, build 0aa59064

## How to use?

First we need to clone the asgard repository
```
$ git clone https://github.com/hmashudi/asgard.git
```

Once it's done go to asgard directory
```
$ cd asgard/
```

Run docker compose to build docker image and deploy the containers

```
$ docker-compose up --build -d
```

**Note:** `--build` this option is to build the docker image first based on the `Dockerfile` inside of both `alphaserver` and `alphaclient` directory, and `-d` this option will detach the containers once they are created.


## How to verify?

1. Check the docker containers status both for `alphaserver` and `alphaclient`
```
$ docker-compose ps
    Name                Command            State    Ports  
-----------------------------------------------------------
alphaclient_1   /bin/sh ./startup.sh       Up      22/tcp  
alphaclient_2   /bin/sh ./startup.sh       Up      22/tcp  
alphaserver     python3 ./alphaserver.py   Up      5000/tcp
```

2. Once the cluster up and running, follow the docker logs for `alphaserver` container as follow
```
$ docker logs -f alphaserver 
Socket created
Socket now listening
Received connection from 10.5.0.6:52106
Received connection from 10.5.0.7:37384
```
As above log shown that `alphaserver` socket creation, listening status and right now ready for receiving connection from `alphaclient`, and also from the log we can see there are incoming connection from `alphaclient` IP addresses that are ready to report the SSH login attempt metric.  

3. Open new terminal and try to SSH to `alphaclient` containers with the following details

- SSH user: `root`
- SSH password: `PASSWORD`

SSH to alphaclient_1 container
```
ssh root@10.5.0.6
root@10.5.0.6's password:
```
SSH to alphaclient_2 container
```
ssh root@10.5.0.7
root@10.5.0.7's password: 
```
4. Check again docker logs on the `alphaserver` container
```
$ docker logs -f alphaserver 
Socket created
Socket now listening
Received connection from 10.5.0.6:52106
Received connection from 10.5.0.7:37384
Processed result: ba6b51e048c4 had 1 attempt of ssh session
Processed result: 3c523ec1e7be had 1 attempt of ssh session
```
As we can confirm on above log `alphaclient_1` and `alphaclient_2` containers reported the SSH login attempt to `alphaserver`

## How it work?

There are 2 logic we spilt it on the `alphaserver` and `alphaclient`

**alphaserver:**
- the `alphaserver` is responsible to open and listening socket used for communication from/to alphaclient.
- manage active thread so it can handle multiple `alphaclient` instance.
- processing/decode the input received from `alphaclient` and present it.

**alphaclient:**
- `alphaclient` is responsible for monitor and following the log written by SSH process during startup.
- Check for login activity on the SSH log (/var/log/sshd.log).
- send login attempt data to `alphaserver`.
