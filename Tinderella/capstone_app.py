import pickle as pkl
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from flask import Flask, redirect, request, render_template
from flask.json import jsonify
import random
import numpy as np
from pymongo import MongoClient
import ast

app = Flask(__name__)

# Global variables
app.images = []
app.product_lst = []


# # OUR HOME PAGE
# #============================================
@app.route('/')
def welcome():
    with open('index.html') as f:
        return f.read()


# First Template
# ==============================================
# create the page the form goes to
# @app.route('/image_display')
# def image_display():
#   fname2rowInd = pkl.load(open('data/fname_to_rowIndex.pkl', 'rb'))
#   rand_fnames = random.sample(fname2rowInd, 5)
# rand_fnames = [
# 'barneys_158585078.jpg', 'barneys_158585079.jpg',
# 'barneys_158585085.jpg', 'saks_0469652878373.jpg',
# 'saks_0469653001749.jpg', 'saks_0471952635914.jpg']
#   full_rand_fnames =
# ['../static/display/%s' % rand_fname for rand_fname in rand_fnames]
#   ind_lst = [fname2rowInd[rand_fname] for rand_fname in rand_fnames]

#   print ind_lst
#   return render_template('images.html', path_lst=full_rand_fnames)

# POST /images
# ==============================================
# Returns all the images to the frontend
#
@app.route('/images', methods=['POST'])
def find_all_images():
    print request
    with open('ordered_img_lst.txt', 'r') as f:
        app.images = f.read().split('\n')
    return jsonify(images=app.images)


# POST: /results
# ===============================================
# Calculates the mean given the likes and returns the results HTML page with
# the images and metadata
@app.route('/results', methods=['POST'])
def results():
    print request

    results_images = []
    results_meta = []
    cards_liked = ast.literal_eval(request.form['cards_liked'])
    print cards_liked

    if len(cards_liked) == 0:
        return redirect('/', code=302)

    app.product_lst =
    [item.strip('.jpg').split('_', 1) for item in app.images]
    mean_img_array =
    np.mean(np.array(app.feature_matrix[cards_liked]), axis=0)

    neighbors = app.NN_model.kneighbors(
        mean_img_array,
        return_distance=False)
    print 'neighbor indices: ', neighbors[0]
    for n in neighbors[0]:
        print 'product_name = ', app.images[n]
        results_images.append(
            '/static/shoes/' + app.images[n])
        count = 0
        for collection in app.mongo_db.collection_names():
            cursor = app.mongo_db[collection].find(
                {
                 'company': app.product_lst[n][0],
                 'product_id': app.product_lst[n][1]
                })

            for info in cursor:
                if count == 0:
                    results_meta.append(info)
                count += 1

    print 'results_meta', len(results_meta)

    return render_template(
        'results.html',
        images=results_images,
        metadata=results_meta)


if __name__ == '__main__':
    # Load the feature matrix and model first
    app.feature_matrix =
    np.load('data/rescaled_new_feat_matrix_50_50_10e_test15k.npy')
    print('Feature matrix loaded')

    with open('data/NN_50_20neighbors.pkl', 'r') as m:
        app.NN_model = pkl.load(m)
    print('NN_model loaded')

    db = 'shoes'
    table_name = 'category'
    client = MongoClient()
    app.mongo_table = client[db][table_name]
    app.mongo_db = client[db]

    app.run(host='0.0.0.0', port=1111, debug=True, use_reloader=False)
