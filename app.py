
from nis import cat
from urllib import request
from flask import Flask, request, Response, send_file
from ml import scrape
from flask_cors import CORS
import json



# http://localhost:5000/scrape_data?data=data&cat=category&loc=location



app = Flask(__name__)

CORS(app)
@app.route("/scrape_data", methods = ['GET'])
def hello_world():
    try:
        args = request.args


        queries = json.loads(args.get("data"))
        category = args.get("cat")
        loc = args.get("loc")

        print('\n\n\n')
        print(queries)
        print(type(queries))
        print('\n\n\n')

        scraped_data = scrape(queries, category, loc)
        print(scraped_data[0], scraped_data[1])
        return send_file(scraped_data[0], attachment_filename=scraped_data[1], as_attachment=True)
    except Exception as e:
        print("ERROR!!!!",e)
        return e
