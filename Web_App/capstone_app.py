import pickle as pkl
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from flask import Flask
from flask import request
from flask import render_template
import random

app = Flask(__name__)
app.likes = []

# OUR HOME PAGE
#============================================
@app.route('/')
def welcome():
    myname = "virginia"
    return render_template('index.html', data=myname)


# First Template
#==============================================
# create the page the form goes to
@app.route('/image_display' ) #, methods=['POST']
def image_display():
	fname2rowInd = pkl.load(open('data/fname_to_rowIndex.pkl', 'rb'))
	fname_lst = fname2rowInd.keys()
	ind_lst = fname2rowInd.values()

	img_path_lst = []
	random_image_index = random.sample(range(3200), 5)
	# if 
	for index in random_image_index:
		img_path_lst.append(fname_lst[index])

	# return render_template('images.html', data = img_path_lst)

# Display Results
# ===============================================
# Calculates the mean and returns the nearnest neighbor of the means
@app.route('/results', methods=['POST'])
def results():

	kmeans = pickle.load(open('/Volumes/hermanng_backup/Virginia_Capstone/FeatVecs/kmeansModel.pkl','r'))
	neigh = pickle.load(open('/Volumes/hermanng_backup/Virginia_Capstone/FeatVecs/neighbors', 'r'))
	
	user_preference = request.form['user_pref']
	if user_preference == 1:
		np.append(likes, img)
	mean_img_array = np.mean(np.array([likes]))
	return neigh.kneighbors(mean_img_array, return_distance=False)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=1111, debug=True)




