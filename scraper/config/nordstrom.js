var _ = require('underscore');
var cheerio = require('cheerio');
var BASE_URL = require('./urls.js').NORDSTROM_BASE_URL;
var categories = require('./urls.js').nordstrom;
var listingsURL = BASE_URL + '/c/womens-shoes';

/*
 * Nordstrom's Listings class
 *
 */
function Listings(html, url) {
  this.html = html;
  this.$ = cheerio.load(html);
  this.url = url || listingsURL;

  // Nordstrom's product listings data is stored within the React javascript
  // code embedded within the webpage.
  this.products = JSON.parse(
    html.split('"Products":')[1].split(',"SortOptions":')[0]
  );
}

Listings.prototype.getItemURLs = function() {
  return _.pluck(this.products, 'ProductPageUrl');
};

Listings.prototype.getProductIds = function() {
  return _.map(_.pluck(this.products, 'Id'), function(id) {
    return '' + id;
  });
};

Listings.prototype.getNextPageURL = function() {
  var $ = this.$;
  var nextPage = $('.page-arrow.page-next a').attr('href');
  return nextPage ? (this.url + nextPage) : false;
};

/*
 * Nordstrom's Item class
 *
 */
function Item(html) {
  this.html = html;
  this.$ = cheerio.load(html);

  // Nordstrom's product data is stored within the React javascript code
  // embedded within the webpage.
  this.rawData = JSON.parse(
    html.split('"StyleModel":')[1].split(',"AnalyticModel":')[0]
  );
  this.data = setupItem(this.$, this.rawData);
}

var setupItem = function($, rawData) {
  var data = {
    retailer: 'Nordstrom',
    retailerId: 'nordstrom',
    productId: '' + rawData.Id,
    altProductId: $('.product-details .style-number').html().match(/\d+/)[0],
    designer: rawData.Brand.Name,
    productName: rawData.Name,
    priceCurrency: rawData.CurrencyCode,
    images: []
  };

  var currentColor = $('.immersive-color-filter-color-name').html();
  if (currentColor) {
    data.color = currentColor;
  } else {
    data.color = rawData.DefaultColor;
  }

  data.url = $('meta[property="og:url"]').attr('content') +
    '?fashioncolor=' +
    encodeURIComponent(data.color);

  var fullPrice = $('.price-display-item.regular-price').html();
  var discount = $('.price-display-item .price-current').html();
  data.price= (discount ? discount : fullPrice).match(/\d+.\d+/)[0];

  var details = rawData.Description;
  data.details = details ? details.trim() : null;

  _.each(rawData.StyleMedia, function(media) {
    if (media.ColorName === data.color) {
      var image = {
        url: media.ImageMediaUri.Gigantic
      };

      if (media.MediaGroupType === 'Main') {
        image.primary = true;
      }

      data.images.push(image);
    }
  });

  return data;
};

Item.prototype.getOtherColors = function() {
  var $ = this.$;
  var that = this;
  var urls = [];
  $('.color-select option').each(function() {
    var color = $(this).html();
    if (color !== 'Select a color' && color !== that.data.color) {
      urls.push(
        that.data.url.split('?')[0] + '?fashioncolor=' + color
      );
    }
  });

  return {
    type: 'url',
    colors: urls
  };
};

module.exports.id = 'nordstrom';
module.exports.categories = categories;
module.exports.Item = Item;
module.exports.Listings = Listings;
module.exports.listingsURL = listingsURL;
