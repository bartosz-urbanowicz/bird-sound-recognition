import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img
from keras.utils import to_categorical
import matplotlib.pyplot as plt
import os
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense, Activation, BatchNormalization
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
import librosa

IMAGE_WIDTH = 128
IMAGE_HEIGHT = 128
IMAGE_CHANNELS = 3
BATCH_SIZE = 32
FAST_RUN = False

FRAME_SIZE = 1024
HOP_LENGTH = 256
N_MELS = 90
FMIN = 1400

data_path = "./data/final2/"

def make_melspectrogram(dir_name, file_name):
    y, sr = librosa.load(data_path + dir_name + "/" + file_name)
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
    mel_min, mel_max = log_mel_spectrogram.min(), log_mel_spectrogram.max()
    melspectrogram_normalized = (log_mel_spectrogram - mel_min) / (mel_max - mel_min)
    melspectrogram_expanded = np.expand_dims(melspectrogram_normalized, axis=-1)
    return melspectrogram_expanded


def data_frame_from_directory(dir_name):
    categories = []
    melspectrograms = []
    for i, filename in enumerate(os.listdir(data_path + dir_name)):
        category = filename.split('_')[0]
        categories.append(category)
        print("applying mel spectrogram; dir ",dir_name , "file",  str(i) + "/", len(os.listdir(data_path + dir_name)))
        melspectrograms.append(make_melspectrogram(dir_name, filename))
    df = pd.DataFrame({
        'category': categories,
        "data": melspectrograms
    })
    return df

# train_df = data_frame_from_directory("train")
validate_df = data_frame_from_directory("val")
# test_df = data_frame_from_directory("test")

input_shape = validate_df["data"][0].shape
print("input_shape: ", input_shape)

# train_datagen = ImageDataGenerator(
#     rescale=1./255,
# )

# validation_test_datagen = ImageDataGenerator(rescale=1./255)

# train_generator = train_datagen.flow_from_dataframe(
#     train_df,
#     data_path,
#     x_col="filename",
#     y_col="category",
#     target_size=(IMAGE_WIDTH, IMAGE_HEIGHT),
#     batch_size=BATCH_SIZE,
#     class_mode="categorical",
#     shuffle=True
# )

# validation_generator = validation_test_datagen.flow_from_dataframe(
#     validate_df,
#     data_path,
#     x_col="filename",
#     y_col="category",
#     target_size=(IMAGE_WIDTH, IMAGE_HEIGHT),
#     batch_size=BATCH_SIZE,
#     class_mode="categorical",
# )

# test_generator = validation_test_datagen.flow_from_dataframe(
#     test_df,
#     data_path,
#     x_col="filename",
#     y_col="category",
#     target_size=(IMAGE_WIDTH, IMAGE_HEIGHT),
#     batch_size=BATCH_SIZE,
#     class_mode="categorical",
# )

# define model

model = Sequential()

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
model.add(Dense(2, activation='softmax'))

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

# epochs=3 if FAST_RUN else 50
# model.fit(
#     train_generator,
#     epochs = epochs,
#     validation_data = validation_generator,
#     # validation_steps=total_validate//BATCH_SIZE,
#     # batch_size=total_train//BATCH_SIZE,
#     callbacks=[
#         earlystop,
#         learning_rate_reduction
#         ]
# )

# model.save("./models/model_1_10_classes.keras")

# fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
# ax1.plot(model.history.history['loss'], color='b', label="Training loss")
# ax1.plot(model.history.history['val_loss'], color='r', label="validation loss")
# ax1.set_xticks(np.arange(1, epochs + 1, 1))
# ax1.set_yticks(np.arange(0, 2.0, 0.1))
# ax1.legend(loc='best', shadow=True)
# ax1.grid(True)

# ax2.plot(model.history.history['accuracy'], color='b', label="Training accuracy")
# ax2.plot(model.history.history['val_accuracy'], color='r',label="Validation accuracy")
# ax2.set_xticks(np.arange(1, epochs, 1))
# ax2.legend(loc='best', shadow=True)
# ax2.grid(True)

# plt.tight_layout()
# plt.show()

# # evaluate model

# loss, accuracy = model.evaluate(test_generator)
# print(f'Test accuracy: {accuracy * 100:.2f}%')

# predictions = model.predict(test_generator)
# predicted_classes = np.argmax(predictions, axis=1)
# true_classes = test_generator.classes
# class_labels = list(test_generator.class_indices.keys())

# # Display some predictions
# plt.figure(figsize=(12, 12))
# for i in range(9):
#     plt.subplot(3, 3, i + 1)
#     plt.imshow(load_img(os.path.join(data_path, test_df.iloc[i]['filename']), target_size=(IMAGE_WIDTH, IMAGE_HEIGHT)))
#     plt.title(f"True: {class_labels[true_classes[i]]}\nPred: {class_labels[predicted_classes[i]]}")
#     plt.axis('off')
# plt.tight_layout()
# plt.show()
