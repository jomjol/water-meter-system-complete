## Changelog
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
##### 4.4.0 (2019-12-27)
* Change to new base image: export OpenCV and Tensorflow in new base images (for Raspberry and Synology Version)
##### 4.3.0 (2019-12-20)
* Update roi.jpg on every run
##### 4.2.1 (2019-12-17)
* Workaround for memory leak in tensorflow function predict() - see [https://github.com/keras-team/keras/issues/13118](https://github.com/keras-team/keras/issues/13118)
##### 4.2.0 (2019-12-07)
* Reading of analog counters is enabled or disabled via config.ini **special thanks to alikanarya**
##### 4.1.1 (2019-11-29)
* Error correction in ReadDigitalDigitClass.py
##### 4.1.0 (2019-11-25)
* Upgrade to Tensorflow 2.0
* Changed image processing within CNN to Pillow (instead of OpenCV)
* Training analog and digital CNN with additional type of counter and digits respectivelely
##### 3.0.2 (2019-11-07)
* Correct error for disable Logging
##### 3.0.1 (2019-11-03)
* Update to Pillow 6.2.0
##### 3.0.0 (2019-10-06)
* Impementation of optional consistency check of readout value (not negative, maximum rate)
##### 2.3.0 (2019-10-05)
* Load default configuration, if none is present (beneficial for Docker-Version with mounted config and log directories)
* Parameter "simple" to reduche output to a single value
##### 2.2.0 (2019-09-18)
* Update neural network for readout analog meter
* storage and usage of last full readouts to substitute "NaN" values in digital counters
##### 2.1.0 Integration of direct request to Image provider
* The image soucre can be specified within in the config.ini. If no "url"-Parameter is given, the image will be pulled directly from the given source, including logging.
* Update of the name convention of the log-files from Unix-Timestamp to Human-Readable time coding
##### 2.0.0 Implementation in Python
* Usage of improved analog detection (sinus and cosinus coding)
* New folder structure to support easy implementation in Docker-ContainerUp
* **Attention:** adaption of INI-File needed, as Python is handling this slightly different 
##### 1.x.y Initial Version within NodeJS
* Implemenation of neural networks with version 1.x (analog and digital)
neuron