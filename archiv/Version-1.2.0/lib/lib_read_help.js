const jpeg = require('jpeg-js');
const opencv = require('opencv4nodejs');
const fs = require('fs');
const tf = require('@tensorflow/tfjs')

function ImageResize(input, output, dx, dy)
{
    var im = opencv.imread(input).resize(dx, dy);
    opencv.imwrite(output, im);
}

function load_image_to_tensor(image_name, dx, dy)
{
    var jpegData = fs.readFileSync(image_name);
    var rawImageData = jpeg.decode(jpegData);
    var rawImOhneAlpha = [];
    fLen = rawImageData.data.length;
    for (i = 0; i < fLen; i++) {
      if (((i+1) % 4) != 0)
      {
        rawImOhneAlpha.push(rawImageData.data[i]);
      }
    }
    var image_tensor = tf.tensor(rawImOhneAlpha, [1, dx, dy, 3])
    return image_tensor;
}

module.exports = 
{
    ImageResize,
    load_image_to_tensor
}