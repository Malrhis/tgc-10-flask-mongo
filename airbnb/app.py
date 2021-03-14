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
db = client[DB_NAME]


@app.route('/')
def show_listings():

    # retrive the value of the input named country
    country = request.args.get('country')
    min_beds = request.args.get('min_beds')
    page = request.args.get('page')

    # if page is empty convert it to zero
    if page is None:
        page = 0
    else:
        # Convert page into an int because it all is an integer
        page = int(page)

    criteria = {}

    if country:
        criteria['address.country'] = country

    if min_beds:
        criteria['beds'] = {
            "$gte": int(min_beds)
        }

    listings = db.listingsAndReviews.find(criteria, {
        'name': 1,
        'summary': 1,
        'images': 1,
        'address': 1,
        'beds': 1
    }).skip(page*20).limit(20)

    # for rendering in the front end
    return render_template('listings.template.html',
                           listings=listings, page=page,
                           fullpath=request.full_path)


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
