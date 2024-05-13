
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment
from pydub.utils import make_chunks
import noisereduce as nr
import os

recordings_path = "./data/xeno-canto/"
segmented_path = "./data/segmented/"

wanted_chunk_size = 5
min_chunk_size = 4

# print("segmenting files")
# success_count = 0
# fail_count = 0
# for dir_name in os.listdir(recordings_path):
#     for file_name in os.listdir(recordings_path + dir_name):
#         try:
#             file = AudioSegment.from_mp3(recordings_path + dir_name + "/" + file_name)
#             if not os.path.exists(segmented_path + dir_name):
#                 os.makedirs(segmented_path + dir_name)  
#             chunks = make_chunks(file, wanted_chunk_size * 1000)
#             for i, chunk in enumerate(chunks):
#                 if chunk.duration_seconds > min_chunk_size:
#                     chunk_name =  segmented_path + dir_name + "/" + file_name[:-4] + "_" + str(i) + ".mp3"
#                     chunk.export(chunk_name, format="mp3")
#             success_count += 1
#         except Exception as e:
#             fail_count += 1
#             print("error processing file", recordings_path + dir_name + "/" + file_name)
# print("segmenting completed,  failed", str(fail_count) + "/" + str(fail_count + success_count))

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