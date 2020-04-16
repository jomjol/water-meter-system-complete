# water-meter-system-complete

This repository describes a readout of an analog water meter with the help of a camera and image processing, including neural network processing to extract the values.
The interface is a local HTTP-server, that takes an image as input, processes it and gives as an output the readout of the water meter counter, including the subdigits.

Although the server can be installed manually in a windows as well as an Linux system, it is strongly recommended to use the provided docker containers. The installation is due to the use of image processing (OpenCV, ...) and Neural Network Systems (Tensorflow) not really straight forward and I needed a lot of try and error. 

**Therefore I have decided to capsule the server in a docker container**. 

This is available for an Intel based System (e.g. Synology Docker) as well as an Raspberry PI Version.


## Docker-Versions
| Label | 	Content  | Comments   |
| -------------- | ------------- | ------------- |
| rolling | Experimental version for amd64-systems (e.g. Intel processors) | newest features, not fully tested |
| raspi-rolling | Experimental version for armv7-systems (Raspberry PI3 and higher) | newest features, not fully tested  |
| latest | Latest stable version for amd64-systems (e.g. Intel processors) | Currently identical to 5.6.1 (2020-03-12) |
| raspi-latest | Latest stable version for armv7-systems (Raspberry PI3 and higher) | Currently identical to 5.6.1 (2020-03-12) |
| v4.x | Update to Tensorflow 2.0, fully automated build | Details see below |
| v3.x | Tensorflow 1.4, manual build | Details see below  |


## Running docker
Choose for the fitting docker tag and run the server with the following parameters:

```docker run -p 3000:3000 --mount type=bind,source="$(pwd)"/config/,target=/config --mount type=bind,source="$(pwd)"/log/,target=/log jomjol/wasserzaehler:DOCKER_TAG```

#### Paramters
| Parameter | 	Meaning  | Example |
| -------------- | ------------- | ------------- |
| PATH_TO_LOCAL_CONFIG | Configuration parameters are stored in this path - easeast way to handle is a local copy of this directory | ```/home/pi/config``` |
| PATH_TO_LOCAL_LOG | Logging paramters and images are stored in in this path - easeast way to handle is a local copy of this directory | ```/home/pi/config``` |
| DOCKER_TAG | Docker tag for the correct docker version | ```raspi-latest``` |

The config and the log directory can be empty at the very first start. They will be loaded with a default configuratio, that can be modified afterwards.

### Development
To test your local changes run `docker build -t watermeter .` and 
`docker run -p 3000:3000 --mount type=bind,source="$(pwd)"/config/,target=/config --mount type=bind,source="$(pwd)"/log/,target=/log watermeter`.

