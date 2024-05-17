from pydub import AudioSegment
from pydub.utils import make_chunks
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import librosa

recording_path = "temp.wav"
segmented_path = "segmented"
mel_path = "melspectrograms"
wanted_chunk_size = 5
min_chunk_size = 5

FRAME_SIZE = 1024
HOP_LENGTH = 256
N_MELS = 90
FMIN = 1400
IMAGE_WIDTH = 128
IMAGE_HEIGHT = 128

def make_melspectrogram(file_name):
    fig = plt.figure(1, figsize=(IMAGE_WIDTH / plt.rcParams['figure.dpi'], IMAGE_HEIGHT / plt.rcParams['figure.dpi']), frameon=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    fig.add_axes(ax)
    ax.set_axis_off()
    y, sr = librosa.load(segmented_path + "/" + file_name)
    mel_spectrogram = librosa.feature.melspectrogram(
        y=y, 
        sr=sr,
        n_fft=FRAME_SIZE,
        hop_length=HOP_LENGTH,
        n_mels=N_MELS, # mel bands
        fmin=FMIN, # high-pass filter
        fmax=sr/2
    )
    log_mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)
    librosa.display.specshow(
        log_mel_spectrogram,
        x_axis="time",
        y_axis="mel",
        sr=sr,
        fmax=sr/2,
        fmin=FMIN,
        ax=ax
    )
    fig.savefig(mel_path + "/" + file_name[:-4] + ".jpg")

def prepare_data():
    for filename in os.listdir(segmented_path):
        os.remove(segmented_path + "/" + filename)
    for filename in os.listdir(mel_path):
        os.remove(mel_path + "/" + filename)
    file = AudioSegment.from_mp3(recording_path)
    chunks = make_chunks(file, wanted_chunk_size * 1000)
    for i, chunk in enumerate(chunks):
        chunk_name =  segmented_path + "/" + str(i) + ".mp3"
        chunk.export(chunk_name, format="mp3")
    for filename in os.listdir(segmented_path):
        make_melspectrogram(filename)
