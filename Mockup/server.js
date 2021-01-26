'use strict';
var http = require('http');
var fs = require('fs');
var port = process.env.PORT || 1337;


http.createServer(function (req, res) {
    fs.readFile('index.html', function (err, html) {
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.write(html);
        res.end();
    });
}).listen(port);