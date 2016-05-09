var cheerio = require('cheerio');
var BASE_URL = require('./urls.js').BARNEYS_BASE_URL;
var userAgent = 'Python-urllib/3.1';

/*
 * Barneys' Listings class
 *
 */
function Listings(html, url) {
  this.html = html;
  this.$ = cheerio.load(html);
  this.url = url || BASE_URL;
}

Listings.prototype.getItemURLs = function() {
  var $ = this.$;
  return $('#search-result-items .thumb-link').map(function() {
    return $(this).attr('href');
  }).get();
};

Listings.prototype.getProductIds = function() {
  var $ = this.$;
  return $('.product-tile').map(function() {
    return $(this).attr('data-itemid');
  }).get();
};

Listings.prototype.getNextPageURL = function() {
  var $ = this.$;
  var nextPage = $('.pagination .page-next.active').attr('href');
  return nextPage ? nextPage : false;
};

/*
 * Barneys' Item class
 *
 */
function Item(html) {
  this.html = html;
  this.$ = cheerio.load(html);
  this.data = setupItem(this.$);
}

var setupItem = function($) {
  var data = {
    retailer: 'Barneys New York',
    retailerId: 'barneys',
    productId: $('meta[property="product:retailer_part_no"]').attr('content'),
    designer: $('meta[property="product:brand"]').attr('content'),
    productName: $('#product-content .product-name').html(),
    color: '',
    url: $('meta[property="og:url"]').attr('content'),
    price: $('meta[property="product:price:amount"]').attr('content'),
    priceCurrency: $('meta[property="product:price:currency"]')
      .attr('content'),
    images: []
  };

  var details = $('#collapseOne .panel-body.standard-p').html();
  data.details = details ? details.trim() : null;

  $('#product-image-carousel .item').each(function() {
    var image = { url: $('img', this).attr('src') };

    if (image.url.match(/shoefrontqtr/i)) {
      image.primary = true;
    }

    data.images.push(image);
  });

  return data;
};

Item.prototype.getOtherColors = function() {
  // Barneys uses a separate product ID for each color
  return false;
};

module.exports.Item = Item;
module.exports.Listings = Listings;
module.exports.listingsURL = BASE_URL;
module.exports.userAgent = userAgent;
