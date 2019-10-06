# Description of the Config.ini

The config.ini file contains the information for the alignment and ROIs to process the image. It consists of 3 main segments, which are described in the following sections:

* `[Imagesource]`
* `[ConsistencyCheck]`
* `[alignment]`
* `[Analog_Counter]`
* `[Digital_Counter]`


A draft for a step-by-step instruction to extract the picture parameters can be found here: [Alignment_procedure_draft.pdf](/images/Alignment_procedure_draft.pdf)
			
## Imagesource
#### Main section [Imagesource]
The parameter `url=` in the server request can be omitted, if in the Imagesource sector a fixed source is defined. In this case an image is directly loaded from the source an processed accordingly


| Parameter        | Meaning           | Example        |
| ------------- | ------------- | ------------- |
| URLImageSource | Link to the jpg-source | `URLImageSource=http://192.168.178.20/capture_with_light` |
| TimeoutLoadImage | Maximum waiting time for image source response - otherwise error is issued | `TimeoutLoadImage=30` |
| LogImageLocation | optional - if set, the source images will be logged in the given folder | `LogImageLocation=./log/source_image` |
| LogOnlyFalsePictures | optional - if enabled, only false picture will be stored to avoid large amounts of pictures | `LogOnlyFalsePictures=True` |

## ConsistencyCheck
#### Main section [ConsistencyCheck]
Here a consistency check of the readout value with respect to the previous full read value can be configured. Prequisite is, that the previous value is stored and has no non readable digits ("N"). This can be achieved by using setPreValue to store the first value and the parameter &usePreValue to constantly remove the "N" in case of unambigous digits.

| Parameter        | Meaning           | Example        |
| ------------- | ------------- | ------------- |
| Enabled | Diable or Enable the Check | `Enabled=True` |
| AllowNegativeRates | If set to `False`, then only increasing counter values are accepted | `AllowNegativeRates=False` |
| MaxRateValue | Maximum absolute change from the previous value (+/-) | `MaxRateValue=0.1` |
| ErrorReturn | Return value, in case of unconsistent values | `ErrorReturn=OldValue, ErrorMessage, Readout` |

Options for ErrorReturn are the following:
* `OldValue` = giving back the old value and ignore the "false" readout
* `NewValue` = notify about unconstent value, but still accept it and give it back as readout
* `ErrorMessage` = attach to value a reason for the inconistent value (max rate or negative)
* `Readout` = attach the original readout - usefull, if the OldValue is given back to see, what the readout really was



## Alignment

#### Main section [aligment]
In the main sections the parameter for the rotation is stored:

| Parameter        | Meaning           | Example        |
| ------------- | ------------- | ------------- |
| initial_rotation_angle | Fixed rotation angle for prealigment | `initial_rotation_angle=0` |

#### Sub section for reference [alignment.ref0],[alignment.ref1], [alignment.ref2]

Here the details for the fine alignment references are stored. There need to be 3 subsections ([alignment.ref0], [alignment.ref1], [alignment.ref2]) to ensure the affine transformation:

| Parameter        | Meaning           | Example        |
| ------------- | ------------- | ------------- |
| image | link and name of reference picture | `image=./reference/Ref_ZR.jpg` |
| pos_x | x target coordinate (upper left corner) | `pos_x=70` |
| pos_y | y target coordinate (upper left corner) | `pos_y=203` |


## Definition of ROIs
The ROIs are defined in two steps:
1. name - main section
2. details on position - sub section

For further processing there are two types of ROIs distinguished: 

* Analog_Counter: ROIs for analog counters
* Digital_Digit: ROIs for digital digits for OCR

The syntax of the parameters is identically for both categories.

#### Main sectin ROIs [Digital_Digit], [Analog_Counter]

Here a list of the ROIs is defined. The number is not limited. For each ROI a line with 'name[]' needs to be added. Don't forget the bracket [] also for only one single ROI.

