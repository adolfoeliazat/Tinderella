var _ = require('underscore');
var async = require('async');
var cheerio = require('cheerio');
var fetchURL = require('./scraper_tools.js').fetchURL;
var upsert = require('./scraper_tools.js').upsert;

var BASE_URL = 'http://shop.nordstrom.com/c/womens-shoes';
var BASE_IMG_URL = 'http://g.nordstromimage.com/imagegallery/store/product/';
var parsedCount = 0;
var scrapedCount = 0;
var parseComplete = false;

/*
 * scrapeItemURLs()
 *
 * Given the HTML contents of a list results page, find all the URLs that
 * correspond to individual product items. Trigger individual scrapes for
 * each set of product items scraped.
 *
 */
var scrapeItemURLs = function(html) {
    $ = cheerio.load(html);
    var itemURLs = $('.nui-product-module .product-photo-href').map(
        function() {
            return $(this).attr('href');
        }
    ).get();
    parsedCount += itemURLs.length;

    var fetchItem = function(url) {
        fetchURL(url, scrapeItem);
    };

    // Trigger async scrape for all the items
    async.each(itemURLs, fetchItem, function(err) {
        console.log("Couldn't fetch item: " + err);
        scrapedCount++;
    });

    // Recursively scrape the next page until we've reached the end
    var nextPage = BASE_URL + $('.page-arrow.page-next a').attr('href');
    if (nextPage) {
        fetchURL(nextPage, scrapeItemURLs);
    } else {
        console.log("URL scraping complete: " +
            parsedCount +
            " Nordstrom shoe URLs scraped"
        );
        parseComplete = true;
    }
};

/*
 * scrapeItem()
 *
 * Given the HTML contents of a product detail page, scrape the relevant
 * contents of the product and save the entry into MongoDB. Save a new entry
 * for each color available for a shoe.
 *
 */
var scrapeItem = function(html, stopScrapingColors) {
    stopScrapingColors = stopScrapingColors || false;
    $ = cheerio.load(html);

    var item = {
        retailer: 'Nordstrom',
        productId: $('.product-details .style-number').html().match(/\d+/)[0],
        designer: $('.product-details .brand-title span').html(),
        productName: $('.product-details .product-title h1').html(),
        color: $('.immersive-color-filter-color-name').html(),
        priceCurrency: 'USD'
    };
    item.url = $('meta[property="og:url"]').attr('content') +
        '?fashioncolor=' + encodeURIComponent(item.color);

    // Fetch the other colors for this item if specified
    if (!stopScrapingColors) {
        var otherColorURLs = [];
        $('.color-select option').each(function() {
            var color = $(this).html();
            if (color !== 'Select a color' && color !== item.color) {
                var colorURL = item.url.split('?')[0] +
                    '?fashioncolor=' + color;
                otherColorURLs.push(colorURL);
            }
        });
        parsedCount += otherColorURLs.length;

        var fetchItemOnly = function(url) {
            fetchURL(url, scrapeOneColorItem);
        };

        async.each(otherColorURLs, fetchItemOnly, function(err) {
            console.log("Couldn't fetch item: " + err);
            scrapedCount++;
        });
    }

    var currPrice = $('.price-display-item.regular-price').html();
    var salePrice = $('.price-display-item .price-current').html();
    if (salePrice) {
        item.price = salePrice.match(/\d+.\d+/)[0];
    } else if (currPrice) {
        item.price = currPrice.match(/\d+.\d+/)[0];
    } else {
        item.price = '';
    }

    var details = $('.product-details-and-care p').html();
    item.details = details ? details.trim() : '';

    item.images = [];
    $('.thumbnails li').each(function() {
        var image = {
            url: $('img', this).attr('src').split('?')[0]
        };

        if ($(this).hasClass('selected')) {
            image.primary = true;
        }

        item.images.push(image);
    });

    upsert(item);
    scrapedCount++;
    if (parseComplete && scrapedCount === parsedCount) {
        console.log('Nordstrom - All done');
        process.exit(0);
    }
};

/*
 * scrapeOneColorItem()
 *
 * Helper function that passes an additional parameter to scrapeItem, telling
 * it not to scrape the other colors for that item, to avoid infinite
 * recursion.
 *
 */
var scrapeOneColorItem = function(html) {
    scrapeItem(html, true);
};

var scrapeShoes = function() {
    fetchURL(BASE_URL, scrapeItemURLs);
};
module.exports.scrapeShoes = scrapeShoes;
