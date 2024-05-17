import librosa
import os
import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Pool
from itertools import repeat

segmented_path = "./data/final2/"
mel_path = "./data/final3/"

FRAME_SIZE = 1024
HOP_LENGTH = 256
N_MELS = 90
FMIN = 1400
IMAGE_WIDTH = 128
IMAGE_HEIGHT = 128

# for i, dir_name in enumerate(os.listdir(segmented_path)):
#     for j, file_name in enumerate(os.listdir(segmented_path + dir_name)):
        

def make_melspectrogram(dir_name, done_filenames, file_name):
    if file_name in done_filenames:
        print("omitting file")
        return
    # print("dir", str(i + 1) + "/" + str(len(os.listdir(segmented_path))), "file", str(j) + "/" + str(len(os.listdir(segmented_path + dir_name))))
    fig = plt.figure(1, figsize=(IMAGE_WIDTH / plt.rcParams['figure.dpi'], IMAGE_HEIGHT / plt.rcParams['figure.dpi']), frameon=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    fig.add_axes(ax)
    ax.set_axis_off()
    y, sr = librosa.load(segmented_path + dir_name + "/" + file_name)
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
    fig.savefig(mel_path + dir_name + "/" + file_name[:-4] + ".jpg")

def apply_melspectrograms():
    dir_names = ["val"]
    for dir_name in dir_names:
        filenames = os.listdir(segmented_path + dir_name)
        done_filenames = os.listdir(mel_path + dir_name)
        done_filenames = [file[:-4] + ".mp3" for file in done_filenames]
        with Pool() as pool:
            pool.starmap(make_melspectrogram, zip(repeat(dir_name), repeat(done_filenames), filenames))

if __name__ == "__main__":
    apply_melspectrograms()