# Import Dependencies

from flask import Flask, render_template, redirect

from flask_pymongo import PyMongo

import Scrape_MissionToMars                  # import Scrape_MissionToMars.py python code file



# Create an instance of Flask app

app = Flask(__name__)



#Use flask_pymongo to set up connection to MongoDB

# Will be using

#   MongoDB Database: mars_db

# MongoDB Collection: mars_dict



# Connection to 'mars_db' database

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"

mongo = PyMongo(app)



# Create route that renders index.html template and finds documents from MongoDB

@app.route("/")

def home():

    # Check for previously stored data for display from the collection 'mars_dict'

    mars_info_data = mongo.db.mars_dict.find_one()

    # Return template and any stored data for display on the web page 'index.html'

    return render_template("index.html", mars_dict=mars_info_data)



# Route that will trigger scrape function

@app.route("/scrape")

def scrape():



    # Call the "scrape()" function from the python file "scrape_mars"

    mars_data = Scrape_MissionToMars.scrape()



    # Perform update/insert of the scrpaed data into collection

    # "mars_dict" in MongoDB "mars_db"

    mongo.db.mars_dict.update({}, mars_data, upsert=True)



    # return redirect("/", code=302)

    return redirect("/")



# Call the main function

if __name__ == "__main__":

    app.run(debug= True)