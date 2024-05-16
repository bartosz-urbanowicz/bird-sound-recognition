from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['POST'])
def upload_audio():
    data = request.json["data"]
    print(data)
    return({"bird_name": "ptak"}, 200)