var _ = require('underscore');
var async = require('async');

var Barneys = require('./barneys.js');
var Nordstrom = require('./nordstrom.js');
var Saks = require('./saks.js');

/*
 * Overall scraper module that requires the individual modules and runs all
 * the scrapers in parallel (and can also run specific scrapers only.
 */

if (process.argv[2]) {
    switch (process.argv[2]) {
        case 'barneys':
            Barneys.scrapeShoes();
            break;

        case 'nordstrom':
            Nordstrom.scrapeShoes();
            break;

        case 'saks':
            Saks.scrapeShoes();
            break;
    }
} else {
    async.parallel(
        [
            Barneys.scrapeShoes(),
            Nordstrom.scrapeShoes(),
            Saks.scrapeShoes()
        ],
        function(err) {
            console.log("All scraping complete");
        }
    );
}
