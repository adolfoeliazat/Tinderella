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

var urls = require('./config/urls.js');
var db = mongojs('Tinderella', ['shoes', 'shoe_tags']);
// NOTE: Need to call db.close() in the future to terminate the program
// properly

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
var fetchURL = function(url, encoding, cb, retailerId, userAgent) {
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
      return false;
    }
  }).on('response', function(res) {
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
      cb(data, retailerId);
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

  fetchURL(primaryImage.url, 'binary', saveImage);
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
      console.log('Error upserting to shoes: ' + err);
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
      retailerId: obj.retailerId,
      productId: obj.productId
    },
    update: {
      $setOnInsert: {
        retailerId: obj.retailerId,
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
      console.log('Error upserting to shoe_tags: ' + err);
    } else {
      if (!doc) {
        console.log('New entry saved to mongoDB.shoe_tags: ' +
          obj.retailerId + ': ' + obj.productId
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
var scrapeItemURLs = function(html, retailerId) {
  var page = new sources[retailerId].Listings(html);
  var userAgent = sources[retailerId].userAgent;

  // Trigger async scrape for all the items
  async.each(
    page.getItemURLs(),
    function(url) {
      fetchURL(url, 'utf8', scrapeItem, retailerId, userAgent);
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
    fetchURL(nextPage, 'utf8', scrapeItemURLs, retailerId, userAgent);
  } else {
    console.log('Shoe URL scraping complete');
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
var scrapeItem = function(html, retailerId, stopScrapingColors) {
  var item = new sources[retailerId].Item(html);
  var userAgent = sources[retailerId].userAgent;

  // Save or update MongoDB
  upsertShoe(item.data, downloadImage);

  // Fetch the other colors for this item if specified
  var otherColors = item.getOtherColors();
  if (!stopScrapingColors && otherColors) {
    switch (otherColors.type) {
      case 'url':
        async.each(
          otherColors,
          function(url) {
            fetchURL(url, 'utf8', scrapeOneColorItem, retailerId, userAgent);
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
          var newItem = new sources[retailerId].Item(item.html);
          newItem.changeColor(color);
          upsertShoe(newItem.data, downloadImage);
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
var scrapeOneColorItem = function(html, retailerId) {
  scrapeItem(html, retailerId, true);
};

/*
 * scrapeShoes()
 *
 * Kicks off scraping shoe data for a specific retailer.
 *
 */
var scrapeShoes = function(retailerId) {
  var url = sources[retailerId].listingsURL;
  var userAgent = sources[retailerId].userAgent;
  fetchURL(url, 'utf8', scrapeItemURLs, retailerId, userAgent);
};

/*
 * scrapeProductIds()
 *
 * Looks for all the product IDs referenced in a listings page. Used to
 * populate the list of products matching a specific category from a retailer.
 *
 */
var scrapeProductIds = function(html, retailerId, tags) {
  var page = new sources[retailerId].Listings(html);
  var userAgent = sources[retailerId].userAgent;
  var productIds = page.getProductIds();

  _.each(productIds, function(productId) {
    var obj = {
      retailerId: retailerId,
      productId: productId,
      tags: tags
    };

    upsertShoeTag(obj);
  });

  // Recursively scrape the next page until we've reached the end
  var nextPage = page.getNextPageURL();
  if (nextPage) {
    var wrapper = function(html, retailerId) {
      scrapeProductIds(html, retailerId, tags);
    };

    fetchURL(nextPage, 'utf8', wrapper, retailerId, userAgent);
  } else {
    console.log('Shoe tags URL scraping complete for tags ' + tags);
  }
};

/*
 * scrapeTags()
 *
 * Kicks off scraping all the shoes that match all applicable tags.
 *
 */
var scrapeTags = function(retailerId) {
  var categories = urls[retailerId];
  var userAgent = sources[retailerId].userAgent;

  // Kick off each url's scraping synchronously to manage concurrent threads
  async.each(
    categories,
    function(category) {
      var wrapper = function(html, retailerId) {
        scrapeProductIds(html, retailerId, category.tags);
      };

      fetchURL(category.url, 'utf8', wrapper, retailerId, userAgent);
    },
    function(err) {
      if (err) {
        console.log('Error scraping product IDs: ' + err);
      } else {
        console.log('Finished scraping product IDs');
      }
    }
  );
};

/*
 * Main routine
 *
 */
var retailerId = process.argv[2];
if (retailerId) {
  switch (retailerId) {
    case 'barneys':
    case 'nordstrom':
    case 'saks':
      console.log("Starting scraping for " + retailerId + '...');
      scrapeShoes(retailerId);
      scrapeTags(retailerId);
      break;
  }
} else {
  console.log("Starting scraping for all retailers...");
  async.each(
    Object.keys(sources),
    function(retailerId) {
      scrapeShoes(retailerId);
      scrapeTags(retailerId);
    },
    function(err) {
      if (err) {
        console.log('Error scraping sources: ' + err);
      } else {
        console.log('All scraping complete.');
      }
    }
  );
}
