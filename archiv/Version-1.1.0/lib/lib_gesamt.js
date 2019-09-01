const cv = require('opencv4nodejs');
const image_cut = require('./lib_image_cut.js');
const readCounter = require("./lib_read_digital_counter");
const readNeedle = require("./lib_read_analog_needle")

///////////////////////////////////////////////////////////////////////////////////////
//////// Help Functions ///////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////

function ZeigerEval(zahl, ziffer_vorgaenger)
{
    ergebnis_nachkomma = Math.floor((zahl * 10) % 10);
    ergebnis_vorkomma = Math.floor(zahl % 10);

    if (ziffer_vorgaenger == -1)
        ergebnis = ergebnis_vorkomma;
    else
    {
        ergebnis_rating = ergebnis_nachkomma - ziffer_vorgaenger;
        if (ergebnis_nachkomma >= 5)
            ergebnis_rating-=5;
        else
            ergebnis_rating+=5;
        ergebnis = Math.round(zahl);
        if (ergebnis_rating < 0)
            ergebnis-=1;
        if (ergebnis == -1)
            ergebnis+=10;
    }
    ergebnis = ergebnis  % 10;
    return ergebnis;
}

function AnalogReadoutToValue(ziffern)
{
    prev = -1;
    erg = "";

    for (i_cnt = ziffern.length - 1; i_cnt >= 0; --i_cnt)
    {
        zif = ZeigerEval(ziffern[i_cnt], prev);
        prev = zif;
        erg = zif + erg;
    }

    return erg;
}

function DigitalReadoutToValue(ziffern)
{
  erg = "";
  zif = "";

  for (i_cnt = 0; i_cnt < ziffern.length; ++i_cnt)
  {
      if (ziffern[i_cnt] == "NaN")  ziffern[i_cnt] = "N"
      erg += ziffern[i_cnt];
  }

  return erg;
}
///////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////


const getZaehlerstand = async function(img_file, save_cut_zeiger, save_cut_ziffer, simple = true)
{
    var nachkomma;
    var ziffern = [];
    var txt = "";

    var jetzt = new Date();
    name = jetzt.toISOString();
    
    cut_images = image_cut.cutImage(img_file, save_cut_zeiger, save_cut_ziffer, name);        //nur Zerlegen

    zeiger = await readNeedle.Readout(cut_images[0]);
    nachkomma = AnalogReadoutToValue(zeiger);

    ziffern = await readCounter.Readout(cut_images[1]);
    vorkomma = DigitalReadoutToValue(ziffern);

    zaehlerstand = vorkomma + '.' + nachkomma;
    zaehlerstand = zaehlerstand.replace(/^0+/, '');

    txt = zaehlerstand + '\t' + vorkomma  + '\t' + nachkomma; 

    if (!simple)
    {
        txt += '<p>Aligned Image: <p><img src=/image_tmp/alg.jpg></img><p>';
        txt += 'Digital Counter: <p>'
        for (i = 0; i < cut_images[1].length; ++i)
        {
            name_zw = cut_images[1][i].substring(1, cut_images[1][i].length);
            txt += '<img src='+  name_zw + '></img>' + ziffern[i];
        }
        txt += '<p>';
        txt += 'Analog Meter: <p>'
        for (i = 0; i < cut_images[0].length; ++i)
        {
            name_zw = cut_images[0][i].substring(1, cut_images[0][i].length);
            txt += '<img src='+  name_zw + '></img>' + zeiger[i].toPrecision(2);
        }
        txt += '<p>';
    }

    return txt;
}

function init()
{
    image_cut.init();
}

module.exports = 
{
    getZaehlerstand,
    init
}