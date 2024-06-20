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

def create_mfccs(df):
    features = []
    labels = []
    for i in range(0, len(df)):
        print("calculating mfccs for file " + str(i) + "/" + str(len(df)), end="\r")
        filename = df.iloc[i]["filename"]
        y, _ = librosa.load(data_path + filename, duration=MAX_DURATION)
        mfccs = librosa.feature.mfcc(y=y, n_fft=FRAME_SIZE, hop_length=HOP_LENGTH, n_mfcc=N_MFCC)
        features.append(mfccs)
        labels.append(df.iloc[i]["category"])
    return np.array(features), to_categorical(y, num_classes=len(class_labels))

X_train, y_train = create_mfccs(train_df)
X_test, y_test = create_mfccs(test_df)
X_val, y_val = create_mfccs(validate_df)

length = len(X_train[0][0][0])

input_shape = (N_MFCC, length)
model = Sequential()
model.add(Masking(mask_value=0., input_shape=(N_MFCC, length)))
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
        # earlystop,
        learning_rate_reduction
    ]
)

model.save("./models/rnn_model_2_10_classes.keras")

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
plt.savefig('./plots/rnn_model_2_10_classes.png')

loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test accuracy: {accuracy * 100:.2f}%')
