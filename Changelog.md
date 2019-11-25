## Changelog
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