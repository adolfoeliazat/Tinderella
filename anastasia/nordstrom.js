var async = require('async');
var cheerio = require('cheerio');

var fetchURL = require('./scraper_tools.js').fetchURL;
var upsert = require('./scraper_tools.js').upsert;

var NORDSTROM = 'Nordstrom';
var NORDSTROM_BASE_URL = 'http://shop.nordstrom.com/c/womens-shoes';
var parsedCount = 0;
var scrapedCount = 0;
var parseComplete = false;
