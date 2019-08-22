const cv_lib = require('opencv4nodejs');
const os = require("os");
const ini = require("ini")
const fs = require('fs')

var alignment_rotation_angle;

var reference_image0;
var reference_image1;
var reference_image2;
var reference_p0;
var reference_p1;
var reference_p2;

var Analog_Counter;
var Analog_Counter_Pos  = [];

var Digital_Digit;
var Digital_Digit_Pos = [];


function init()
{
    var config = ini.parse(fs.readFileSync('./config.ini', 'utf-8'));

    var rf = "initial_rotation_angle";

    var test = config['alignment'][rf];

    alignment_rotation_angle = parseFloat(config.alignment.initial_rotation_angle);

    reference_image0 = config.alignment.ref0.image;
    reference_p0 = new cv_lib.Point2(config.alignment.ref0.pos_x, config.alignment.ref0.pos_y)

    reference_image1 = config.alignment.ref1.image;
    reference_p1 = new cv_lib.Point2(config.alignment.ref1.pos_x, config.alignment.ref1.pos_y)

    reference_image2 = config.alignment.ref2.image;
    reference_p2 = new cv_lib.Point2(config.alignment.ref2.pos_x, config.alignment.ref2.pos_y)

    Analog_Counter = config.Analog_Counter.name;
    for (var i = 0; i < Analog_Counter.length; ++i)
    {
        x1 = parseInt(config['Analog_Counter'][Analog_Counter[i]]['pos_x']);
        y1 = parseInt(config['Analog_Counter'][Analog_Counter[i]]['pos_y']);
        dx = parseInt(config['Analog_Counter'][Analog_Counter[i]]['dx']);
        dy = parseInt(config['Analog_Counter'][Analog_Counter[i]]['dy']);
        p_neu = new cv_lib.Rect(x1, y1, dx, dy);
        Analog_Counter_Pos.push(p_neu);
    }

    Digital_Digit = config.Digital_Digit.name;
    for (var i = 0; i < Digital_Digit.length; ++i)
    {
        x1 = parseInt(config['Digital_Digit'][Digital_Digit[i]]['pos_x']);
        y1 = parseInt(config['Digital_Digit'][Digital_Digit[i]]['pos_y']);
        dx = parseInt(config['Digital_Digit'][Digital_Digit[i]]['dx']);
        dy = parseInt(config['Digital_Digit'][Digital_Digit[i]]['dy']);
        p_neu = new cv_lib.Rect(x1, y1, dx, dy);
        Digital_Digit_Pos.push(p_neu);
    }
}

function Alignment(source)
{
    const ref0 = cv_lib.imread(reference_image0);
    const ref1 = cv_lib.imread(reference_image1);
    const ref2 = cv_lib.imread(reference_image2);

    const p1 = getRefKoordinaten_lib(source, ref0);
    const p2 = getRefKoordinaten_lib(source, ref1);
    const p3 = getRefKoordinaten_lib(source, ref2);

    target = calcImageCorrect(source, p1, p2, p3);

    return target;
}

function cutImage(img_file, save_cut_zeiger, save_cut_ziffer, name)
{
    var source = cv_lib.imread(img_file);

    cv_lib.imwrite('./image_tmp/org.jpg', source);
    target = rotateImage(source, alignment_rotation_angle);
    cv_lib.imwrite('./image_tmp/rot.jpg', source);
    target = Alignment(target);
    cv_lib.imwrite('./image_tmp/alg.jpg', target);

    var zeiger = [];
    zeiger = cutZeiger(target);

    var ziffern = [];
    ziffern = cutZiffern(target);

    if (save_cut_zeiger == true)
    {
        for (i = 0; i < Digital_Digit.length; ++i)
        {
            var name_dest = name + '/' + Analog_Counter[i] + '.jpg';
            fs.copyFile(zeiger[i], name_dest, (err) => {
              if (err) throw err;
            });        
        }
    }

    if (save_cut_ziffer == true)
    {
        for (i = 0; i < Digital_Digit.length; ++i)
        {
            var name_dest = name + '/' + Digital_Digit[i] + '.jpg';
            fs.copyFile(ziffern[i], name_dest, (err) => {
              if (err) throw err;
            });        
        }
    }

    return [zeiger, ziffern]
}

function cutZeiger(source)
{
    var target;
    var name_zeiger = []
    for (i = 0; i < Analog_Counter.length; ++i)
    {
        target = source.getRegion(Analog_Counter_Pos[i]);
        name_zeiger[i] = './image_tmp/' + Analog_Counter[i] + '.jpg'
        cv_lib.imwrite(name_zeiger[i], target);
    }

    return name_zeiger;
}


function cutZiffern(source)
{
    var target;
    var name = []
    for (i = 0; i < Digital_Digit.length; ++i)
    {
        target = source.getRegion(Digital_Digit_Pos[i]);
        name[i] = './image_tmp/' + Digital_Digit[i] + '.jpg'
        cv_lib.imwrite(name[i], target);
    }

    return name;
}

function getRefKoordinaten_lib(src, ref)
{
  const matched = src.matchTemplate(ref, 5);
  const minMax = matched.minMaxLoc();
  const { maxLoc: { x, y } } = minMax;

  return [x, y];
}

function rotateImage(source, winkel)
{
    dsize = new cv_lib.Size(source.cols, source.rows);
    center = new cv_lib.Point(source.cols / 2, source.rows / 2);
    M = cv_lib.getRotationMatrix2D(center, winkel, 1);
    var target = source.warpAffine(M, dsize, cv_lib.BORDER_CONSTANT);

    return target;
}

function calcImageCorrect(source, p1, p2, p3)
{
    var PtrIst = [new cv_lib.Point(p1[0], p1[1]), new cv_lib.Point(p2[0], p2[1]), new cv_lib.Point(p3[0], p3[1])];
    var PtrTarget = [reference_p0, reference_p1, reference_p2];

    var M = cv_lib.getAffineTransform(PtrIst, PtrTarget);
    var dsize =  new cv_lib.Size(source.cols, source.rows);
 
    var target = source.warpAffine(M, dsize, cv_lib.BORDER_CONSTANT);
    
    return target;
}

module.exports = 
{
    cutImage,
    init
}