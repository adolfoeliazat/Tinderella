var _ = require('underscore');
var async = require('async');
var fs = require('fs');
var mongojs = require('mongojs');
var request = require('request');

var sources = {
  barneys: require('./config/barneys.js'),
  nordstrom: require('./config/nordstrom.js'),
  saks: require('./config/saks.js')
};

var IMAGE_PATH = '../data/images/';
var DEFAULT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) ' +
  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 ' +
  'Safari/537.36';

/*
 * fetchURL()
 *
 * Description:
 * Use the request library to fetch the URL and pass the contents to
 * helper functions.
 *
 */
var fetchURL = function(url, encoding, cb, retailer, userAgent) {
  userAgent = userAgent || DEFAULT_USER_AGENT;

  var options = {
    url: url,
    headers: {
      'User-Agent': userAgent
    }
  };

  request.get(options, function(err) {
    if (err) {
      console.log('Request error: ' + err + ' for URL: ' + url);
    }
  }).on('response', function(res) {
    debugger;
    if (res.statusCode != 200) {
      console.log('Error: ' + res.statusCode + ' for URL: ' + url);
      return false;
    }

    var data = '';
    res.setEncoding(encoding);
    res.on('data', function(chunk) {
      data += chunk;
    });
    res.on('end', function() {
      cb(data, retailer);
    });
  });
};

/*
 * downloadImage(obj)
 *
 * Description:
 * Given a shoe object, fetch the primary image and save it to disk.
 *
 */
var downloadImage = function(obj) {
  var saveImage = function(img) {
    var fileName = obj.retailerId + '_' +
      obj.productId + '_' + obj.color.replace(" ", "_") + '.jpg';
    var filePath = IMAGE_PATH + fileName;
    fs.writeFile(filePath, img, 'binary', function(err) {
      if (err) {
        console.log('Error saving image: ' + filePath);
      } else {
        console.log('Image saved successfully: ' + filePath);
      }
    });
  };

  var imageURL = _.find(obj.images, function(img) {
    return img.primary === true;
  }).url;

  fetchURL(imageURL, 'binary', saveImage);
};

/*
 * upsertAndDownload()
 *
 * Description:
 * Upserts the object into the shoes collection, given a unique combination
 * of retailer, product ID, and item color.
 *
 * Download the primary image only if the record is upserted.
 *
 */
var upsertAndDownload = function(obj) {
  var db = mongojs('Tinderella', ['shoes']);

  db.shoes.findAndModify({
    query: {
      retailerId: obj.retailerId,
      productId: obj.productId,
      color: obj.color
    },
    update: {
      $setOnInsert: obj
    },
    new: false,
    upsert: true
  }, function(err, doc) {
    if (err) {
      console.log('Error upserting: ' + err);
    } else {
      if (!doc) {
        console.log('New entry saved to mongoDB: ' +
          obj.retailer + ': ' + obj.productId + ': ' + obj.color
        );

        downloadImage(obj);
      }
    }

    db.close();
  });
};

/*
 * scrapeItemURLs()
 *
 * Given the HTML contents of a list results page, find all the URLs that
 * correspond to individual product items. Trigger individual scrapes for
 * each set of product items scraped.
 *
 */
var scrapeItemURLs = function(html, retailer) {
  var page = new sources[retailer].Listings(html);
  var userAgent = sources[retailer].userAgent;

  // Trigger async scrape for all the items
  async.each(
    page.getItemURLs(),
    function(url) { fetchURL(url, 'utf8', scrapeItem, retailer, userAgent); },
    function(err) {
      if (err) {
        console.log("Couldn't fetch item: " + err);
      }
    }
  );

  // Recursively scrape the next page until we've reached the end
  var nextPage = page.getNextPageURL();
  if (nextPage) {
    fetchURL(nextPage, 'utf8', scrapeItemURLs, retailer, userAgent);
  } else {
    console.log('URL scraping complete');
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
var scrapeItem = function(html, retailer, stopScrapingColors) {
  var item = new sources[retailer].Item(html);
  var userAgent = sources[retailer].userAgent;

  // Save or update MongoDB
  upsertAndDownload(item.data);

  // Fetch the other colors for this item if specified
  var otherColors = item.getOtherColors();
  if (!stopScrapingColors && otherColors) {
    switch (otherColors.type) {
      case 'url':
        async.each(
          otherColors,
          function(url) {
            fetchURL(url, 'utf8', scrapeOneColorItem, retailer, userAgent);
          },
          function(err) {
            if (err) {
              console.log("Couldn't fetch item: " + err);
            }
          }
        );
        break;

      case 'text':
        _.each(otherColors.colors, function(color) {
          var newItem = new sources[retailer].Item(item.html);
          newItem.changeColor(color);
          upsertAndDownload(newItem.data);
        });
        break;
    }
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
var scrapeOneColorItem = function(html, retailer) {
  scrapeItem(html, retailer, true);
};

/*
 * scrapeShoes()
 *
 * Kicks off scraping for a specific retailer.
 *
 */
var scrapeShoes = function(retailer) {
  var url = sources[retailer].listingsURL;
  var userAgent = sources[retailer].userAgent;
  fetchURL(url, 'utf8', scrapeItemURLs, retailer, userAgent);
};

/*
 * Main routine
 *
 */
var retailer = process.argv[2];
if (retailer) {
  switch (retailer) {
    case 'barneys':
    case 'nordstrom':
    case 'saks':
      console.log("Starting scraping for " + retailer + '...');
      scrapeShoes(retailer);
      break;
  }
} else {
  console.log("Starting scraping for all retailers...");
  async.each(
    Object.keys(sources),
    function(retailer) { scrapeShoes(retailer); },
    function(err) {
      if (err) {
        console.log('Error scraping sources: ' + err);
      } else {
        console.log('All scraping complete.');
      }
    }
  );
}
