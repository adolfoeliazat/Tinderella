var _ = require('underscore');
var async = require('async');
var cheerio = require('cheerio');

var fetchURL = require('./scraper_tools.js').fetchURL;
var upsert = require('./scraper_tools.js').upsert;

var BASE_URL = 'http://www.barneys.com/barneys-new-york/women/shoes';
var BARNEYS_UA = 'Python-urllib/3.1';
var parsedCount = 0;
var scrapedCount = 0;
var parseComplete = false;

/*
 * scrapeItemURLs()
 *
 * Description:
 * Given the HTML contents of a list results page, find all the URLs that
 * correspond to individual product items. Trigger individual scrapes for
 * each set of product items scraped.
 *
 */
var scrapeItemURLs = function(html) {
    $ = cheerio.load(html);
    var itemURLs = $('#search-result-items .thumb-link').map(function() {
        return $(this).attr('href');
    }).get();
    parsedCount += itemURLs.length;

    var fetchItem = function(url) {
        fetchURL(url, scrapeItem, BARNEYS_UA);
    };

    // Trigger async scrape for all the items
    async.each(itemURLs, fetchItem, function(err) {
        console.log("Couldn't fetch item: " + err);
        scrapedCount++;
    });

    // Recursively scrape the next page of items until we've reached the end
    var nextPage = $('.pagination .page-next.active').attr('href');
    if (nextPage) {
        fetchURL(nextPage, scrapeItemURLs, BARNEYS_UA);
    } else {
        console.log('URL scraping complete: ' +
            parsedCount +
            ' Barneys shoe URLs scraped'
        );
        parseComplete = true;
    }
};

/*
 * scrapeItem()
 *
 * Description:
 * Given the HTML contents of a product detail page, scrape the relevant
 * contents of the product and save the entry into MongoDB.
 *
 */
var scrapeItem = function(html) {
    $ = cheerio.load(html);

    var item = {
        retailer: 'Barneys New York',
        productId: $('meta[property="product:retailer_part_no"]')
            .attr('content'),
        designer: $('meta[property="product:brand"]').attr('content'),
        productName: $('#product-content .product-name').html(),
        url: $('meta[property="og:url"]').attr('content'),
        price: $('meta[property="product:price:amount"]').attr('content'),
        priceCurrency: $('meta[property="product:price:currency"]')
            .attr('content')
    };

    var details = $('#collapseOne .panel-body.standard-p').html();
    item.details = details ? details.trim() : '';

    item.images = [];
    $('#product-image-carousel .item').each(function() {
        var image = {
            url: $('img', this).attr('src')
        };
        if ($('a', this).attr('data-index') === '0') {
            image.primary = true;
        }
        item.images.push(image);
    });

    upsert(item);
    scrapedCount++;
    if (parseComplete && scrapedCount === parsedCount) {
        console.log('Barneys - All done');
        process.exit(0);
    }
};

var scrapeShoes = function() {
    fetchURL(BASE_URL, scrapeItemURLs, BARNEYS_UA);
};
module.exports.scrapeShoes = scrapeShoes;
