# Dependencies and Setup
from flask import Flask, render_template
from flask_pymongo import PyMongo 
import scrape_mars

# Flask Setup
app = Flask(__name__)


# PyMongo Connection Setup
app.config["MONGO_URI"] = "mongodb://localhost:27017/marsscrape"  
mongo = PyMongo(app)




# Flask Routes

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrapper():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return "Scraping Successful"

# Define Main Behavior
if __name__ == "__main__":
    app.run()