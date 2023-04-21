# OpenMiDaS: Edge-based Monocular Depth Estimation

OpenMiDaS utilizes Gabriel, a platform originally designed for wearable cognitive assistance applications, to stream image data to the backend server which runs an cognitive engines to perform monocular depth estimation. The resulting colormapped images are sent back to the device.

Copyright &copy; 2023
Carnegie Mellon University

This is a developing project.

## License

Unless otherwise stated in the table below, all source code and documentation are under the GPL, Version 2.0.
A copy of this license is reproduced in the [LICENSE](LICENSE) file.


## Prerequisites

OpenMiDaS uses the [MiDaS](https://github.com/isl-org/MiDaS) models from pyTorch hub  for monocular depth estimation. It has been tested on __Ubuntu 20.04 LTS (focal)__. It requires an nVidia GPU.

OpenMiDaS has an Android client that is available on the [Google PlayStore](https://play.google.com/store/apps/details?id=edu.cmu.cs.openmidas). It requires an Android device running Android 7.0+ (API level 33).

## Server Installation using Docker

The quickest way to set up an OpenMiDaS server is to download and run our pre-built Docker container.  All of the following steps must be executed as root. We tested these steps using Docker 19.03.

### 1. Install Docker and docker-compose

If you do not already have Docker installed, install it using the steps in this [Docker install guide](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/).

### 2. Ensure an NVIDIA driver is installed

You can use the [CUDA Download page](https://developer.nvidia.com/cuda-downloads) to learn how to install the driver.

If you think you may already have an NVIDIA driver installed, run `nvidia-smi`. The Driver version will be listed at the top of the table that gets printed.

### 3. Install the [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-docker)

Follow [these instructions](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker).


### 4. Obtain  Docker images

```sh
docker pull cmusatyalab/openmidas:stable
```

### 5. Configure the environment for OpenMiDaS

In the `~/openmidas/server/` directory, there is a template.env file that can be used as an example docker-compose environment. Copy it to .env and then modify it to control things such as the MiDaS model to use.

```sh
cd ~/openmidas/server/
cp template.env .env
#edit .env file as necessary
```

### 5. Launch the Docker containers with docker-compose

To launch all the containers and interleave the output from each container in the terminal:

```sh
cd ~/openmidas/server
docker-compose up
```

If you wish to launch the containers in the background, you can pass the -d flag to docker compose. You can then use docker logs to inspect what is happening to individual containers.

```sh
cd ~/openmidas/server
docker-compose up -d
```

### 7. Tearing down

Hitting CTRL-C while `docker-compose up` is running will stop the containers. However to explicitly destroy them, you can use `docker-compose down`. This will also destroy the networks.

## Android Client Installation

You can download the client from the [Google Play Store](https://play.google.com/store/apps/details?id=edu.cmu.cs.openmidas).

Alternatively, you can build the client yourself using [Android Studio](https://developer.android.com/studio). The source code for the client is located in the `android-client` directory. You should use the standardDebug [build variant](https://developer.android.com/studio/run#changing-variant).

### Managing Servers

Servers can be added by entering a server name and address and pressing the + sign button. Once a server has been added, pressing the 'Connect' button will connect to the OpenMiDaS server at that address. Pressing the trash can button will remove the server from the server list.

### Settings

#### General

* Show Screenshot/Recording Buttons - This will enable icons to allow you to capture video or screenshots while running OpenMiDaS.
* Display Metrics - Enabling this option will show the metrics including FPS.

#### Experimental

* Resolution - Configure the resoultion to capture at. This will have a moderate impact in the computation time on the server.
* Gabriel Token Limit - Allows configuration of the token-based flow control mechanism in the Gabriel platform. This indicates how many frames can be in flight before a response frame is received back from the server. The minimum of the token limit specified in the app and the number of tokens specified on the server will be used.
* MiDaS Model - Configure the model used on the server. MiDaS has 3 pretrained models: Large, Hybrid, and Small.
* Colormap - Configure which colormap to apply to the depth estimation. These correspond to OpenCV's [colormaps](https://docs.opencv.org/3.4/d3/d50/group__imgproc__colormap.html#ga9a805d8262bcbe273f16be9ea2055a65).

### Front-facing Camera

Once connected to a server, an icon is displayed in the upper right hand corner which allows one to toggle between front- and rear-facing cameras.


## Credits

Please see the [CREDITS](CREDITS.md) file for a list of acknowledgments.
