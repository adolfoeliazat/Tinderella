var fs = require('fs');

var mongojs = require('mongojs');
var request = require('request');

var db = mongojs('Tinderella', ['shoes']);
var USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) ' +
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 ' +
    'Safari/537.36';

/*
 * fetchURL()
 *
 * Description:
 * Use the request library to fetch the URL and pass the HTML contents to
 * helper functions.
 *
 */
var fetchURL = function(url, cb, user_agent) {
    user_agent = user_agent || USER_AGENT;

    var options = {
        url: url,
        headers: {
            'User-Agent': user_agent
        }
    };

    request.get(options).on('response', function(res) {
        if (res.statusCode != 200) {
            console.log("Error: " + res.statusCode);
            return false;
        }

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
 * Upserts the object into the shoes collection, given a unique combination
 * of retailer, product ID, and item color
 *
 */
var upsert = function(obj) {
    db.shoes.update(
        {
            retailer: obj.retailer,
            productId: obj.productId,
            color: obj.color
        },
        obj,
        { upsert: true },
        function(err, doc) {
            console.log('Saved to mongoDB: ' +
                obj.retailer +
                ':' +
                obj.productId +
                ':' +
                obj.color
            );
        }
    );
};

module.exports.fetchURL = fetchURL;
module.exports.upsert = upsert;
