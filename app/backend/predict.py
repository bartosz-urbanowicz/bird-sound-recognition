from keras.models import load_model, Sequential
import os
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense, Activation, BatchNormalization
from kapre.composed import get_melspectrogram_layer
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np

IMAGE_WIDTH = 128
IMAGE_HEIGHT = 128

class_labels = [
    'Aegolius funereus',
    'Emberiza citrinella', 
    'Erithacus rubecula',
    'Fringilla coelebs',
    'Parus major',
    'Periparus ater', 
    'Phylloscopus collybita',
    'Sylvia atricapilla',
    'Turdus merula',
    'Turdus philomelos'
    ]

model_path = "../../models/model_1_10_classes.keras"
image_path = 'melspectrograms/'

target_size = (128, 128)

model = load_model(model_path)

def load_and_preprocess_image(image_path):
    img = load_img(image_path, target_size=(IMAGE_WIDTH, IMAGE_HEIGHT))
    img_array = img_to_array(img)
    img_array /= 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict():
    predictions_added = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    for filename in os.listdir(image_path):
        img_array = load_and_preprocess_image(image_path + filename)
        predictions = model.predict(img_array)
        predictions_added = np.add(predictions_added, predictions)
    predicted_class_index = np.argmax(predictions_added, axis=1)[0]
    predicted_class_label = class_labels[predicted_class_index]
    return predicted_class_label, predictions_added[0][predicted_class_index] / len(os.listdir(image_path))