var _ = require('underscore'),
    cheerio = require('cheerio'),
    express = require('express'),
    http = require('http'),
    mongojs = require('mongojs'),
    request = require('request');

var BARNEYS_BASE_URL = 'http://www.barneys.com/barneys-new-york/women/shoes';
var barneysItems = [];

var scrapeURL = function(url) {
    console.log('Scraping ' + url);
    request.get(url).on('response', function(res) {
        var data = '';
        res.setEncoding('utf8');
        res.on('data', function(chunk) {
            data += chunk;
        });
        res.on('end', function() {
            getBarneysItems(data);
        });
    });
};

var getBarneysItems = function(html) {
    $ = cheerio.load(html);
    $('#search-result-items .thumb-link').each(function() {
        var currentItem = $(this).attr('href');
        //console.log('Adding item ' + currentItem);
        barneysItems.push(currentItem);
    });

    // Recursively scrape the next page until we've reached the end
    var nextPage = $('.pagination .page-next.active').attr('href');
    if (!nextPage) {
        console.log("Total of " + barneysItems.length + " shoes scraped");

        // TO-DO: Scrape the individual items and save into MongoDB
        process.exit(0);
    } else {
        scrapeURL(nextPage);
    }
};

var startScrape = function() {
    scrapeURL(BARNEYS_BASE_URL);
};

startScrape();
