import numpy as np
import os
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
from keras.models import Sequential
from keras.layers import Dense, Dropout, Masking
from keras.layers import CuDNNLSTM as LSTM
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
import keras
from keras import backend as K
from keras.regularizers import l2

os.environ['TF_GPU_ALLOCATOR'] = 'cuda_malloc_async'

K.clear_session()

FRAME_SIZE = 1024
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

X_train = np.load("data/rnn_3_spectrograms/X_train.npy")
y_train = np.load("data/rnn_3_spectrograms/y_train.npy")
X_test = np.load("data/rnn_3_spectrograms/X_test.npy")
y_test = np.load("data/rnn_3_spectrograms/y_test.npy")
X_val = np.load("data/rnn_3_spectrograms/X_val.npy")
y_val = np.load("data/rnn_3_spectrograms/y_val.npy")

X_train = X_train[::3]
y_train = y_train[::3]
X_test = X_test[::3]
y_test = y_test[::3]
X_val = X_val[::3]
y_val = y_val[::3]

input_shape = X_train[1].shape
regularization = l2(0.0001)

model = Sequential()
model.add(LSTM(128, input_shape=input_shape, return_sequences=True, kernel_regularizer=regularization))
model.add(Dropout(0.3))
model.add(LSTM(64, return_sequences=False, kernel_regularizer=regularization))
model.add(Dropout(0.3))
model.add(Dense(64, activation='relu', kernel_regularizer=regularization))
model.add(Dropout(0.3))
model.add(Dense(64, activation='relu', kernel_regularizer=regularization))
model.add(Dropout(0.3))
model.add(Dense(len(class_labels), activation='softmax', kernel_regularizer=regularization))

opt = keras.optimizers.Adam(learning_rate=0.001)

model.compile(optimizer=opt, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

earlystop = EarlyStopping(patience=15)

learning_rate_reduction = ReduceLROnPlateau(
    monitor='val_accuracy',
    patience=5,
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

model.save("./models/rnn_model_3_10_classes.keras")

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
plt.savefig('./plots/rnn_model_3_10_classes.png')

loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test accuracy: {accuracy * 100:.2f}%')