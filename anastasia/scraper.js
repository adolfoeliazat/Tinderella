var _ = require('underscore');
var async = require('async');

var Barneys = require('./barneys.js');
var Nordstrom = require('./nordstrom.js');
var Saks = require('./saks.js');

// 1. Overall scraper module that requires the individual modules and runs all the scrapers
// in parallel (and can also run specific scrapers only, if passed an array).

async.parallel(
    [
        //Barneys.scrapeShoes()
        Nordstrom.scrapeShoes()
        //Saks.scrapeShoes()
    ],
    function(err) {
        console.log("All scraping complete");
    }
);
