import librosa
import os
import matplotlib.pyplot as plt
import numpy as np
import noisereduce as nr

segmented_path = "./data/segmented/"
mel_path = "./data/mels/"

FRAME_SIZE = 1024
HOP_LENGTH = 256
N_MELS = 90
FMIN = 1400

print("creating mel spectrograms")

for i, dir_name in enumerate(os.listdir(segmented_path)):
    for j, file_name in enumerate(os.listdir(segmented_path + dir_name)):
        print("dir", str(i + 1) + "/" + str(len(os.listdir(segmented_path))), "file", str(j) + "/" + str(len(os.listdir(segmented_path + dir_name))))
        fig = plt.figure(1, figsize=(64 / plt.rcParams['figure.dpi'], 64 / plt.rcParams['figure.dpi']), frameon=False)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        fig.add_axes(ax)
        ax.set_axis_off()
        y, sr = librosa.load(segmented_path + dir_name + "/" + file_name)
        y = nr.reduce_noise(y=y, sr=sr)
        mel_spectrogram = librosa.feature.melspectrogram(y=y, 
                                        sr=sr,
                                        n_fft=FRAME_SIZE,
                                        hop_length=HOP_LENGTH,
                                        n_mels=N_MELS, # mel bands
                                        fmin=FMIN, # high-pass filter
                                        fmax=sr/2
                                        )
        log_mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)
        librosa.display.specshow(log_mel_spectrogram,
                                    x_axis="time",
                                    y_axis="mel",
                                    sr=sr, 
                                    fmax=sr/2,
                                    fmin=FMIN,
                                    ax=ax)
        fig.savefig(mel_path + file_name[:-4] + ".jpg") 

print("mel spectrograms created at", mel_path)