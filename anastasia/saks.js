var async = require('async');
var cheerio = require('cheerio');

var fetchURL = require('./scraper_tools.js').fetchURL;
var upsert = require('./scraper_tools.js').upsert;

var SAKS = 'Saks Fifth Avenue';
var SAKS_BASE_URL = '';
var parsedCount = 0;
var scrapedCount = 0;
var parseComplete = false;
