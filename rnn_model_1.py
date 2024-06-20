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
N_MFCC = 13
MAX_DURATION = 300
FAST_RUN = False
BATCH_SIZE = 16

data_path = "./data/xeno-canto/"

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

categories = []
filenames = []
for category in os.listdir(data_path):
    for filename in os.listdir(data_path + category):
        filenames.append(category + "/" + filename)
        categories.append(class_labels.index(category))
df = pd.DataFrame({
    'filename': filenames,
    'category': categories
})

def pad(arr, length):
    num_elements = arr.shape[0]
    padded_arr = np.zeros((num_elements, length))
    for i in range(num_elements):
        row_length = arr[i].size
        if row_length < length:
            total_padding = length - row_length
            left_padding = total_padding // 2
            right_padding = total_padding - left_padding
            padded_arr[i, left_padding:left_padding + row_length] = arr[i]
        else:
            padded_arr[i, :length] = arr[i][:length]
    return padded_arr

if FAST_RUN:
    df = df[:10]

data = []
max_length = 0
for i in range(0, len(df)):
    print("calculating mfccs for file " + str(i) + "/" + str(len(df)), end="\r")
    filename = df.iloc[i]["filename"]   
    y, sr = librosa.load(data_path + filename, duration=MAX_DURATION)
    mfccs = librosa.feature.mfcc(y=y, n_fft=FRAME_SIZE, hop_length=HOP_LENGTH, n_mfcc=N_MFCC)
    data.append(mfccs)
    if np.shape(mfccs)[1] > max_length:
        max_length = np.shape(mfccs)[1]
labels = []
features = []
for i in range(0, len(df)):
    print("padding mfccs " + str(i) + "/" + str(len(df)), end="\r")
    labels.append(df.iloc[i]["category"])
    features.append(pad(data[i], max_length))
X = np.array(features)
y = labels

X = np.array((X - np.min(X)) / (np.max(X) - np.min(X)))
X = X / np.std(X)
y = to_categorical(y, num_classes=len(class_labels))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=123, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=123, stratify=y_train)

input_shape = (N_MFCC, max_length)
model = Sequential()
model.add(Masking(mask_value=0., input_shape=(N_MFCC, max_length)))
model.add(LSTM(128, input_shape=input_shape, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(128, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.4))
model.add(Dense(48, activation='relu'))
model.add(Dropout(0.4))
model.add(Dense(len(class_labels), activation='softmax'))

opt = keras.optimizers.Adam(learning_rate=0.001)

model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])

earlystop = EarlyStopping(patience=15)

learning_rate_reduction = ReduceLROnPlateau(
    monitor='val_accuracy',
    patience=2,
    verbose=1,
    factor=0.5,
    min_lr=0.00001
)

epochs = 3 if FAST_RUN else 50
history = model.fit(X_train, y_train,
    epochs=epochs,
    batch_size=BATCH_SIZE,
    validation_data=(X_val, y_val), 
    shuffle=True,
    callbacks=[
        earlystop,
        learning_rate_reduction
    ]
)

model.save("./models/rnn_model_1_10_classes.keras")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
ax1.plot(history.history['loss'], color='b', label="Training loss")
ax1.plot(history.history['val_loss'], color='r', label="Validation loss")
ax1.set_xticks(np.arange(1, epochs + 1, 1))
ax1.set_yticks(np.arange(0, 2.0, 0.1))
ax1.legend(loc='best', shadow=True)
ax1.grid(True)

ax2.plot(history.history['accuracy'], color='b', label="Training accuracy")
ax2.plot(history.history['val_accuracy'], color='r', label="Validation accuracy")
ax2.set_xticks(np.arange(1, epochs, 1))
ax2.legend(loc='best', shadow=True)
ax2.grid(True)

plt.tight_layout()
plt.savefig('./plots/rnn_model_1_10_classes.png')

loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test accuracy: {accuracy * 100:.2f}%')
