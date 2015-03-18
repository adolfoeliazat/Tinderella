## Tinderella
[tinderellashoes](http://www.tinderellashoes.com)

### Summary

Tinderella is an image-based shoe recommender app. It was built using rigorous computer vision and machine learning algorithms.

#### How To Use Tinderella?

* To "Like" a shoe: Swipt Right or Click on "Heart" button.
* To "Dislike" a shoe: Swipt Left or Click on "X" button.
* Result: all images that user "Liked" will appear along with new recommendations!
..* User can click on the "link" button and the original product page is opened in a new tab.
..* User can also click on the "pinit" button to pin image to Pinterest.
* After results are loaded, if user wishes to start over, scroll to bottom to click on "Start Over".


### Motivation

Shopping for women is actually a very visual process. Women are often inspired by what they see -magazines spreads, images on social network, However, most online retailers generate recommedations based on consumer search and view history. Two major disadvantage of this method are voilation of consumer privacy and encountering the cold start problem.

Tinderella leverages techniques used in the field of computer vision and machine learning to generate recommendations. 


### Datasource

* [Nordstrom Women Shoes](http://shop.nordstrom.com/c/womens-shoes?origin=leftnav)
* [Saks Women Shoes](http://www.saksfifthavenue.com/main/SectionPage.jsp?catId=2534374306622397&FOLDER%3C%3Efolder_id=2534374306622397)
* [Barneys New York Women Shoes](http://www.barneys.com/barneys-new-york/women/shoes)


### Technology
To run this app, you would need the following libraries:

* pymongo
* scikit-learn 0.15.2
* pickle
* flask
* numpy

### Process

* Web Scraping - 
* First Pipeline - Image Labeling and Standardization
* Second Pipeline - Feature Engineering and Image Processing
* Keen.io - back end for analytics apps
* Front end development
* [Insight Data Science](http://www.insightdatascience.com/fellows.html)




