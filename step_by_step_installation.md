# Step by step instruction

This is a step by step instruction to install the wasserzaehler.js server including all dependencies on a linux server system.


## Prequisite
This instruction was tested on a Ubuntu 19.04. Linux system. The system was tested on a desktop as well as an server (terminal) version.
The system was tested in a VirtualBox environment, in which the Ubuntu system was freshly installed. All updates were installed previously:

1. ``sudo apt update``
2. ``sudo apt upgrade``


### Remark
Installation on a Ubuntu 18.04 LTS failed. The node.js version (8.10) is not compatible with the tensorflow requirements

## Installation

Run following command - Especially command 1 and 2 takes a longer time (1: a lot to load, 2: download and compile):
1. ``sudo apt install nodejs npm git build-essential cmake pkg-config python``
2. ``sudo npm install @tensorflow/tfjs @tensorflow/tfjs-node @tensorflow/tfjs-core`` 
3. ``npm install --save opencv4nodejs``
4.



## Support
As the code is not foul proof it will crash as soon as something unexpected will happen. E.g. file-link is not working or the JPG-image is corrupted.

There are several strategies to handle this. One could extend the code with extended error management. This is very time consuming and might make the code much more complicated. 

I'm using another approach: as soon as the code crashes, it will be restarted automatically. This can be very easy be implemented with [http://pm2.keymetrics.io/](http://pm2.keymetrics.io/). 
Two topics can handled very easy: restart of the system and automatic start of the wasserzaehler.js and restart of the server in cases it crashes