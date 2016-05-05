var _ = require('underscore');
var cheerio = require('cheerio');
var BASE_URL = 'http://www.saksfifthavenue.com';
var listingsURL = BASE_URL + '/Shoes/shop/_/N-52k0s7';
var userAgent = 'Googlebot/2.1';

/*
 * Saks' List of categories/subcategories and their URLs
 *
 */
var categories = [
  {
    tags: ['Sandals', 'Flats'],
    url: BASE_URL + '/Shoes/Sandals/Flats/shop/_/N-52k0su'
  },
  {
    tags: ['Sandals', 'Heels'],
    url: BASE_URL + '/Shoes/Sandals/Heels/shop/_/N-52k0sv'
  },
  {
    tags: ['Sandals', 'Flats'],
    url: BASE_URL + '/Shoes/Sandals/Flats/shop/_/N-52k0su'
  },
  {
    tags: ['Sandals', 'Wedges'],
    url: BASE_URL + '/Shoes/Sandals/Wedges/shop/_/N-52k0sw'
  },
  {
    tags: ['Sandals', 'Gladiators'],
    url: BASE_URL + '/Shoes/Sandals/Gladiators/shop/_/N-52k3ne'
  },
  {
    tags: ['Sandals', 'Platforms'],
    url: BASE_URL + '/Shoes/Sandals/Platforms/shop/_/N-52k29z'
  },
  {
    tags: ['Pumps and Slingbacks', 'Pumps'],
    url: BASE_URL + '/Shoes/Pumps-and-Slingbacks/Pumps/shop/_/N-52k0sq'
  },
  {
    tags: ['Pumps and Slingbacks', 'Slingbacks'],
    url: BASE_URL + '/Shoes/Pumps-and-Slingbacks/Slingbacks/shop/_/N-52k0ss'
  },
  {
    tags: ['Pumps and Slingbacks', 'Point Toe'],
    url: BASE_URL + '/Shoes/Pumps-and-Slingbacks/Point-Toe/shop/_/N-52k0sr'
  },
  {
    tags: ['Pumps and Slingbacks', 'Peep Toe'],
    url: BASE_URL + '/Shoes/Pumps-and-Slingbacks/Peep-Toe/shop/_/N-52k0sn'
  },
  {
    tags: ['Pumps and Slingbacks', 'Platforms'],
    url: BASE_URL + '/Shoes/Pumps-and-Slingbacks/Platforms/shop/_/N-52k0so'
  },
  {
    tags: ['Flats', 'Ballet Flats'],
    url: BASE_URL + '/Shoes/Flats/Ballet-Flats/shop/_/N-52k29p'
  },
  {
    tags: ['Flats', 'Espadrilles'],
    url: BASE_URL + '/Shoes/Flats/Espadrilles/shop/_/N-52k29q'
  },
  {
    tags: ['Flats', 'Point Toe'],
    url: BASE_URL + '/Shoes/Flats/Point-Toe/shop/_/N-52k29r'
  },
  {
    tags: ['Wedges'],
    url: BASE_URL + '/Shoes/Wedges/shop/_/N-52k0t0'
  },
  {
    tags: ['Espadrilles'],
    url: BASE_URL + '/Shoes/Espadrilles/shop/_/N-52k86d'
  },
  {
    tags: ['Sneakers'],
    url: BASE_URL + '/Shoes/Sneakers/shop/_/N-52k0sy'
  },
  {
    tags: ['Boots', 'Booties'],
    url: BASE_URL + '/Shoes/Boots/Booties/shop/_/N-52k0sb'
  },
  {
    tags: ['Boots', 'Tall'],
    url: BASE_URL + '/Shoes/Boots/Tall/shop/_/N-52k0t1'
  },
  {
    tags: ['Boots', 'Over the Knee'],
    url: BASE_URL + '/Shoes/Boots/Over-the-Knee/shop/_/N-52k0sd'
  },
  {
    tags: ['Boots', 'Cold Weather'],
    url: BASE_URL + '/Shoes/Boots/Cold-Weather/shop/_/N-52k0sc'
  },
  {
    tags: ['Boots', 'Rain Boots'],
    url: BASE_URL + '/Shoes/Boots/Rain-Boots/shop/_/N-52k0se'
  },
  {
    tags: ['Oxfords and Loafers'],
    url: BASE_URL + '/Shoes/Oxfords-and-Loafers/shop/_/N-52k868'
  },
  {
    tags: ['Evening'],
    url: BASE_URL + '/Shoes/Evening/shop/_/N-52k0sg'
  },
  {
    tags: ['Wedding'],
    url: BASE_URL + '/Shoes/Wedding/shop/_/N-52k0sz'
  },
  {
    tags: ['Mules and Slides'],
    url: BASE_URL + '/Shoes/Mules-and-Slides/shop/_/N-52k29y'
  },
  {
    tags: ['Mary Janes'],
    url: BASE_URL + '/Shoes/Mary-Janes/shop/_/N-52kddn'
  },
  {
    tags: ['Exotics'],
    url: BASE_URL + '/Shoes/Exotics/shop/_/N-52k0sh'
  },
  {
    tags: ['Slippers'],
    url: BASE_URL + '/Shoes/Slippers/shop/_/N-52k0sx'
  },
  {
    tags: ['Cold Weather'],
    url: BASE_URL + '/Shoes/Cold-Weather/shop/_/N-52k6sn'
  }
];

