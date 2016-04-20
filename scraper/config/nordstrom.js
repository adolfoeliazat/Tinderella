var cheerio = require('cheerio');
var listingsURL = 'http://shop.nordstrom.com/c/womens-shoes';

/*
 * Nordstrom's Listings class
 *
 */
function Listings(html) {
  this.$ = cheerio.load(html);
}

Listings.prototype.getItemURLs = function() {
  var $ = this.$;
  return $('.nui-product-module .product-photo-href').map(function() {
    return $(this).attr('href');
  }).get();
};

Listings.prototype.getNextPageURL = function() {
  var $ = this.$;
  var nextPage = $('.page-arrow.page-next a').attr('href');
  return nextPage ? (listingsURL + nextPage) : false;
};

/*
 * Nordstrom's Item class
 *
 */
function Item(html) {
  this.$ = cheerio.load(html);
  this.data = setupItem(this.$);
}

var setupItem = function($) {
  var data = {
    retailer: 'Nordstrom',
    productId: $('.product-details .style-number').html().match(/\d+/)[0],
    designer: $('.product-details .brand-title span').html(),
    productName: $('.product-details .product-title h1').html(),
    color: $('.immersive-color-filter-color-name').html(),
    priceCurrency: 'USD'
  };

  data.url = $('meta[property="og:url"]').attr('content') +
    '?fashioncolor=' +
    encodeURIComponent(data.color);

  var fullPrice = $('.price-display-item.regular-price').html();
  var discount = $('.price-display-item .price-current').html();
  data.price= (discount ? discount : fullPrice).match(/\d+.\d+/)[0];

  var details = $('.product-details-and-care p').html();
  data.details = details ? details.trim() : null;

  data.images = [];
  $('.thumbnails li').each(function() {
    var image = {
        url: $('img', this).attr('src').split('?')[0]
    };

    if ($(this).hasClass('selected')) {
        image.primary = true;
    }

    data.images.push(image);
  });

  return data;
};

Item.prototype.getOtherColorURLs = function() {
  var $ = this.$;
  var that = this;
  var otherColorURLs = [];
  $('.color-select option').each(function() {
    var color = $(this).html();
    if (color !== 'Select a color' && color !== that.data.color) {
      otherColorURLs.push(
        that.data.url.split('?')[0] + '?fashioncolor=' + color
      );
    }
  });

  return otherColorURLs;
};

module.exports.listingsURL = listingsURL;
module.exports.Listings = Listings;
module.exports.Item = Item;
