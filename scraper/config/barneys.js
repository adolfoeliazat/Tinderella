var cheerio = require('cheerio');
var listingsURL = 'http://www.barneys.com/barneys-new-york/women/shoes';
var userAgent = 'Python-urllib/3.1';

/*
 * Barneys' Listings class
 *
 */
function Listings(html) {
  this.html = html;
  this.$ = cheerio.load(html);
}

Listings.prototype.getItemURLs = function() {
  var $ = this.$;
  return $('#search-result-items .thumb-link').map(function() {
    return $(this).attr('href');
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
    if ($('a', this).attr('data-index') === '0') {
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

module.exports.listingsURL = listingsURL;
module.exports.userAgent = userAgent;
module.exports.Listings = Listings;
module.exports.Item = Item;
