import pandas as pd
import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pickle
import joblib
from sklearn.model_selection import train_test_split
# from tensorflow.python.keras import models, layers
# import tensorflow as tf

y,sr=librosa.load('data/XC816727 - łabędź krzykliwy - Cygnus cygnus.mp3')
# librosa.display.waveshow(y,sr=sr, x_axis='time', color='cyan')
S = librosa.feature.melspectrogram(y=y, sr=sr)

fig, ax = plt.subplots() 
S_dB = librosa.power_to_db(S, ref=np.max)
img = librosa.display.specshow(S_dB, x_axis='time',
                         y_axis='mel', sr=sr,
                         fmax=8000, ax=ax)
fig.colorbar(img, ax=ax, format='%+2.0f dB')

plt.show()
print(sr)