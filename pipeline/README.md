## Tinderella Pipeline
======

The pipeline processes all the scraped images and metadata to produce a matrix of relations between similar shoes, available for querying through the recommendation server. 

The pipeline takes the following elements for input:
* Directory of images
* Database of image metadata

The end result of the pipeline are two data models:
1. Feature matrix for all shoes
2. 20 nearest neighbors (shoes) for all shoes


### Recommendation Server

The recommendation server runs on port 8010 and exposes several API endpoints:

#### GET /recommendations/
Returns an array of shoe recommendations given an array of shoe IDs. 
