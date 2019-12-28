## Changelog
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