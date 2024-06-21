from keras.models import load_model
from pydub import AudioSegment
import librosa
import numpy as np

FRAME_SIZE = 1024
HOP_LENGTH = 256
N_MELS = 90
FMIN = 1400
EXPECTED_SHAPE = (90, 431)

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

model_path = "../../models/rnn_model_3_10_classes.keras"
audio_path = 'temp.wav'

model = load_model(model_path)

# def split_audio(file_path, segment_length=5000):
#     audio = AudioSegment.from_file(file_path)
#     segments = []
#     for i in range(0, len(audio), segment_length):
#         segment = audio[i:i + segment_length]
#         segments.append(segment)
#     return segments

def split_audio(file_path, segment_length=5):
    y, sr = librosa.load(file_path)
    segments = []
    segment_samples = segment_length * sr
    total_length = librosa.get_duration(y=y, sr=sr)
    num_segments = int(np.ceil(total_length / segment_length))
    for i in range(num_segments):
        start_sample = i * segment_samples
        end_sample = min((i + 1) * segment_samples, len(y))
        segments.append(y[start_sample:end_sample])
    return segments

def create_melspectrogram(segment, sr=22050):
    melspec =  librosa.feature.melspectrogram(
        y=segment, 
        sr=sr,
        n_fft=FRAME_SIZE,
        hop_length=HOP_LENGTH,
        n_mels=N_MELS,
        fmin=FMIN,
        fmax=sr/2
    )
    if melspec.shape[1] > EXPECTED_SHAPE[1]:
        melspec = melspec[:, :EXPECTED_SHAPE[1]]
    elif melspec.shape[1] < EXPECTED_SHAPE[1]:
        pad_width = EXPECTED_SHAPE[1] - melspec.shape[1]
        melspec = np.pad(melspec, ((0, 0), (0, pad_width)), mode='constant')
    return melspec

def predict_rnn():
    predictions_added = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    segments = split_audio(audio_path)
    for i, segment in enumerate(segments):
        melspectrogram = create_melspectrogram(segment)
        melspectrogram = melspectrogram[np.newaxis, ...]
        predictions = model.predict(melspectrogram)
        print(predictions)
        predictions_added = np.add(predictions_added, predictions)
    predicted_class_index = np.argmax(predictions_added, axis=1)[0]
    predicted_class_label = class_labels[predicted_class_index]
    return predicted_class_label, predictions_added[0][predicted_class_index] / len(segments)
    
