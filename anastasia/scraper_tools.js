var mongojs = require('mongojs');
var request = require('request');

var db = mongojs('Tinderella', ['shoes']);

/*
 * fetchURL()
 *
 * Description:
 * Use the request library to fetch the URL and pass the HTML contents to
 * helper functions.
 *
 */
var fetchURL = function(url, cb) {
    request.get(url).on('response', function(res) {
        var data = '';
        res.setEncoding('utf8');
        res.on('data', function(chunk) {
            data += chunk;
        });
        res.on('end', function() {
            cb(data);
        });
    });
};

/*
 * upsert()
 *
 * Description:
 * Upserts the object into the shoes collection
 *
 */
var upsert = function(obj) {
    db.shoes.update(
        {
            retailer: obj.retailer,
            productId: obj.productId
        },
        obj,
        { upsert: true },
        function(err, doc) {
            console.log('Saved to mongoDB: ' + obj.retailer + ':' + obj.productId);
        }
    );
};

module.exports.fetchURL = fetchURL;
module.exports.upsert = upsert;
