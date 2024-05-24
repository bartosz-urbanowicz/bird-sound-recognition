from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import base64
import os
from prepare_data import prepare_data
from predict import predict
import ffmpeg

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['POST'])
def upload_audio():
    data = request.json["data"]
    wav_file = open("temp.wav", "wb")
    input_audio_data = base64.b64decode(data)
    ffmpeg_cmd = (
        ffmpeg
        .input('pipe:', format='s16le', acodec='pcm_s16le', ar='44.1k', ac=2)
        .output('pipe:', format='s16le', acodec='pcm_s16le', ar='44.1k', ac=2)
        .run_async(pipe_stdin=True, pipe_stdout=True, quiet=True)
    )
    ffmpeg_cmd.stdin.write(input_audio_data)
    ffmpeg_cmd.stdin.close()
    audio_data, _ = ffmpeg_cmd.communicate()
    wav_file.write(audio_data)
    prepare_data()
    class_name, probability = predict()
    return({"bird_name": class_name, "probability": probability}, 200)