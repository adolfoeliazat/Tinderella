var _ = require('underscore'),
    cheerio = require('cheerio'),
    express = require('express'),
    http = require('http'),
    mongojs = require('mongojs');

var BARNEYS_OPTS = {
    host: 'www.barneys.com',
    method: 'GET',
    path: '/barneys-new-york/women/shoes/'
};

var req = http.get(BARNEYS_OPTS, function(res) {
    res.setEncoding('utf8');
    res.on('data', function(chunk) {
        console.log('BODYPART: ' + chunk);
    });

    res.on('end', function() {
        console.log('everything crawled');
    });
});

req.on('error', function(error) {
    console.log('Got error: ' + error.message);
});

