# water-meter-system-complete
 
This repository is the sum of different projects to read out an analog water meter with the help of a camera and image processing, including neural network processing to extract the values.
The result is a HTTP-server, that takes an image as input, process it and gives as an output the water meter number, including the subdigits.

The overall system with description of the single steps is described here: [https://github.com/jomjol/water-meter-measurement-system](https://github.com/jomjol/water-meter-measurement-system)

A graphical overview about the steps is shown in the following flow:

<img src="./images/signal_flow.png"> 

The code is implented in node.js. To run it copy the whole [code](code) directory including subdirectory.

Path are relative, so it should run immediatly with the following command:
* `node wasserzaehler.js`

### Remarks
* Node assumes some libraries to be installed using:
	* `opencv4nodejs`
	* `ini`
    * `opencv4nodejs`
    * `@tensorflow/tfjs-node`
    * `@tensorflow/tfjs`
    * `jpeg-js`
    * `http`, `url`
	
	
	
## Running the server

The server is listening to port 3000 and accepts requests in the following syntac:

http://server-ip:3000/?url=http://picture-server/image.jpg&full

| Parameter | Meaning | example |
| --------- | ------- | ------- |
| server-ip | address of the node-server running the script | `localhost` |
| url | url to the picture to be analysed | `url=http://picture-server/image.jpg` |
| full | optional - if set the details on the processing is shown, otherwise only the number is given back | `full` |


The output depends on the setting of the paramter `full`:

### `full` is omitted: 

<img src="./images/server_output.png" width="400">
   
### `full` is set: 

<img src="./images/sever_output_full.png" width="400">



