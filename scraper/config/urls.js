var NORDSTROM_BASE_URL = 'http://shop.nordstrom.com';
var SAKS_BASE_URL = 'http://www.saksfifthavenue.com';

/*
 * Nordstrom's list of categories/subcategories and their URLs
 *
 */
var nordstrom = [
  {
    tags: ['Sandals', 'Ankle Strap'],
    url: NORDSTROM_BASE_URL + '/c/shoes-ankle-straps'
  },
  {
    tags: ['Sandals', 'Block Heel'],
    url: NORDSTROM_BASE_URL + '/c/womens-block-heel-sandals'
  },
  {
    tags: ['Sandals', 'Cage'],
    url: NORDSTROM_BASE_URL + '/c/cage-sandals'
  }
];

/*
 * Saks' List of categories/subcategories and their URLs
 *
 */
var saks = [
  {
    tags: ['Sandals', 'Flats'],
    url: SAKS_BASE_URL + '/Shoes/Sandals/Flats/shop/_/N-52k0su'
  },
  {
    tags: ['Sandals', 'Heels'],
    url: SAKS_BASE_URL + '/Shoes/Sandals/Heels/shop/_/N-52k0sv'
  },
  {
    tags: ['Sandals', 'Flats'],
    url: SAKS_BASE_URL + '/Shoes/Sandals/Flats/shop/_/N-52k0su'
  },
  {
    tags: ['Sandals', 'Wedges'],
    url: SAKS_BASE_URL + '/Shoes/Sandals/Wedges/shop/_/N-52k0sw'
  },
  {
    tags: ['Sandals', 'Gladiators'],
    url: SAKS_BASE_URL + '/Shoes/Sandals/Gladiators/shop/_/N-52k3ne'
  },
  {
    tags: ['Sandals', 'Platforms'],
    url: SAKS_BASE_URL + '/Shoes/Sandals/Platforms/shop/_/N-52k29z'
  },
  {
    tags: ['Pumps and Slingbacks', 'Pumps'],
    url: SAKS_BASE_URL + '/Shoes/Pumps-and-Slingbacks/Pumps/shop/_/N-52k0sq'
  },
  {
    tags: ['Pumps and Slingbacks', 'Slingbacks'],
    url: SAKS_BASE_URL
      + '/Shoes/Pumps-and-Slingbacks/Slingbacks/shop/_/N-52k0ss'
  },
  {
    tags: ['Pumps and Slingbacks', 'Point Toe'],
    url: SAKS_BASE_URL
      + '/Shoes/Pumps-and-Slingbacks/Point-Toe/shop/_/N-52k0sr'
  },
  {
    tags: ['Pumps and Slingbacks', 'Peep Toe'],
    url: SAKS_BASE_URL + '/Shoes/Pumps-and-Slingbacks/Peep-Toe/shop/_/N-52k0sn'
  },
  {
    tags: ['Pumps and Slingbacks', 'Platforms'],
    url: SAKS_BASE_URL
      + '/Shoes/Pumps-and-Slingbacks/Platforms/shop/_/N-52k0so'
  },
  {
    tags: ['Flats', 'Ballet Flats'],
    url: SAKS_BASE_URL + '/Shoes/Flats/Ballet-Flats/shop/_/N-52k29p'
  },
  {
    tags: ['Flats', 'Espadrilles'],
    url: SAKS_BASE_URL + '/Shoes/Flats/Espadrilles/shop/_/N-52k29q'
  },
  {
    tags: ['Flats', 'Point Toe'],
    url: SAKS_BASE_URL + '/Shoes/Flats/Point-Toe/shop/_/N-52k29r'
  },
  {
    tags: ['Wedges'],
    url: SAKS_BASE_URL + '/Shoes/Wedges/shop/_/N-52k0t0'
  },
  {
    tags: ['Espadrilles'],
    url: SAKS_BASE_URL + '/Shoes/Espadrilles/shop/_/N-52k86d'
  },
  {
    tags: ['Sneakers'],
    url: SAKS_BASE_URL + '/Shoes/Sneakers/shop/_/N-52k0sy'
  },
  {
    tags: ['Boots', 'Booties'],
    url: SAKS_BASE_URL + '/Shoes/Boots/Booties/shop/_/N-52k0sb'
  },
  {
    tags: ['Boots', 'Tall'],
    url: SAKS_BASE_URL + '/Shoes/Boots/Tall/shop/_/N-52k0t1'
  },
  {
    tags: ['Boots', 'Over the Knee'],
    url: SAKS_BASE_URL + '/Shoes/Boots/Over-the-Knee/shop/_/N-52k0sd'
  },
  {
    tags: ['Boots', 'Cold Weather'],
    url: SAKS_BASE_URL + '/Shoes/Boots/Cold-Weather/shop/_/N-52k0sc'
  },
  {
    tags: ['Boots', 'Rain Boots'],
    url: SAKS_BASE_URL + '/Shoes/Boots/Rain-Boots/shop/_/N-52k0se'
  },
  {
    tags: ['Oxfords and Loafers'],
    url: SAKS_BASE_URL + '/Shoes/Oxfords-and-Loafers/shop/_/N-52k868'
  },
  {
    tags: ['Evening'],
    url: SAKS_BASE_URL + '/Shoes/Evening/shop/_/N-52k0sg'
  },
  {
    tags: ['Wedding'],
    url: SAKS_BASE_URL + '/Shoes/Wedding/shop/_/N-52k0sz'
  },
  {
    tags: ['Mules and Slides'],
    url: SAKS_BASE_URL + '/Shoes/Mules-and-Slides/shop/_/N-52k29y'
  },
  {
    tags: ['Mary Janes'],
    url: SAKS_BASE_URL + '/Shoes/Mary-Janes/shop/_/N-52kddn'
  },
  {
    tags: ['Exotics'],
    url: SAKS_BASE_URL + '/Shoes/Exotics/shop/_/N-52k0sh'
  },
  {
    tags: ['Slippers'],
    url: SAKS_BASE_URL + '/Shoes/Slippers/shop/_/N-52k0sx'
  },
  {
    tags: ['Cold Weather'],
    url: SAKS_BASE_URL + '/Shoes/Cold-Weather/shop/_/N-52k6sn'
  }
];

module.exports.nordstrom = nordstrom;
module.exports.saks = saks;
module.exports.NORDSTROM_BASE_URL = NORDSTROM_BASE_URL;
module.exports.SAKS_BASE_URL = SAKS_BASE_URL;