| Parameter        | Meaning           | Example        |
| ------------- | ------------- | ------------- |
| names | naming of the ROIs and references to sub section | `name=ziffer1, ziffer2, ziffer3` |
| Modelfile | path to the Modelfile for the neural network | `Modelfile=./config/neuralnets/Train_CNN_Digital-Readout_Version2.h5` |
| LogImageLocation | path to storage of detected images for debugging / data collection. If this is empty, no logging will happen | `LogImageLocation=./log/digital_digit` |
| LogNames | name of dedicated ROIs to be stored. If this is disabled, all ROIs will be logged (if enabled) | `LogNames=zeiger3, zeiger4` |


#### Sub section of individual ROIs [Digital_Digits.name], [Analog_Counter.name]

The naming of the sub section depends on the ROI naming defined in the main section. For every ROI "xyz" defined in the main section there needs to be either a corresponding sub section (e.g. [Digital_Digits.xyz] with the following content:

| Parameter        | Meaning           | Example        |
| ------------- | ------------- | ------------- |
| pos_x | x coordinate ROI (upper left corner) | `pos_x=546` |
| pos_y | y coordinate ROI (upper left corner) | `pos_y=303` |
| dx | x lenght of the ROI | `dx=142` |
| dy | y length of the ROI | `dy=142` |


# Remark

**Currently there is no error handling implemented in the processing of the code. Therefore a carefull review of the ini file is substantial!**

## Example

~~~~
[Imagesource]
TimeoutLoadImage=30
#IP durch die IP des ESP32 ersetzen!
URLImageSource=http://IP-ESP32-CAM/capture_with_flashlight
LogImageLocation=./log/source_image
# Falls nur schlechte / fehlerhafte Bilder gelockt werden sollen, naechste Zeile Kommentar entfernen
#LogOnlyFalsePictures=True

[ConsistencyCheck]
Enabled=True
AllowNegativeRates=False
#Maximum Change of new to old value (+ or -)
MaxRateValue=0.1

#Return in Case of Error: Value = OldValue or NewValue
#                         ErrorMessage = Return Text with problem (seperated by Tabstopp) if nothing, then no error message
#                         Readout = Real Readout without corrections (NewValue)
ErrorReturn=OldValue, ErrorMessage, Readout
#ErrorReturn=OldValue, ErrorMessage
#ErrorReturn=NewValue, ErrorMessage


[alignment]
initial_rotation_angle=180

[alignment.ref0]
image=./config/Ref_ZR_x99_y219.jpg
pos_x=99
pos_y=219

[alignment.ref1]
image=./config/Ref_m3_x512_y117.jpg
pos_x=512
pos_y=117

[alignment.ref2]
image=./config/Ref_x0_x301_y386.jpg
pos_x=301
pos_y=386

[Digital_Digit]
names=ziffer1, ziffer2, ziffer3, ziffer4, ziffer5
Modelfile=./config/neuralnets/Train_CNN_Digital-Readout_Version2.h5
LogImageLocation=./log/digital_digit
#LogNames=zeiger3, zeiger4

[Analog_Counter]
names=zeiger1, zeiger2, zeiger3, zeiger4
Modelfile=./config/neuralnets/CNN_Analog-Readout_Version-2.1.1.h5
LogImageLocation=./log/analog_counter
#LogNames=zeiger3, zeiger4

[Analog_Counter.zeiger1]
pos_x=491
pos_y=307
dx=115
dy=115

[Analog_Counter.zeiger2]
pos_x=417
pos_y=395
dx=115
dy=115

[Analog_Counter.zeiger3]
pos_x=303
pos_y=424
dx=115
dy=115

[Analog_Counter.zeiger4]
pos_x=163
pos_y=358
dx=115
dy=115

    
[Digital_Digit.ziffer1]
pos_x=215
pos_y=97
dx=42
dy=75

[Digital_Digit.ziffer2]
pos_x=273
pos_y=97
dx=42
dy=75

[Digital_Digit.ziffer3]
pos_x=332
pos_y=97
dx=42
dy=75

[Digital_Digit.ziffer4]
pos_x=390
pos_y=97
dx=42
dy=75

[Digital_Digit.ziffer5]
pos_x=446
pos_y=97
dx=42
dy=75

~~~~

