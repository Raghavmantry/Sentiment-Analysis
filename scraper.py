import pandas as pd
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import pandas as pd


def scrapeNinjest():
    URL_timeline = 'https://mastodon.social/api/v1/timelines/public'
    URL_hashtag = 'https://mastodon.social/api/v1/timelines/tag/mastodon'
    params = {
        'limit': 1000
    }

    since = pd.Timestamp('now', tz='utc') - pd.DateOffset(hour=1)
    is_end = False
    results = []
    print("************** Starting data scraping ****************")
    while True:
        r = requests.get(URL_hashtag, params=params)
        dataset = r.json()

        if len(dataset) == 0:
            break
        
        for t in dataset:
            timestamp = pd.Timestamp(t['created_at'], tz='utc')
            if timestamp <= since:
                is_end = True
                break
            soup = BeautifulSoup(t.get('content'), 'html.parser')
            results.append(soup.text)
        
        if is_end:
            break
        
        max_id = dataset[-1]['id']
        params['max_id'] = max_id

    df = pd.DataFrame(results)
    print("************** Data scraping complete ****************")
    # Convert the DataFrame to a dictionary with string keys
    data_dict = df.rename(columns={0: 'text'}).to_dict(orient='records')

    # MongoDB connection string
    mongo_uri = 'mongodb+srv://admin:87654321@cluster0.kimytll.mongodb.net/'

    # Connect to MongoDB
    client = MongoClient(mongo_uri)

    # Select a database and collection
    db = client['Assesment']  # Replace 'mydatabase' with your database name
    collection = db['Assesment']  # Replace 'mycollection' with your collection name

    # Insert data into MongoDB
    # collection.insert_many(data_dict)

    # Close the MongoDB connection
    client.close()