import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from flask import Flask
from flask import request

app = Flask(__name__)

# OUR HOME PAGE
#============================================
@app.route('/')
def welcome():
    images = {img1: [img2, img3, img4, img5]}
    return render_template('index.html', images=images)


# First Template
#==============================================
# create the page the form goes to
@app.route('/image_display', methods=['POST'] )
def image_display():
    img_path_lst = []
    random_image_index = random.sample(3200, 5))
    for index in random_image_index:
        img_path_lst.append(item_path[index])

    return render_template('images.html', data = img_path_lst)

# Display Results
# ===============================================
# Calculates the mean and returns the nearnest neighbor of the means
@app.route('results', methods=['POST'])
    def results():
        likes = []
        kmeans = pickle.load(open('/Volumes/hermanng_backup/Virginia_Capstone/FeatVecs/kmeansModel.pkl','r'))
        neigh = pickle.load(open('/Volumes/hermanng_backup/Virginia_Capstone/FeatVecs/neighbors', 'r'))
        
        user_preference = request.form['user_pref']
        if user_preference == 1:
            np.append(likes, img)
        mean_img_array = np.mean(np.array([likes]))
        return neigh.kneighbors(mean_img_array, return_distance=False)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777, debug=True)




