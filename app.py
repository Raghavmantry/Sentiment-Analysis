import pandas as pd
from spacy.lang.en.stop_words import STOP_WORDS
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import json
from scraper import scrapeNinjest
# import nltk
from keras.models import load_model
# from tenacity import retry
# from tensorflow.keras.preprocessing.text import Tokenizer                        
# from nltk.corpus import stopwords 
# from nltk.stem import PorterStemmer
# import numpy as np
import os
from process import pre_process, pro
import matplotlib.pyplot as plt
from io import BytesIO
import base64
model= load_model("model_lstm.h5")
# import numpy as np
# import spacy
# from sklearn.svm import LinearSVC
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.pipeline import Pipeline
# import joblib
# import string
# from tokenizer import tokenizee
# We have loaded the modek
# os.chdir(r'C:\Users\utkar\Desktop\Hate speech\Twitter_kagle')
# model = load_model("network_lstm.h5")
# model = load_model("C:\Users\utkar\Desktop\Hate speech\Twitter_kagle\model_lstm.h5")
# Now we have to process the given input and predict it using the trained model
# model_load.predict(X_val)





stopwords = list(STOP_WORDS)

# Create the app object
app = Flask(__name__)

scrapeNinjest()

@app.route('/')
def predict():
    mongo_uri = 'mongodb+srv://admin:87654321@cluster0.kimytll.mongodb.net/'

    # Connect to MongoDB
    client = MongoClient(mongo_uri)

    # Select a database and collection
    db = client['Assesment']  # Replace 'mydatabase' with your database name
    collection = db['Assesment']  # Replace 'mycollection' with your collection name

    # Retrieve data from MongoDB
    result = collection.find()
    res = []
    # Print retrieved documents
    for document in result:
        text = document.get('text', '')  # Replace 'text' with the actual field name
        lis = pre_process(text)
        pred = model.predict(lis)
        res.append([pred[0][0], pred[0][1], pred[0][2]])

    data = {
        "labels": list(range(1, len(res))),
        "pos": [],
        "neg": [],
        "neut": []
    }

    for d in res:
        a = float(d[0])  # Convert to Python float
        b = float(d[1])  # Convert to Python float
        c = float(d[2])  # Convert to Python float
        # mx = 0 
        # if a > b and a > c:
        data['neut'].append(a)
        # elif b > a and b > c:
        data['pos'].append(b)
        # elif c > a and c > b:
        data['neg'].append(c)

    json_data = json.dumps(data, indent=4)
    with open('static/data.json', 'w') as json_file:
        json_file.write(json_data)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
