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

var db = mongojs('Tinderella', ['shoes', 'shoe_tags']);
// NOTE: Need to call db.close() in the future to terminate the program
// properly

var IMAGE_PATH = '../data/images/';
var DEFAULT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) ' +
  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 ' +
  'Safari/537.36';

/*
 * checkRetry(options)
 *
 * Re-invoke fetchURL() once if the HTTP request encounters an error.
 */
var checkRetry = function(options, cb) {
  if (!options.stopRetrying) {
    return fetchURL(_.extend(options, { stopRetrying: true }), cb);
  } else {
    console.log("Confirmed error retrieving URL: " + options.url);
    return false;
  }
};

/*
 * fetchURL()
 *
 * Description:
 * Use the request library to fetch the URL and pass the contents to
 * helper functions.
 *
 */
var fetchURL = function(options, cb) {
  var userAgent = options.userAgent || DEFAULT_USER_AGENT;

  var requestOptions = {
    url: options.url,
    headers: {
      'User-Agent': userAgent
    }
  };

  request.get(requestOptions, function(err) {
    if (err) {
      console.log('Request error: ' + err + ' for URL: ' + options.url);
      return checkRetry(options, cb);
    }
  }).on('response', function(res) {
    if (res.statusCode != 200) {
      console.log('Error: ' + res.statusCode + ' for URL: ' + options.url);
      return checkRetry(options, cb);
    }

    var data = '';
    res.setEncoding(options.encoding);
    res.on('data', function(chunk) {
      data += chunk;
    });
    res.on('end', function() {
      cb(data, options);
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
    var fileName = obj.retailerId + '_' + obj.productId;
    if (obj.color) {
      fileName += '_' + obj.color.replace(/ /g, "_").replace(/\//g, "");
    }
    var filePath = IMAGE_PATH + fileName + '.jpg';
    fs.writeFile(filePath, img, 'binary', function(err) {
      if (err) {
        console.log('Error saving image: ' + filePath);
      } else {
        console.log('Image saved successfully: ' + filePath);
      }
    });
  };

  var primaryImage = _.find(obj.images, function(img) {
    return img.primary === true;
  });

  if (!primaryImage) {
    primaryImage = obj.images[0];
  }

  fetchURL({
    url: primaryImage.url,
    encoding: 'binary'
  }, saveImage);
};

/*
 * upsertShoe()
 *
 */
var upsertShoe = function(obj, cb) {
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
      console.log('Error upserting productId '
        + obj.productId
        + ' to shoes: ' + err);
    } else {
      if (!doc) {
        console.log('New entry saved to mongoDB.shoes: ' +
          obj.retailerId + ': ' + obj.productId + ': ' + obj.color
        );

        cb(obj);
      }
    }
  });
};

/*
 * upsertShoeTag()
 *
 */
var upsertShoeTag = function(obj) {
  db.shoe_tags.findAndModify({
    query: {
      retailerId: obj.retailer.id,
      productId: obj.productId
    },
    update: {
      $setOnInsert: {
        retailerId: obj.retailer.id,
        productId: obj.productId
      },
      $addToSet: {
        tags: {
          $each: obj.tags
        }
      }
    },
    new: false,
    upsert: true
  }, function(err, doc) {
    if (err) {
      console.log('Error upserting productId '
        + obj.productId
        + ' to shoe_tags: ' + err);
    } else {
      if (!doc) {
        console.log('New entry saved to mongoDB.shoe_tags: ' +
          obj.retailer.id + ': ' + obj.productId
        );
      }
    }
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
var scrapeItemURLs = function(html, options) {
  var retailer = options.retailer;
  var nextRetailer = options.nextRetailer;
  var page = new retailer.Listings(html, options.url);

  if (!page.url) {
    return checkRetry(options, scrapeItemURLs);
  }

  // Trigger async scrape for all the items
  async.each(
    page.getItemURLs(),
    function(url) {
      fetchURL({
        url: url,
        encoding: 'utf8',
        retailer: retailer
      }, scrapeItem);
    },
    function(err) {
      if (err) {
        console.log("Couldn't fetch item: " + err);
      }
    }
  );

  // Recursively scrape the next page until we've reached the end
  var nextPage = page.getNextPageURL();
  if (nextPage) {
    fetchURL({
      url: nextPage,
      encoding: 'utf8',
      retailer: retailer,
      nextRetailer: nextRetailer
    }, scrapeItemURLs);
  } else {
    console.log('Shoe URL scraping complete for ' + retailer.id);
    nextRetailer();
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
var scrapeItem = function(html, options) {
  var retailer = options.retailer;
  var item = new retailer.Item(html, options.url);
  if (!item.data) {
    return checkRetry(options, scrapeItem);
  }

  // Save or update MongoDB
  upsertShoe(item.data, downloadImage);

  // Fetch the other colors for this item if specified
  var otherColors = item.getOtherColors();
  if (!options.stopScrapingColors && otherColors) {
    switch (otherColors.type) {
      case 'url':
        async.each(
          otherColors,
          function(url) {
            fetchURL({
              url: url,
              encoding: 'utf8',
              retailer: retailer,
              stopScrapingColors: true
            }, scrapeItem);
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
          var newItem = new retailer.Item(item.html, options.url);
          newItem.changeColor(color);
          upsertShoe(newItem.data, downloadImage);
        });
        break;
    }
  }
};

/*
 * scrapeShoes()
 *
 * Kicks off scraping shoe data for a specific retailer.
 *
 */
var scrapeShoes = function(retailer, nextRetailer) {
  fetchURL({
    url: retailer.listingsURL,
    encoding: 'utf8',
    retailer: retailer,
    nextRetailer: nextRetailer
  }, scrapeItemURLs);
};

/*
 * scrapeProductIds()
 *
 * Looks for all the product IDs referenced in a listings page. Used to
 * populate the list of products matching a specific category from a retailer.
 *
 */
var scrapeProductIds = function(html, options) {
  var category = options.category;
  var retailer = options.retailer;
  var page = new retailer.Listings(html, category.url);
  var productIds = page.getProductIds();

  _.each(productIds, function(productId) {
    upsertShoeTag({
      retailer: retailer,
      productId: productId,
      tags: category.tags
    });
  });

  // Recursively scrape the next page until we've reached the end
  var nextPage = page.getNextPageURL();
  if (nextPage) {
    fetchURL({
      url: nextPage,
      encoding: 'utf8',
      retailer: retailer,
      category: category,
      nextRetailer: options.nextRetailer,
      nextCategory: options.nextCategory
    }, scrapeProductIds);
  } else {
    console.log('Shoe tags URL scraping complete for tags ' + category.tags);
    if (category.url === _.last(retailer.categories).url) {
      options.nextRetailer();
    }
    options.nextCategory();
  }
};

/*
 * scrapeTags()
 *
 * Kicks off scraping all the shoes that match all applicable tags.
 */
var scrapeTags = function(retailer, nextRetailer) {
  var categories = retailer.categories;
  var categoryFunctions = _.map(categories, function(category) {
    return (function(nextCategory) {
      fetchURL({
        url: category.url,
        encoding: 'utf8',
        category: category,
        retailer: retailer,
        nextRetailer: nextRetailer,
        nextCategory: nextCategory
      }, scrapeProductIds);
    });
  });

  // Kick off each url's scraping synchronously to manage concurrent threads
  async.series(categoryFunctions);
};

/*
 * startScrape()
 *
 * Launch function, decides which scraper(s) to kick off.
 */
var startScrape = function(retailerId) {
  var retailers;
  if (retailerId && !sources[retailerId]) {
      console.log("Please specify a matching retailer to start scraping.");
      process.exit(1);
  } else {
    if (retailerId) {
      retailers = _.filter(sources, function(source, key) {
        return key === retailerId;
      });
    } else {
      retailers = sources;
    }

    console.log("Starting scrape for: " + _.pluck(retailers, 'id'));
    var generateFunctions = function(op) {
      return _.map(retailers, function(retailer) {
        return (function(cb) { op(retailer, cb); });
      });
    };

    // async.series(generateFunctions(scrapeShoes));
    async.series(generateFunctions(scrapeTags));
  }
};

/*
 * Main routine
 *
 */
var retailerId = process.argv[2];

if (!retailerId) {
  startScrape();
} else {
  startScrape(retailerId);
}
