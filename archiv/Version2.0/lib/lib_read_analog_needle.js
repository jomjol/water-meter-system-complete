require('@tensorflow/tfjs-node')
const tf = require('@tensorflow/tfjs')
const help = require('./lib_read_help')

var keras_model;
var img_zw = './image_tmp/resize_tmp.jpg';

const ReadoutSingleImage = async function(image_name) 
{
    help.ImageResize(image_name, img_zw, 32, 32)
    var pic_tensor = help.load_image_to_tensor(img_zw, 32, 32);
    if (keras_model == undefined)
    {
        keras_model = await tf.loadLayersModel('file://lib/DL_model_analog_needle/model.json');
    }
    var pred = await keras_model.predict(pic_tensor);
    var metric1 = await pred.as1D().dataSync()[0];
    var metric2 = await pred.as1D().dataSync()[1];
    var selector = await pred.as1D().dataSync()[2];
    var result = 0;
    if (selector < 0.5)
      result = metric2 - 0.5;
    else
      result = metric1;
    result = ((result % 1) + 1) % 1;      // positve Modulo
    result = result * 10;
    return result;
}

const Readout = async function(image_names) 
{
    erg = [];
    for (izw = 0; izw < image_names.length; ++izw)
    {
      erg_zw = await ReadoutSingleImage(image_names[izw]);
      erg.push(erg_zw);
    }
    return erg;
}

module.exports = 
{
    Readout
}