## Changelog - lastest version
##### 5.6.1 (2020-03-12)
* Correct error in docker commmand (remove space character in bind)
##### 5.6.0 (2020-03-07)
* Internal update of config.ini handling (started)
* Update roi.html
##### 5.5.2 (2020-02-23)
* Modification of Errortext in case RateToHigh, NegativeRate (Blank after "Error", e.g. "ErrorRateToHigh" --> "Error - RateToHigh")
* Change MaxRateValue from 0.1 to 0.2 in Default Config.ini
##### 5.5.1 (2020-02-15)
* Update CNN-Digital to v5.0.0 (improved training data from iobroker users)
* Update CNN-Analog to v5.0.0 (improved training data from iobroker users)
##### 5.5.0 (2020-02-12)
* Update CNN-Digital to v4.2.0 (improved training data from iobroker users)
##### 5.4.9 (2020-01-27)
* Extensdion to json output: ../wasserzaehler.json
##### 5.3.0 (2020-01-08)
* Integration of storage of prevalue in file to reload on startup
* Correction of drawing analog counter ROIs even if they are disabled
##### 5.2.0 (2020-01-03)
* Raspberry Version: Remove autorestart (not working) - instead: use cron job for regular restart to handle tensorflow memory leak [Setting up cron job](https://github.com/jomjol/water-meter-system-complete/blob/raspi-rolling/Raspi-Cron-Job.md)
##### 5.1.0 (2019-12-28)
* Raspberry Version: Autorestart on Python Crash of wasserzaehler.py
##### 5.0.0 (2019-12-28)
* Separate environmental setup to dedicated Docker images (for Raspberry: raspi-opencv-tensorflow and for Synology (Intel w/o AVX2): synology-opencv-tensorflow)

### [Full Changelog](https://github.com/jomjol/water-meter-system-complete/blob/raspi-rolling/Changelog.md)


The overall system with description of the single steps is described here: [https://github.com/jomjol/water-meter-measurement-system](https://github.com/jomjol/water-meter-measurement-system)

A graphical overview about the steps is shown in the following flow:

<img src="https://github.com/jomjol/water-meter-system-complete/blob/master/images/signal_flow.png" width="800"> 

## Setup

To run the Python code copy the whole [code](code) directory including subdirectory.

Path are relative, so it should run immediately with the following command:
* `pip install requirements.txt`
* `python wasserzaehler.py`

### Configuration

The configuration is stored in the subdirectory `config`. In the Ini-file the CNN-Network to be loaded is listed. Configuration of the neural network (*.h5) itself is stored in the subdirectory `neuralnets`.
Detailed information on config.ini see [Config_Description.md](Config_Description.md)

##### Consistency Check
There is a consistency check of the readout value implemented. Prequesite for this check is a storage of the last full readout (without "N"), which can be achieved by the parameter "usePreValue".

		
	
## Running the server

The server is listening to port 3000 and accepts requests in the following syntac:

* http://server-ip:3000/wasserzaehler.html

| Parameter | Meaning | example |
| --------- | ------- | ------- |
| server-ip | address of the node-server running the script | `localhost` |

Without any parameter and correct setting in the CONFIG.INI the server responses with an readout of the water meter:
<img src="https://github.com/jomjol/water-meter-system-complete/blob/master/images/server_output.png" width="400">

The output of the server are 3 numbers, separated by a tabulator.

| Number | Meaning | 
| --------- | ------- |
| First number | Full readout, including main digits and subdigits, leading zeros are suppresed |
| Second number | Direct readout of the digital digits, including leading zeros |
| Third number | post digit numbers |

##### Remark
If a digit cannot be recognized, e.g. because it is half between 2 digits, then instead of the number a "N" is written at the corresponding position. In this case a direct conversion to a number will not work. Additional information (e.g. last valid full reading) needs to be used to extrapolate the missing digit (see below).


### Optional parameters

* http://server-ip:3000/wasserzaehler.html?url=http://picture-server/image.jpg&full
* http://server-ip:3000/wasserzaehler.html?usePreValue
* http://server-ip:3000/wasserzaehler.html?single

| Parameter | Meaning | example |
| ----- | ------- | ------ |
| url | url to a dedicated picture to be analysed | `url=http://picture-server/image.jpg` |
| full | response extended by details on readout process | `full` |
| usePreValue | if available the last fully valid readout is used to complete unambigoius digits ('N'). The prevalue can be set manuelly by 'setPreValue.html' - see below | `usePreValue` |
| single | only a singel number is given back instead of combinded value, digital and analog readouot | `single` |

The paramaters can be combined arbitrary.

Example with parameter `full`:

<img src="https://github.com/jomjol/water-meter-system-complete/blob/master/images/sever_output_full.png" width="400">

## Additional Settings
* http://server-ip:3000/roi.html

The page `roi.html` return the image including the ROIs visible. This is usefull to check for correct setting:
<img src="https://github.com/jomjol/water-meter-system-complete/blob/master/images/roi_masked.jpg" width="400">

* http://server-ip:3000/setPreValue.html?value=401.57

The page `setPreValue.html` stores the number given in the parameter `value` to initiate the internal storage of a valid data. This can be used, in case the digital counter is between two number and cannot be readout uniquely at the moment.

| Parameter | Meaning | example |
| --------- | ------- | ------- |
| value | valid setting of water meter readout | `value=401.57` |

* http://server-ip:3000/version.html

The page `version.html` returns a version number.
   



