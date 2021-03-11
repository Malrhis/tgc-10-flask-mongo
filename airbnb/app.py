from flask import Flask, render_template, request, redirect, url_for
import os
import pymongo
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.environ.get('MONGO_URI')
DB_NAME = 'sample_airbnb'

# create the mongo client
# to allow us to connect to the mongo db
client = pymongo.MongoClient(MONGO_URI)


results = client[DB_NAME].listingsAndReviews.find().limit(20)
for r in results:
    print(r)

# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)