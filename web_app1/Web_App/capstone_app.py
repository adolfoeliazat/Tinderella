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
@app.route('/image_display')
def image_display():
	fname2rowInd = pkl.load(open('data/fname_to_rowIndex.pkl', 'rb'))
	rand_fnames = random.sample(fname2rowInd, 5)
	# rand_fnames = ['barneys_158585078.jpg', 'barneys_158585079.jpg', 'barneys_158585085.jpg', 'saks_0469652878373.jpg', 'saks_0469653001749.jpg', 'saks_0471952635914.jpg']
	full_rand_fnames = ['../static/display/%s' % rand_fname for rand_fname in rand_fnames]
	ind_lst = [fname2rowInd[rand_fname] for rand_fname in rand_fnames]

	print ind_lst

	return render_template('images.html', path_lst=full_rand_fnames)

@app.route('/get_likes_dislikes', methods=['POST'])
def get_likes_dislikes():
	print request
	print 'HERE'
	like, dislike
	compute mean

	data = request.json
	image url
	print data
	return data
# Display Results
# ===============================================
# Calculates the mean and returns the nearnest neighbor of the means
@app.route('/results', methods=['POST'])
def results():


	show img_url

	# kmeans = pickle.load(open('/Volumes/hermanng_backup/Virginia_Capstone/FeatVecs/kmeansModel.pkl','r'))
	neigh = pkl.load(open('data/nearest_neighbor.pkl', 'r'))
	
	user_like = request.form['user_like']
	user_not = request.form['user_not']

	if user_like == 1:
		np.append(likes, img)
	mean_img_array = np.mean(np.array([likes]))
	return neigh.kneighbors(mean_img_array, return_distance=False)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=1111, debug=True)




