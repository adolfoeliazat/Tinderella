var _ = require('underscore');
var async = require('async');
var cheerio = require('cheerio');

var fetchURL = require('./scraper_tools.js').fetchURL;
var upsert = require('./scraper_tools.js').upsert;

var BASE_URL = 'http://shop.nordstrom.com/c/womens-shoes';
var BASE_ITEM_URL = 'http://shop.nordstrom.com';
var BASE_IMG_URL = 'http://g.nordstromimage.com/imagegallery/store/product/';

var parsedCount = 0;
var scrapedCount = 0;
var parseComplete = false;

/*
 * scrapeItemURLs()
 *
 * Description:
 * Given the HTML contents of a list results page, find all the URLs that correspond to
 * individual product items. Trigger individual scrapes for each set of product
 * items scraped.
 *
 */
var scrapeItemURLs = function(html) {
    $ = cheerio.load(html);
    var itemURLs = $('.fashion-results .fashion-item .title').map(function() {
        return BASE_ITEM_URL + $(this).attr('href');
    }).get();
    parsedCount += itemURLs.length;

    var fetchItem = function(url) {
        fetchURL(url, scrapeItem);
    };

    // Trigger async scrape for all the items
    async.each(itemURLs, fetchItem, function(err) {
        console.log("Couldn't fetch item: " + err);
    });

    // Recursively scrape the next page of item URLs until we've reached the end
    var nextPage = BASE_URL + $('.product-results-pagination .page-next a').attr('href');
    if (nextPage) {
        fetchURL(nextPage, scrapeItemURLs);
    } else {
        console.log("URL scraping complete: " + parsedCount + " Nordstrom shoe URLs scraped");
        parseComplete = true;
    }
};

/*
 * scrapeItem()
 *
 * Description:
 * Given the HTML contents of a product detail page, scrape the relevant contents
 * of the product and save the entry into MongoDB. Save a new entry for each color
 * available for a shoe.
 *
 */
var scrapeItem = function(html) {
    $ = cheerio.load(html);

    var item = {
        retailer: 'Nordstrom',
        productId: $('#right-column .item-price-rows').attr('data-item-number'),
        designer: $('#right-column #brand-title a').html(),
        productName: $('#right-column #product-title h1').html(),
        url: $('meta[property="og:url"]').attr('content'),
        priceCurrency: 'USD'
    };

    var currPrice = $('#right-column .item-price span').html();
    var salePrice = $('#right-column .item-price span.sale-price').html();
    if (salePrice) {
        item.price = salePrice.match(/\d+.\d+/);
    } else if (currPrice) {
        item.price = currPrice.match(/\d+.\d+/)
    } else {
        item.price = '';
    }

    var details = $('#right-column #details-and-care .accordion-content').html();
    item.details = details ? details.trim() : '';

    var upsertItemWithColor = function(itemParams) {
        var newItem = _.clone(item);
        _.extend(newItem, itemParams);
        upsert(newItem);

        scrapedCount++;
        if (parseComplete && scrapedCount === parsedCount) {
            console.log('All done');
            process.exit(0);
        }
    };

    // Save a new MongoDB entry for each color available for the shoe
    var itemColors = $('#color-swatch li').map(function() {
        var colorImages = [];
        colorImages.push({ url: BASE_IMG_URL + $(this).attr('data-img-filename'), primary: true });
        colorImages.push({ url: BASE_IMG_URL + $(this).attr('data-img-gigantic-filename') });

        return {
            color: $(this).attr('title'),
            images: colorImages
        };
    }).get();

    parsedCount += itemColors.length - 1; // Don't double-count the initial item
    async.each(itemColors, upsertItemWithColor, function(err) {
        console.log("Couldn't upsert item with color: " + err);
    });
};

var scrapeShoes = function() {
    fetchURL(BASE_URL, scrapeItemURLs);
};
module.exports.scrapeShoes = scrapeShoes;
