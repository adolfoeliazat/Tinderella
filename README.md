## Tinderella - An Image-Based Shoe Recommender Project
====================================================================
![web app](https://github.com/virginiayung/Tinderella_Capstone_Project/blob/master/Others/tiny_logo.png) [www.tinderellashoes.com](http://www.tinderellashoes.com)

### Summary

The Tinderella capstone project is a full stack computer vision project that includes the following three major components: 

* Data Engieering (two image pre-processing pipelines)
* Data Science (feature engieering, testing and modeling building)
* Front End Development

The end-product is an image-based shoe recommender app called the [Tinderella](http://www.tinderellashoes.com) app. The app is both fun and efficient(generates recommendations within seconds). 


#### How To Use Tinderella?

* To "Like" a shoe: Swipt right or Click on ![heart](https://github.com/virginiayung/Tinderella_Capstone_Project/blob/master/Others/tiny_like_icon.png "Logo Title Text 1")
 button.


* To "Dislike" a shoe: Swipt left or Click on ![X](https://github.com/virginiayung/Tinderella_Capstone_Project/blob/master/Others/tiny_dislike_icon.png) button.

* Result: all images that user "Liked" will appear along with new recommendations!  
    * User can click on the "link" button and the original product page is opened in a new tab.  
    * User can also click on the "pinit" button to pin image to Pinterest. 
* After results are loaded, if the user wishes to start over, scroll to bottom to click on "Start Over".


### Motivation

Shopping for women is a very visual process. Women are constantly stimulated and inspired by what they see - magazines spreads, images on social network, a pair of heels worn by a woman crossing the street. However, most online retailers generate recommedations based on consumer search and view history. Two major criticisms of this approach most often are that it voilates consumer privacy and that sfaces the cold start problem.

Tinderella utilizes techniques used in the field of computer vision and machine learning to accurately and promptly generates recommendations.


### How Was Tinderella Built?

#### Web Scraping and data storage:

* 16,000 images were scraped from 3 datasources (listed below) and stored in their respective subdirectories.  
    * 6 subdirectories created: boots, flats, pumps and slingbacks, sandals, sneakers, wedges

* metadata storage in mongoDB - company(datasource), designer brand, product description, price, product link etc

#### First Pipeline - Image Labeling and Standardization

Images are "pump" into this first pipeline from each subdirectory. Each image is then resized to the following 3 sizes and the appropriate file name (company name withe product id) is attached.

* 50-by-50 px
* 100-by-100 px
* 200-by-2oo px


#### Second Pipeline - Feature Engineering

##### Pre-Transformation Feature Engineering(feature engineering on 3D structure tensor)


* 1\. Color Extraction with K Means Clustering   
* 2\. Local Histogram Equalizer   
* 3\. Local Otsu Threshold 
* 4\. Image Segmentation Algorithms: 
    * 4.1\. felzenszwalb 
    * 4.2\. slic 
    * 4.2\. quickshift 
* 5\. Feature Detection Algorithms: 
    * 5.1\. CENSURE
    * 5.2\. ORB
* 6\. Edge Detection Algorithms(Transformed Image):   
    * 7.1\. Canny
    * 7.2\. Roberts
    * 7.3\. Sobel
    * 7.4\. Scharr

##### Post-Transformation Feature Engineering(feature engineering on transformed image)
* 7\. Feature Detection Algorithms:
    * 8.1\. CENSURE 
    * 8.2\. ORB



#### Testing and Modeling - 

#####Testing Methods(Use supervised learning and labels to test feature engineering results):
1. Random Forest with 5-fold Cross Validation: 

Best Results Achieved: 
* 50-by-50 px: 82% accuracy, 0.70 average F1
* 100-by-100 px: 84% accuracy, 0.71 average F1
* 200-by-2oo px: 87% accuracy, 0.72 average F1

2. Gradient Descent with 5-fold Cross Validation:
* 50-by-50 px: 66% accuracy
* 100-by-100 px: 67% accuracy
* 200-by-200 px: 70% accuracy

K-Nearest Neighbors (Visually inspect results)


##### Modeling:

* K-Means Clustering
* Nearest Neighbors (20 neighbors)


### Technology
To run this web app, you would need the following libraries:

* pymongo
* scikit-learn 0.15.2
* pickle
* flask
* numpy



### Datasource

* [Nordstrom Women Shoes](http://shop.nordstrom.com/c/womens-shoes?origin=leftnav)
* [Saks Women Shoes](http://www.saksfifthavenue.com/main/SectionPage.jsp?catId=2534374306622397&FOLDER%3C%3Efolder_id=2534374306622397)
* [Barneys New York Women Shoes](http://www.barneys.com/barneys-new-york/women/shoes)




