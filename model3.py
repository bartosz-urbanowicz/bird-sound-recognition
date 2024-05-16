import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img
import tensorflow as tf
from keras.utils import to_categorical
import matplotlib.pyplot as plt
import os
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense, Activation, BatchNormalization
from keras.callbacks import EarlyStopping, ReduceLROnPlateau

IMAGE_WIDTH = 64
IMAGE_HEIGHT = 64
IMAGE_CHANNELS = 3
BATCH_SIZE = 32
FAST_RUN = False

# build dataframe

data_path = "./data/final/"

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



train_datagen = ImageDataGenerator(
    rescale=1./255,
)

validation_test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_dataframe(
    train_df,
    data_path,
    x_col="filename",
    y_col="category",
    target_size=(IMAGE_WIDTH, IMAGE_HEIGHT),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    shuffle=True
)

validation_generator = validation_test_datagen.flow_from_dataframe(
    validate_df,
    data_path,
    x_col="filename",
    y_col="category",
    target_size=(IMAGE_WIDTH, IMAGE_HEIGHT),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
)

test_generator = validation_test_datagen.flow_from_dataframe(
    test_df,
    data_path,
    x_col="filename",
    y_col="category",
    target_size=(IMAGE_WIDTH, IMAGE_HEIGHT),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
)

# define model

model = Sequential()

vgg_16 = tf.keras.applications.VGG16(
    input_shape=(IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_CHANNELS),
    weights=None,
    classes=2
)

model.add(vgg_16)

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
    # validation_steps=total_validate//BATCH_SIZE,
    # batch_size=total_train//BATCH_SIZE,
    callbacks=[
        earlystop,
        learning_rate_reduction
        ]
)

model.save_weights("./models/model_1_2_classes.weights.h5")

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

predictions = model.predict(test_generator)
predicted_classes = np.argmax(predictions, axis=1)
true_classes = test_generator.classes
class_labels = list(test_generator.class_indices.keys())

# Display some predictions
plt.figure(figsize=(12, 12))
for i in range(9):
    plt.subplot(3, 3, i + 1)
    plt.imshow(load_img(os.path.join(data_path, test_df.iloc[i]['filename']), target_size=(IMAGE_WIDTH, IMAGE_HEIGHT)))
    plt.title(f"True: {class_labels[true_classes[i]]}\nPred: {class_labels[predicted_classes[i]]}")
    plt.axis('off')
plt.tight_layout()
plt.show()