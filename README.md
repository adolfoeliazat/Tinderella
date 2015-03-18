## Tinderella
[tinderellashoes](http://www.tinderellashoes.com)

### Summary

The Tinderella capstone project is a full stack computer vision project that includes the following three major components: 
..* data engieering(comprised of two pre-processing pipelines)
..* data science(feature engieering, testing and modeling building)
..* front end developement. 

The end-product is an image-based shoe recommender app called the [Tinderella](http://www.tinderellashoes.com) app. 


#### How To Use Tinderella?

* To "Like" a shoe: Swipt Right or Click on "Heart" button.
* To "Dislike" a shoe: Swipt Left or Click on "X" button.
* Result: all images that user "Liked" will appear along with new recommendations!
..* User can click on the "link" button and the original product page is opened in a new tab.
..* User can also click on the "pinit" button to pin image to Pinterest.
* After results are loaded, if user wishes to start over, scroll to bottom to click on "Start Over".


### Motivation

Shopping for women is a very visual process. Women are often inspired by what they see -magazines spreads, images on social network, However, most online retailers generate recommedations based on consumer search and view history. Two major disadvantage of this method are voilation of consumer privacy and encountering the cold start problem.

Tinderella leverages techniques used in the field of computer vision and machine learning to generate recommendations. 


### Datasource

* [Nordstrom Women Shoes](http://shop.nordstrom.com/c/womens-shoes?origin=leftnav)
* [Saks Women Shoes](http://www.saksfifthavenue.com/main/SectionPage.jsp?catId=2534374306622397&FOLDER%3C%3Efolder_id=2534374306622397)
* [Barneys New York Women Shoes](http://www.barneys.com/barneys-new-york/women/shoes)


### Technology
To run this web app, you would need the following libraries:

* pymongo
* scikit-learn 0.15.2
* pickle
* flask
* numpy

### How Was Tinderella Built?

* Web Scraping and data storage:
..* image data was stored in 
..* metadata storage in mongoDB- 16,000 images from the three datasources listed above.
* First Pipeline - Image Labeling and Standardization
* Second Pipeline - Feature Engineering and Image Processing
* Keen.io - back end for analytics apps
* Front end development
* [Insight Data Science](http://www.insightdatascience.com/fellows.html)




