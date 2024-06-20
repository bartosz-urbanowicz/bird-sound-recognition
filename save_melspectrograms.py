import pandas as pd
import numpy as np
import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize
import warnings
warnings.filterwarnings('ignore')
from sklearn.model_selection import train_test_split
import tensorflow
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Masking
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from keras.utils import to_categorical
import keras

FRAME_SIZE = 1024
HOP_LENGTH = 256
FAST_RUN = False
BATCH_SIZE = 16
N_MELS = 90
FMIN = 1400

data_path = "./data/final2/"

class_labels = [
    "Parus major",
    "Emberiza citrinella",
    "Sylvia atricapilla",
    "Fringilla coelebs",
    "Phylloscopus collybita",
    "Turdus philomelos",
    "Periparus ater",
    "Erithacus rubecula",
    "Turdus merula",
    "Aegolius funereus"
]

def data_frame_from_directory(dir_name):
    filenames = os.listdir(data_path + dir_name)
    categories = []
    for filename in filenames:
        category = filename.split('_')[0]
        categories.append(category)
    df = pd.DataFrame({
        'filename': [dir_name + '/' + filename for filename in filenames],
        'category': categories
    })
    return df

train_df = data_frame_from_directory("train")
validate_df = data_frame_from_directory("val")
test_df = data_frame_from_directory("test")

if FAST_RUN:
    train_df = train_df[:10]
    validate_df = validate_df[:10]
    test_df = test_df[:10]

def create_melspectrograms(df):
    features = []
    labels = []
    for i in range(0, len(df)):
        print("calculating melspectrograms for file " + str(i) + "/" + str(len(df)), end="\r")
        filename = df.iloc[i]["filename"]
        y, sr = librosa.load(data_path + filename)
        melspectrogram = librosa.feature.melspectrogram(
            y=y, 
            sr=sr,
            n_fft=FRAME_SIZE,
            hop_length=HOP_LENGTH,
            n_mels=N_MELS, # mel bands
            fmin=FMIN, # high-pass filter
            fmax=sr/2
        )
        features.append(melspectrogram)
        labels.append(class_labels.index(df.iloc[i]["category"]))
    return np.array(features), np.array(labels)

X_train, y_train = create_melspectrograms(train_df)
X_test, y_test = create_melspectrograms(test_df)
X_val, y_val = create_melspectrograms(validate_df)

np.save("data/rnn_3_spectrograms/X_train.npy", X_train)
np.save("data/rnn_3_spectrograms/y_train.npy", y_train)
np.save("data/rnn_3_spectrograms/X_test.npy", X_test)
np.save("data/rnn_3_spectrograms/y_test.npy", y_test)
np.save("data/rnn_3_spectrograms/X_val.npy", X_val)
np.save("data/rnn_3_spectrograms/y_val.npy", y_val)


