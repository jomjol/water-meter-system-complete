# water-meter-system-complete

## Version
##### 1.0 Initial Version
##### 2.0 Update the Analog Counter Convert to "analog_needle_readout_Version2"
* Improved stability of analog counter conversion
##### 2.1 Update the Analog Counter Convert to "analog_needle_readout_Version2_2"
* Improved stability of analog counter conversion
##### 2.2 Adaption to implement Docker container
* Moved all configuration settings to subfolder ''/config'' - including teached CNNChanged
* Changed internal loading of NN-model (tf.LoadLayersModel) to server modus (internal small file server for model via exprss on port 33123) 
 
This repository is the sum of different projects to read out an analog water meter with the help of a camera and image processing, including neural network processing to extract the values.
The result is a HTTP-server, that takes an image as input, processes it and gives as an output the water meter number, including the subdigits.

The overall system with description of the single steps is described here: [https://github.com/jomjol/water-meter-measurement-system](https://github.com/jomjol/water-meter-measurement-system)

A graphical overview about the steps is shown in the following flow:

<img src="./images/signal_flow.png"> 

The code is implented in node.js. To run it copy the whole [code](code) directory including subdirectory.

Path are relative, so it should run immediatly with the following command:
* `node wasserzaehler.js`

### Remarks
* Node assumes some libraries to be installed using `npm install`:
	* `ini`, `http`, `url`
    * `opencv4nodejs`, `jpeg-js`
    * `@tensorflow/tfjs-node`, `@tensorflow/tfjs`
	
	
	
## Running the server

The server is listening to port 3000 and accepts requests in the following syntac:

* http://server-ip:3000/?url=http://picture-server/image.jpg&full

| Parameter | Meaning | example |
| --------- | ------- | ------- |
| server-ip | address of the node-server running the script | `localhost` |
| url | url to the picture to be analysed | `url=http://picture-server/image.jpg` |
| full | optional - if set the details on the processing is shown, otherwise only the number is given back | `full` |


The output depends on the setting of the paramter `full`.

#### `full` is omitted 

<img src="./images/server_output.png" width="400">

The output of the server are 3 numbers, separated by a tabulator.

| Number | Meaning | 
| --------- | ------- |
| First number | Full readout, including main digits and subdigits, leading zeros are suppresed |
| Second number | Direct readout of the digital digits, including leading zeros |
| Third number | post digit numbers |

##### Remark
If a digit cannot be recognized, e.g. because it is half between 2 digits, then instead of the number a "N" is written at the corresponding position. In this case a direct conversion to a number will not work. Additional information (e.g. last valid full reading) needs to be used to extrapolate the missing digit.
   
#### `full` is set:

It is not necessary to assign a value to the parameter. If the parameter is detected, then addtionally to the readout value, parts of the image processing, including the corresponding images is attached:

<img src="./images/sever_output_full.png" width="400">



