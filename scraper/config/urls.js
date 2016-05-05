var BARNEYS_BASE_URL = 'http://www.barneys.com/barneys-new-york/women/shoes';
var NORDSTROM_BASE_URL = 'http://shop.nordstrom.com';
var SAKS_BASE_URL = 'http://www.saksfifthavenue.com';

/*
 * Barneys New York's list of categories/subcategories and their URLs
 *
 */
var barneys = [
  {
    tags: ['Boots', 'Ankle Boots'],
    url: BARNEYS_BASE_URL + '/boots/ankle-boots'
  },
  {
    tags: ['Boots', 'Knee Boots'],
    url: BARNEYS_BASE_URL + '/boots/knee-boots'
  },
  {
    tags: ['Boots', 'Over the Knee Boots'],
    url: BARNEYS_BASE_URL + '/boots/over-the-knee-boots'
  },
  {
    tags: ['Espadrilles'],
    url: BARNEYS_BASE_URL + '/espadrilles'
  },
  {
    tags: ['Evening'],
    url: BARNEYS_BASE_URL + '/evening'
  },
  {
    tags: ['Flats', 'Ballet Flats'],
    url: BARNEYS_BASE_URL + '/flats/ballet-flats'
  },
  {
    tags: ['Flats', 'Lace-Ups'],
    url: BARNEYS_BASE_URL + '/flats/lace-ups'
  },
  {
    tags: ['Flats', 'Loafers'],
    url: BARNEYS_BASE_URL + '/flats/loafers'
  },
  {
    tags: ['Flats', 'Sandals'],
    url: BARNEYS_BASE_URL + '/flats/sandals'
  },
  {
    tags: ['Heels', 'Mary-Janes'],
    url: BARNEYS_BASE_URL + '/heels/mary-jane'
  },
  {
    tags: ['Heels', 'Peep-Toe'],
    url: BARNEYS_BASE_URL + '/heels/peeptoe'
  },
  {
    tags: ['Heels', 'Pumps'],
    url: BARNEYS_BASE_URL + '/heels/pump'
  },
  {
    tags: ['Heels', 'Sandals'],
    url: BARNEYS_BASE_URL + '/heels/sandals'
  },
  {
    tags: ['Heels', 'Slingbacks'],
    url: BARNEYS_BASE_URL + '/heels/slingback'
  },
  {
    tags: ['Platforms'],
    url: BARNEYS_BASE_URL + '/platforms'
  },
  {
    tags: ['Sandals', 'Flats'],
    url: BARNEYS_BASE_URL + '/sandals/flats'
  },
  {
    tags: ['Sneakers'],
    url: BARNEYS_BASE_URL + '/sneakers'
  },
  {
    tags: ['Wedges'],
    url: BARNEYS_BASE_URL + '/wedges'
  }
];

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
    tags: ['Sandals', 'Block Heels'],
    url: NORDSTROM_BASE_URL + '/c/womens-block-heel-sandals'
  },
  {
    tags: ['Sandals', 'Cage'],
    url: NORDSTROM_BASE_URL + '/c/cage-sandals'
  },
  {
    tags: ['Sandals', 'Comfort'],
    url: NORDSTROM_BASE_URL + '/c/comfort-sandals-for-women'
  },
  {
    tags: ['Sandals', 'Espadrilles'],
    url: NORDSTROM_BASE_URL + '/c/womens-espadrille-sandals'
  },
  {
    tags: ['Sandals', 'Flats'],
    url: NORDSTROM_BASE_URL + '/c/womens-flat-sandals'
  },
  {
    tags: ['Sandals', 'Flip-Flops'],
    url: NORDSTROM_BASE_URL + '/c/womens-flip-flop-sandals'
  },
  {
    tags: ['Sandals', 'Footbed'],
    url: NORDSTROM_BASE_URL + '/c/womens-footbed-sandals'
  },
  {
    tags: ['Sandals', 'Gladiators'],
    url: NORDSTROM_BASE_URL + '/c/gladiator-sandals'
  },
  {
    tags: ['Sandals', 'Lace-Ups'],
    url: NORDSTROM_BASE_URL + '/c/womens-lace-up-sandals'
  },
  {
    tags: ['Sandals', 'Mules'],
    url: NORDSTROM_BASE_URL + '/c/womens-mule-sandals'
  },
  {
    tags: ['Sandals', 'Party & Evening'],
    url: NORDSTROM_BASE_URL + '/c/party-evening-sandals'
  },
  {
    tags: ['Sandals', 'Platforms'],
    url: NORDSTROM_BASE_URL + '/c/womens-platform-sandals'
  },
  {
    tags: ['Sandals', 'Slides'],
    url: NORDSTROM_BASE_URL + '/c/womens-slide-sandals'
  },
  {
    tags: ['Sandals', 'Sport'],
    url: NORDSTROM_BASE_URL + '/c/sport-sandals'
  },
  {
    tags: ['Sandals', 'T-Strap'],
    url: NORDSTROM_BASE_URL + '/c/womens-tstrap-sandals'
  },
  {
    tags: ['Sandals', 'Wedges'],
    url: NORDSTROM_BASE_URL + '/c/womens-wedge-sandals'
  },
  {
    tags: ['Sandals', 'Wooden Sole'],
    url: NORDSTROM_BASE_URL + '/c/wooden-sole-sandals'
  },
  {
    tags: ['Flats', 'Ballet'],
    url: NORDSTROM_BASE_URL + '/c/womens-ballet-flats'
  },
  {
    tags: ['Flats', 'Comfort'],
    url: NORDSTROM_BASE_URL + '/c/comfort-shoes-for-women'
  },
  {
    tags: ['Flats', 'Espadrilles'],
    url: NORDSTROM_BASE_URL + '/c/womens-espadrille-flats'
  },
  {
    tags: ['Flats', 'Lace-Ups'],
    url: NORDSTROM_BASE_URL + '/c/womens-lace-up-flats'
  },
  {
    tags: ['Flats', 'Loafers & Moccasins'],
    url: NORDSTROM_BASE_URL + '/c/womens-flat-loafer-moccasin'
  },
  {
    tags: ['Flats', 'Oxfords'],
    url: NORDSTROM_BASE_URL + '/c/womens-flat-oxfords'
  },
  {
    tags: ['Flats', 'Party & Evening'],
    url: NORDSTROM_BASE_URL + '/c/party-evening-flats'
  },
  {
    tags: ['Flats', 'Pointed Toe'],
    url: NORDSTROM_BASE_URL + '/c/womens-pointed-toe-flats'
  },
  {
    tags: ['Flats', 'Slip-On'],
    url: NORDSTROM_BASE_URL + '/c/womens-slip-ons'
  },
  {
    tags: ['Heels', 'Pumps'],
    url: NORDSTROM_BASE_URL + '/c/womens-pumps-heels'
  },
  {
    tags: ['Heels', 'Sandals'],
    url: NORDSTROM_BASE_URL + '/c/womens-sandals-heels'
  },
  {
    tags: ['Heels', 'Ankle Strap'],
    url: NORDSTROM_BASE_URL + '/c/womens-ankle-strap-heels'
  },
  {
    tags: ['Heels', 'Block Heels'],
    url: NORDSTROM_BASE_URL + '/c/womens-block-heels'
  },
  {
    tags: ['Heels', 'Cage'],
    url: NORDSTROM_BASE_URL + '/c/womens-cage-heels'
  },
  {
    tags: ['Heels', 'Comfort'],
    url: NORDSTROM_BASE_URL + '/c/comfort-heels'
  },
  {
    tags: ['Heels', "D'Orsay"],
    url: NORDSTROM_BASE_URL + '/c/womens-dorsay-heels'
  },
  {
    tags: ['Heels', 'Kitten Heels'],
    url: NORDSTROM_BASE_URL + '/c/womens-kitten-heels'
  },
  {
    tags: ['Heels', 'Lace-Ups'],
    url: NORDSTROM_BASE_URL + '/c/lace-up-heels'
  },
  {
    tags: ['Heels', 'Mary Jane'],
    url: NORDSTROM_BASE_URL + '/c/womens-mary-jane-heels'
  },
  {
    tags: ['Heels', 'Party & Evening'],
    url: NORDSTROM_BASE_URL + '/c/party-evening-heels'
  },
  {
    tags: ['Heels', 'Peep Toe'],
    url: NORDSTROM_BASE_URL + '/c/womens-peep-toe-heels'
  },
  {
    tags: ['Heels', 'Platforms'],
    url: NORDSTROM_BASE_URL + '/c/womens-platform-heels'
  },
  {
    tags: ['Heels', 'Pointed Toe'],
    url: NORDSTROM_BASE_URL + '/c/womens-pointed-toe-heels'
  },
  {
    tags: ['Heels', 'Slingbacks'],
    url: NORDSTROM_BASE_URL + '/c/womens-slingback-heels'
  },
  {
    tags: ['Heels', 'Strappy'],
    url: NORDSTROM_BASE_URL + '/c/womens-strappy-heels'
  },
  {
    tags: ['Heels', 'T-Strap'],
    url: NORDSTROM_BASE_URL + '/c/womens-tstrap-heels'
  },
  {
    tags: ['Sneakers', 'Designer Sneakers'],
    url: NORDSTROM_BASE_URL + '/c/designer-sneakers-for-women'
  },
  {
    tags: ['Sneakers', 'Canvas'],
    url: NORDSTROM_BASE_URL + '/c/canvas-sneakers-for-women'
  },
  {
    tags: ['Sneakers', 'Comfort'],
    url: NORDSTROM_BASE_URL + '/c/comfort-sneakers-for-women'
  },
  {
    tags: ['Sneakers', 'Retro'],
    url: NORDSTROM_BASE_URL + '/c/womens-retro-sneakers'
  },
  {
    tags: ['Sneakers', 'Slip-On'],
    url: NORDSTROM_BASE_URL + '/c/womens-slip-on-sneakers'
  },
  {
    tags: ['Athletic', 'Running'],
    url: NORDSTROM_BASE_URL + '/c/womens-running-shoes'
  },
  {
    tags: ['Athletic', 'Training'],
    url: NORDSTROM_BASE_URL + '/c/womens-training-shoes'
  },
  {
    tags: ['Athletic', 'Walking'],
    url: NORDSTROM_BASE_URL + '/c/womens-walking-shoes'
  },
  {
    tags: ['Athletic', 'Hiking'],
    url: NORDSTROM_BASE_URL + '/c/womens-hiking-shoes'
  },
  {
    tags: ['Athletic', 'Tennis'],
    url: NORDSTROM_BASE_URL + '/c/womens-tennis-shoes'
  },
  {
    tags: ['Wedges', 'Boots'],
    url: NORDSTROM_BASE_URL + '/c/boot-wedges-for-women'
  },
  {
    tags: ['Wedges', 'Booties'],
    url: NORDSTROM_BASE_URL + '/c/booties-wedges-for-women'
  },
  {
    tags: ['Wedges', 'Comfort'],
    url: NORDSTROM_BASE_URL + '/c/comfort-wedges'
  },
  {
    tags: ['Wedges', 'Pumps'],
    url: NORDSTROM_BASE_URL + '/c/wedge-pumps-for-women'
  },
  {
    tags: ['Wedges', 'Sandals'],
    url: NORDSTROM_BASE_URL + '/c/wedge-sandals-for-women'
  },
  {
    tags: ['Wedges', 'Sneakers'],
    url: NORDSTROM_BASE_URL + '/c/wedge-sneakers-for-women'
  },
  {
    tags: ['Booties', 'Block Heel'],
    url: NORDSTROM_BASE_URL + '/c/block-heel-booties'
  },
  {
    tags: ['Booties', 'Comfort'],
    url: NORDSTROM_BASE_URL + '/c/comfort-booties'
  },
  {
    tags: ['Booties', 'Flats'],
    url: NORDSTROM_BASE_URL + '/c/flat-booties'
  },
  {
    tags: ['Booties', 'Fringe'],
    url: NORDSTROM_BASE_URL + '/c/womens-fringe-booties'
  },
  {
    tags: ['Booties', 'Heels'],
    url: NORDSTROM_BASE_URL + '/c/heeled-booties'
  },
  {
    tags: ['Booties', 'Lace-Ups'],
    url: NORDSTROM_BASE_URL + '/c/lace-up-booties'
  },
  {
    tags: ['Booties', 'Moto & Combat'],
    url: NORDSTROM_BASE_URL + '/c/moto-combat-booties'
  },
  {
    tags: ['Booties', 'Peep Toe'],
    url: NORDSTROM_BASE_URL + '/c/peep-toe-booties'
  },
  {
    tags: ['Booties', 'Wedges'],
    url: NORDSTROM_BASE_URL + '/c/wedge-booties'
  },
  {
    tags: ['Booties', 'Western'],
    url: NORDSTROM_BASE_URL + '/c/western-booties'
  },
  {
    tags: ['Pumps', 'Block Heel'],
    url: NORDSTROM_BASE_URL + '/c/block-heel-pumps'
  },
  {
    tags: ['Pumps', 'Classic'],
    url: NORDSTROM_BASE_URL + '/c/womens-classic-pumps'
  },
  {
    tags: ['Pumps', 'Comfort'],
    url: NORDSTROM_BASE_URL + '/c/comfort-pumps-for-women'
  },
  {
    tags: ['Pumps', "D'Orsay"],
    url: NORDSTROM_BASE_URL + '/c/womens-dorsay-pumps'
  },
  {
    tags: ['Pumps', 'Kitten Heel'],
    url: NORDSTROM_BASE_URL + '/c/womens-kitten-heel-pumps'
  },
  {
    tags: ['Pumps', 'Mary Jane'],
    url: NORDSTROM_BASE_URL + '/c/womens-mary-jane-pumps'
  },
  {
    tags: ['Pumps', 'Party & Evening'],
    url: NORDSTROM_BASE_URL + '/c/party-evening-pumps'
  },
  {
    tags: ['Pumps', 'Peep Toe'],
    url: NORDSTROM_BASE_URL + '/c/womens-peep-toe-pumps'
  },
  {
    tags: ['Pumps', 'Platforms'],
    url: NORDSTROM_BASE_URL + '/c/womens-platform-pumps'
  },
  {
    tags: ['Pumps', 'Pointed Toe'],
    url: NORDSTROM_BASE_URL + '/c/pointed-toe-pumps'
  },
  {
    tags: ['Pumps', 'Slingbacks'],
    url: NORDSTROM_BASE_URL + '/c/womens-slingback-pumps'
  },
  {
    tags: ['Pumps', 'Stilettos'],
    url: NORDSTROM_BASE_URL + '/c/womens-stiletto-pumps'
  },
  {
    tags: ['Pumps', 'Wedges'],
    url: NORDSTROM_BASE_URL + '/c/womens-wedge-pumps'
  },
  {
    tags: ['Comfort', 'Boots'],
    url: NORDSTROM_BASE_URL + '/c/womens-comfort-boots'
  },
  {
    tags: ['Comfort', 'Booties'],
    url: NORDSTROM_BASE_URL + '/c/womens-comfort-booties'
  },
  {
    tags: ['Comfort', 'Flats'],
    url: NORDSTROM_BASE_URL + '/c/womens-comfort-flats'
  },
  {
    tags: ['Comfort', 'Heels'],
    url: NORDSTROM_BASE_URL + '/c/womens-comfort-heels'
  },
  {
    tags: ['Comfort', 'Pumps'],
    url: NORDSTROM_BASE_URL + '/c/womens-comfort-pumps'
  },
  {
    tags: ['Comfort', 'Sneakers'],
    url: NORDSTROM_BASE_URL + '/c/womens-comfort-sneakers'
  },
  {
    tags: ['Comfort', 'Sandals'],
    url: NORDSTROM_BASE_URL + '/c/womens-comfort-sandals'
  },
  {
    tags: ['Comfort', 'Mules & Clogs'],
    url: NORDSTROM_BASE_URL + '/c/womens-comfort-mules-clogs'
  },
  {
    tags: ['Comfort', 'Oxfords'],
    url: NORDSTROM_BASE_URL + '/c/womens-comfort-oxfords'
  },
  {
    tags: ['Comfort', 'Slippers'],
    url: NORDSTROM_BASE_URL + '/c/womens-comfort-slippers'
  },
  {
    tags: ['Comfort', 'Wedges'],
    url: NORDSTROM_BASE_URL + '/c/womens-comfort-wedges'
  },
  {
    tags: ['Party & Evening', 'Sandals'],
    url: NORDSTROM_BASE_URL + '/c/womens-evening-shoes-sandals'
  },
  {
    tags: ['Party & Evening', 'Pumps'],
    url: NORDSTROM_BASE_URL + '/c/womens-evening-shoes-pumps'
  },
  {
    tags: ['Party & Evening', 'Peep-Toe'],
    url: NORDSTROM_BASE_URL + '/c/womens-evening-shoes-peep-toe'
  },
  {
    tags: ['Party & Evening', 'Slingbacks'],
    url: NORDSTROM_BASE_URL + '/c/womens-evening-shoes-slingbacks'
  },
  {
    tags: ['Party & Evening', 'Platforms'],
    url: NORDSTROM_BASE_URL + '/c/womens-evening-shoes-platform'
  },
  {
    tags: ['Party & Evening', 'Comfort'],
    url: NORDSTROM_BASE_URL + '/c/womens-party-and-evening-comfort-shoes'
  },
  {
    tags: ['Party & Evening', 'Flats'],
    url: NORDSTROM_BASE_URL + '/c/womens-evening-shoes-flats'
  },
  {
    tags: ['Boots', 'Booties'],
    url: NORDSTROM_BASE_URL + '/c/womens-shoes-booties'
  },
  {
    tags: ['Boots', 'Comfort'],
    url: NORDSTROM_BASE_URL + '/c/comfort-boots-women'
  },
  {
    tags: ['Boots', 'Flats'],
    url: NORDSTROM_BASE_URL + '/c/flat-boots'
  },
  {
    tags: ['Boots', 'Fringe'],
    url: NORDSTROM_BASE_URL + '/c/womens-fringe-boots'
  },
  {
    tags: ['Boots', 'Heeled'],
    url: NORDSTROM_BASE_URL + '/c/heeled-boots'
  },
  {
    tags: ['Boots', 'Knee High'],
    url: NORDSTROM_BASE_URL + '/c/womens-knee-high'
  },
  {
    tags: ['Boots', 'Lace-Ups'],
    url: NORDSTROM_BASE_URL + '/c/lace-up-boots-women'
  },
  {
    tags: ['Boots', 'Mid-Calf'],
    url: NORDSTROM_BASE_URL + '/c/mid-calf-boots-for-women'
  },
  {
    tags: ['Boots', 'Moto & Combat'],
    url: NORDSTROM_BASE_URL + '/c/womens-moto-combat-boots'
  },
  {
    tags: ['Boots', 'Over the Knee'],
    url: NORDSTROM_BASE_URL + '/c/womens-over-the-knee-boots'
  },
  {
    tags: ['Boots', 'Rain & Winter', 'Extreme Cold'],
    url: NORDSTROM_BASE_URL + '/c/womens-extreme-cold-boots'
  },
  {
    tags: ['Boots', 'Rain & Winter', 'Insulated'],
    url: NORDSTROM_BASE_URL + '/c/insulated-boots-for-women'
  },
  {
    tags: ['Boots', 'Rain & Winter', 'Rain'],
    url: NORDSTROM_BASE_URL + '/c/womens-rain-boots'
  },
  {
    tags: ['Boots', 'Rain & Winter', 'Snow'],
    url: NORDSTROM_BASE_URL + '/c/snow-boots-for-women'
  },
  {
    tags: ['Boots', 'Rain & Winter', 'Water Resistant'],
    url: NORDSTROM_BASE_URL + '/c/water-resistant-boots-for-women'
  },
  {
    tags: ['Boots', 'Rain & Winter', 'Waterproof'],
    url: NORDSTROM_BASE_URL + '/c/waterproof-boots-for-women'
  },
  {
    tags: ['Boots', 'Rain & Winter', 'Winter'],
    url: NORDSTROM_BASE_URL + '/c/womens-winter-snow-boots'
  },
  {
    tags: ['Boots', 'Riding'],
    url: NORDSTROM_BASE_URL + '/c/riding-boots'
  },
  {
    tags: ['Boots', 'Wedges'],
    url: NORDSTROM_BASE_URL + '/c/wedge-boots'
  },
  {
    tags: ['Espadrilles', 'Comfort'],
    url: NORDSTROM_BASE_URL + '/c/comfort-espadrilles-for-women'
  },
  {
    tags: ['Espadrilles', 'Flats'],
    url: NORDSTROM_BASE_URL + '/c/espadrille-flats-for-women'
  },
  {
    tags: ['Espadrilles', 'Sandals'],
    url: NORDSTROM_BASE_URL + '/c/espadrille-sandals-for-women'
  },
  {
    tags: ['Espadrilles', 'Sneakers'],
    url: NORDSTROM_BASE_URL + '/c/espadrille-sneakers'
  },
  {
    tags: ['Espadrilles', 'Wedges'],
    url: NORDSTROM_BASE_URL + '/c/espadrille-wedges-for-women'
  },
  {
    tags: ['Mules'],
    url: NORDSTROM_BASE_URL + '/c/womens-mules'
  },
  {
    tags: ['Clogs'],
    url: NORDSTROM_BASE_URL + '/c/womens-clogs'
  },
  {
    tags: ['Slippers', 'Boots'],
    url: NORDSTROM_BASE_URL + '/c/womens-slippers-booties'
  },
  {
    tags: ['Slippers', 'Loafers & Moccasins'],
    url: NORDSTROM_BASE_URL + '/c/womens-slippers-loafer-moccasin'
  },
  {
    tags: ['Slippers', 'Slip-On'],
    url: NORDSTROM_BASE_URL + '/c/womens-slippers-slip-on'
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

module.exports.barneys = barneys;
module.exports.nordstrom = nordstrom;
module.exports.saks = saks;
module.exports.BARNEYS_BASE_URL = BARNEYS_BASE_URL;
module.exports.NORDSTROM_BASE_URL = NORDSTROM_BASE_URL;
module.exports.SAKS_BASE_URL = SAKS_BASE_URL;
