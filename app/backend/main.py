from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import base64
import os
from prepare_data import prepare_data
from predict import predict

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['POST'])
def upload_audio():
    data = request.json["data"]
    os.remove("temp.wav")
    wav_file = open("temp.wav", "wb")
    decode_string = base64.b64decode(data)
    wav_file.write(decode_string)
    prepare_data()
    class_name, probability = predict()
    return({"bird_name": class_name, "probability": probability}, 200)