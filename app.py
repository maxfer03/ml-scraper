from urllib import request
from flask import Flask, request
from ml import scrape
import json


app = Flask(__name__)

@app.route("/scrape_data")
def hello_world():
    args = request.json


    queries = args["data"]
    category = args["category"]
    loc = args["location"]

    print(queries, category)
    scraped_data = scrape(queries, category, loc)

    return scraped_data
