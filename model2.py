import numpy as np
import pandas as pd
from tensorflow.keras.utils import Sequence
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img
from keras.utils import to_categorical
import matplotlib.pyplot as plt
import os
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense, Activation, BatchNormalization
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from kapre.composed import get_melspectrogram_layer
import librosa

IMAGE_WIDTH = 128
IMAGE_HEIGHT = 128
IMAGE_CHANNELS = 3
BATCH_SIZE = 32
AUDIO_DURATION = 5
SR = 22050
FAST_RUN = False

# build dataframe

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
        categories.append(class_labels.index(category))
    df = pd.DataFrame({
        'filename': [dir_name + '/' + filename for filename in filenames],
        'category': categories
    })
    return df

train_df = data_frame_from_directory("train")
validate_df = data_frame_from_directory("val")
test_df = data_frame_from_directory("test")

class AudioDataGenerator(Sequence):
    def __init__(self, df, data_path, batch_size, audio_duration, sr, n_classes, shuffle=True):
        self.df = df
        self.data_path = data_path
        self.batch_size = batch_size
        self.audio_duration = audio_duration
        self.sr = sr
        self.n_classes = n_classes
        self.shuffle = shuffle
        self.indices = np.arange(len(self.df))
        self.on_epoch_end()

    def __len__(self):
        return len(self.df) // self.batch_size

    def __getitem__(self, index):
        batch_indices = self.indices[index * self.batch_size:(index + 1) * self.batch_size]
        batch_df = self.df.iloc[batch_indices]
        X, y = self.__data_generation(batch_df)
        return X, y

    def on_epoch_end(self):
        if self.shuffle:
            np.random.shuffle(self.indices)

    def __data_generation(self, batch_df):
        X = np.empty((self.batch_size, int(self.audio_duration * self.sr), 1))
        y = np.empty((self.batch_size), dtype=int)
        
        for i, (_, row) in enumerate(batch_df.iterrows()):
            file_path = os.path.join(self.data_path, row['filename'])
            audio, _ = librosa.load(file_path, sr=self.sr, duration=self.audio_duration, mono=True)
            audio = audio[:int(self.audio_duration * self.sr)]
            audio = np.expand_dims(audio, axis=-1)
            X[i,] = audio
            y[i] = row['category']
        
        return X, to_categorical(y, num_classes=self.n_classes)

train_generator = AudioDataGenerator(train_df, data_path, BATCH_SIZE, AUDIO_DURATION, SR, len(train_df['category'].unique()), shuffle=True)
validation_generator = AudioDataGenerator(validate_df, data_path, BATCH_SIZE, AUDIO_DURATION, SR, len(validate_df['category'].unique()), shuffle=False)
test_generator = AudioDataGenerator(test_df, data_path, BATCH_SIZE, AUDIO_DURATION, SR, len(test_df['category'].unique()), shuffle=False)

# define model

FRAME_SIZE = 1024
HOP_LENGTH = 256
N_MELS = 90
FMIN = 1400
FMAX = 8000

mel_spectrogram_layer = get_melspectrogram_layer(
    n_fft=FRAME_SIZE,
    hop_length=HOP_LENGTH,
    n_mels=N_MELS,
    mel_f_min=FMIN,
    mel_f_max=FMAX,
)

model = Sequential()

model.add(mel_spectrogram_layer)

model.add(Conv2D(32, (5, 5), activation='relu', input_shape=(IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_CHANNELS))) # 32 3x3 filters
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.4))

model.add(Conv2D(64, (5, 5), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))

model.add(Conv2D(128, (5, 5), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))

model.add(Conv2D(256, (5, 5), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))

model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Dense(train_generator.n_classes, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

#define model callbacks

earlystop = EarlyStopping(patience=15)

learning_rate_reduction = ReduceLROnPlateau(
    monitor='val_accuracy',
    patience=2,
    verbose=1,
    factor=0.5,
    min_lr=0.00001
)

# fit model

epochs=3 if FAST_RUN else 50
model.fit(
    train_generator,
    epochs = epochs,
    validation_data = validation_generator,
    callbacks=[
        earlystop,
        learning_rate_reduction
        ]
)

model.save_weights("./models/model_2_10_classes.weights.h5")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
ax1.plot(model.history.history['loss'], color='b', label="Training loss")
ax1.plot(model.history.history['val_loss'], color='r', label="validation loss")
ax1.set_xticks(np.arange(1, epochs + 1, 1))
ax1.set_yticks(np.arange(0, 2.0, 0.1))
ax1.legend(loc='best', shadow=True)
ax1.grid(True)

ax2.plot(model.history.history['accuracy'], color='b', label="Training accuracy")
ax2.plot(model.history.history['val_accuracy'], color='r',label="Validation accuracy")
ax2.set_xticks(np.arange(1, epochs, 1))
ax2.legend(loc='best', shadow=True)
ax2.grid(True)

plt.tight_layout()
plt.show()

# evaluate model

loss, accuracy = model.evaluate(test_generator)
print(f'Test accuracy: {accuracy * 100:.2f}%')