/*
 * Saks' Listings class
 *
 */
function Listings(html) {
  this.html = html;
  this.$ = cheerio.load(html);
}

Listings.prototype.getItemURLs = function() {
  var $ = this.$;
  return $('.product-text a.mainBlackText').map(function() {
    return $(this).attr('href');
  }).get();
};

Listings.prototype.getProductIds = function() {
  var $ = this.$;
  return $('.product-text a').map(function() {
    var url = $(this).attr('href');
    return url.match(/prd_id=\d+/)[0].split(/=/)[1];
  }).get();
};

Listings.prototype.getNextPageURL = function() {
  var $ = this.$;
  var nextPage = $('.pa-enh-pagination-right-arrow a').attr('href');
  return nextPage ? (BASE_URL + nextPage) : false;
};

/*
 * Saks' Item class
 *
 */
function Item(html) {
  this.html = html;
  this.$ = cheerio.load(html);
  this.data = setupItem(this.$);
}

var setupItem = function($) {
  var priceHTML = $('.product-pricing__price').last().find('span');

  var data = {
    retailer: 'Saks Fifth Avenue',
    retailerId: 'saks',
    altProductId: $('.product-overview__product-code').html(),
    designer: $('.product-overview__brand-link').html(),
    productName: $('.product-overview__short-description').html(),
    details: $('.product-description ul').html(),
    price: priceHTML.last().html(),
    priceCurrency: priceHTML.first().html(),
    url: $('meta[property="og:url"]').attr('content'),
    images: []
  };

  // HTML structure is different for item with one vs multiple colors
  if ($('.product-color-options').children().length === 1) {
    var singleColor = true;
    data.color = $('.product-color-options__selected-value').html();
  } else {
    var singleColor = false;
    data.color = $('.product-color-options li').first().attr('title');
  }
  data.productId = data.url.split('prd_id=')[1];
  data.images = generateItemImages(
    data.altProductId,
    data.color,
    singleColor
  );

  return data;
};

var generateItemImages = function(productId, color, singleColor) {
  /*
   * Saks' default item page doesn't provide image URLs. Instead, we'll assume
   * that every item has 5 images, and use the known conventions to construct
   * the image URLs for each item.
   *
   */
  var IMAGE_URL = 'http://s7d9.scene7.com/is/image/saks/';

  return _.map(_.range(5), function(i) {
    var suffix = (i > 0) ? '_A' + i : '';
    var cSuffix = (!singleColor && i === 0) ?
      '_' + color.replace(/ /g, "").toUpperCase() : '';
    var image = {
      url: IMAGE_URL + productId + suffix + cSuffix
    };
    if (i === 0) {
      image.primary = true;
    }

    return image;
  });
};

Item.prototype.getOtherColors = function() {
  var $ = this.$;
  var colorsHTML = $('.product-color-options');

  if (colorsHTML.children().length === 1) {
    return false;
  } else {
    var colors = colorsHTML.find('li').map(function(i) {
      if (i > 0) return $(this).attr('title');
    }).get();

    return {
      type: 'text',
      colors: colors
    };
  }
};

// Only needed for retailers whose other colors don't generate a new URL
Item.prototype.changeColor = function(newColor) {
  this.data.color = newColor;
  this.data.images = generateItemImages(this.data.altProductId, newColor);
};

module.exports.categories = categories;
module.exports.Item = Item;
module.exports.Listings = Listings;
module.exports.listingsURL = listingsURL;
module.exports.userAgent = userAgent;