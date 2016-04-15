## Tinderella Web Scraper
====

Visits three of the top US retailers and builds an index of item information,
as well as imagery, for each pair of shoes they sell.

* Barney's
* Nordstrom
* Saks Fifth Avenue

Every new shoe that the scraper identifies is upserted into the Tinderella
Mongo database, and all the corresponding images for the shoes are saved
locally as well.


### Requirements
Create a mongo DB named Tinderella, and then a collection named `shoes`.

