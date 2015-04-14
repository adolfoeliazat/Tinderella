var _ = require('underscore'),
    async = require('async'),
    cheerio = require('cheerio'),
    express = require('express'),
    http = require('http'),
    mongojs = require('mongojs'),
    request = require('request');

var BARNEYS = 'Barneys New York';
var BARNEYS_BASE_URL = 'http://www.barneys.com/barneys-new-york/women/shoes';
var TINDERELLA_DB = 'Tinderella';

var db = mongojs(TINDERELLA_DB, ['shoes']);
var parsedCount = 0, scrapedCount = 0;
var parseComplete = false;

/*
 * scrapeItemURLs()
 *
 * Description:
 * Given the HTML contents of a list results page, find all the URLs that correspond to
 * individual Barneys product items. Trigger individual scrapes for each set of product
 * items scraped.
 *
 */
var scrapeBarneysItemURLs = function(html) {
    $ = cheerio.load(html);
    var items = $('#search-result-items .thumb-link').map(function() {
        return $(this).attr('href');
    }).get();
    parsedCount += items.length;

    // Trigger async scrape for all the items
    async.each(items, fetchItem, function(err) {
        console.log("Couldn't fetch item: " + err);
    });

    // Recursively scrape the next page of item URLs until we've reached the end
    var nextPage = $('.pagination .page-next.active').attr('href');
    if (nextPage) {
        fetchItemURLs(nextPage);
    } else {
        console.log("URL scraping complete: " + parsedCount + " shoe URLs scraped");
        parseComplete = true;
    }
};

/*
 * scrapeBarneysItem()
 *
 * Description:
 * Given the HTML contents of a Barneys product detail page, scrape the relevant contents
 * of the product and save the entry into MongoDB.
 *
 */
var scrapeBarneysItem = function(html) {
    $ = cheerio.load(html);

    var barneysItem = {
        retailer: BARNEYS,
        productId: $('meta[property="og:isbn"]').attr('content'),
        designer: $('#product-content .brand a').html(),
        productName: $('#product-content .product-name').html(),
        url: $('meta[property="og:url"]').attr('content'),
        price: $('meta[property="product:price:amount"]').attr('content'),
        priceCurrency: $('meta[property="product:price:currency"]').attr('content')
    };
    var details = $('#collapseOne .panel-body.standard-p').html();
    barneysItem.details = details ? details.trim() : '';

    barneysItem.images = [];
    $('#product-image-carousel .item').each(function() {
        var image = {
            url: $('.shoe', this).attr('src')
        };
        if ($('a', this).attr('data-index') === '0') {
            image.primary = true;
        }
        barneysItem.images.push(image);
    });

    // Upsert into mongoDB
    db.shoes.update(
        {
            retailer: barneysItem.retailer,
            productId: barneysItem.productId
        },
        barneysItem,
        { upsert: true },
        function(err, doc) {
            console.log('Saved to mongoDB: ' + barneysItem.productId);
        }
    );

    scrapedCount++;
    if (parseComplete && scrapedCount === parsedCount) {
        console.log('All done');
        process.exit(0);
    }
};

/*
 * fetchURL()
 *
 * Description:
 * Use the request library to fetch the URL and pass the HTML contents to
 * helper functions.
 *
 */
var fetchURL = function(url, cb) {
    request.get(url).on('response', function(res) {
        var data = '';
        res.setEncoding('utf8');
        res.on('data', function(chunk) {
            data += chunk;
        });
        res.on('end', function() {
            cb(data);
        });
    });
};

/* Helpers for fetchURL()
 */
var fetchItem = function(url) {
    fetchURL(url, scrapeBarneysItem);
};
var fetchItemURLs = function(url) {
    fetchURL(url, scrapeBarneysItemURLs);
};

fetchItemURLs(BARNEYS_BASE_URL);

