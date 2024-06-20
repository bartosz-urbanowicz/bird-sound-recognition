from flask import Blueprint, request
import base64
from prepare_data import prepare_data
from predict import predict

prediction_blueprint = Blueprint("prediction", __name__)

def get_prediction(audio_data, model):
    wav_file = open("temp.wav", "wb")
    audio_data = base64.b64decode(audio_data)
    wav_file.write(audio_data)
    prepare_data()
    class_name, probability = predict()
    return({"bird_name": class_name, "probability": probability})

@prediction_blueprint.route("/", methods=['POST'])
def predict_route():
    data = request.json["data"]
    model = request.json["model"]
    prediction = get_prediction(data, model)
    return (prediction, 200)