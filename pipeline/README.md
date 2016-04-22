## Tinderella Pipeline
======

### Overview
The pipeline processes all the scraped images and metadata to produce a matrix of relations between similar shoes, available for querying through the recommendation server.

The pipeline takes the following elements for input:
* Directory of images
* Database of image metadata

The end result of the pipeline are two data models:
1. Feature matrix for all shoes
2. 20 nearest neighbors (shoes) for all shoes

### Pre-processing
* (in progress) Remove borders from shoe images if they exist
* Standardize image sizes to a square, with shoe image centered


### How to set up Virtualenv
1. Install virtualenv
2. Run virtualenv on the pipeline folder to set up the environment: ```virtualenv pipeline/```
3. Activate the environment whenever running any pipeline code: ```source bin/activate```
4. To deactivate the virtual environment, run ```deactivate``` from the pipeline folder


### Recommendation Server
The recommendation server runs on port 8010 and exposes several API endpoints:


#### GET /recommendations/
Returns an array of shoe recommendations given an array of shoe IDs.
