require('request');
const http = require('http');
const url = require('url');
const zaehlerstand = require("./lib/lib_gesamt");
const fs = require('fs');

var abfrage = function(req, res) {
    var q = url.parse(req.url, true).query;
    var save_cut_zeiger = false;
    var save_cut_ziffer = false;
    var simple = true;
    var filename = q.url;

    if (filename)
    {
        console.log(filename);

        if(typeof(q.full) !== "undefined"){
            simple = false;
        }

        if(typeof(q.save_cut_zeiger) !== "undefined"){
            save_cut_zeiger = true;
        }

        if(typeof(q.save_cut_ziffer) !== "undefined"){
            save_cut_ziffer = true;
        }

        var file = fs.createWriteStream("./image_tmp/aktuell.jpg");
        var request = http.get(filename, (response) => {
            response.pipe(file);
            response.on('end', () => {
                console.log("File fertig");
                file.end();   

                zaehlerstand.getZaehlerstand('./image_tmp/aktuell.jpg', save_cut_zeiger, save_cut_ziffer, simple).then(result => {
                        console.log('Zählerstand: ');
                        console.log(result);
                        res.writeHead(200, {'Content-Type': 'text/html'});
                        res.end(result);})
            });
        });
    }

    if (req.url.indexOf('/image_tmp/') !== -1)
    {
        var s = fs.createReadStream("." + req.url);
        s.on('open', function () {
            res.setHeader('Content-Type', 'image/jpeg');
            s.pipe(res);
        });
    }
}


zaehlerstand.init();

http.createServer(abfrage).listen(3000);