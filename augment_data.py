from audiomentations import Compose, AddGaussianSNR, AddShortNoises, PitchShift, Shift, TimeMask, TimeStretch
import librosa
import os
import soundfile as sf
from multiprocessing import Pool

src_path = "./data/final2/train/"
noise_path = "./data/noise/"

add_gaussian_snr = AddGaussianSNR(
    min_snr_db=3,
    max_snr_db=30,
    p=0.2
)
add_short_noises = AddShortNoises(
    sounds_path="./data/noise",
    min_snr_db=3, max_snr_db=30,
    noise_rms="relative_to_whole_input",
    min_time_between_sounds=2.0,
    max_time_between_sounds=4,
    p=0.2
)

pitch_shift = PitchShift(
    min_semitones=-3,
    max_semitones=3,
    p=0.2
)

shift = Shift(p=1)

time_mask = TimeMask(
    min_band_part=0.05,
    max_band_part=0.2,
    fade=True,
    p=0.2
)

time_stretch = TimeStretch(
    min_rate=0.9,
    max_rate=1.2,
    p=0.2
)

augment = Compose([
    add_gaussian_snr,
    add_short_noises,
    pitch_shift,
    shift,
    time_mask,
    time_stretch
])

def augment_save(filename):
    signal, sr = librosa.load(src_path + filename)
    augmented_signal = augment(signal, sr)
    sf.write(src_path + filename[:-3] + "_aug.mp3", augmented_signal, sr)

def process_files():
    with Pool() as pool:
        pool.map(augment_save, os.listdir(src_path))

if __name__ == "__main__":
    # all noise files to 22050 to not to this every time they are applied
    # for filename in os.listdir(noise_path):
    #     y, sr = librosa.load(noise_path + filename)
    #     audio_resampled = librosa.resample(y=y, orig_sr=sr, target_sr=22050)
    #     os.remove(noise_path + filename)
    #     sf.write(noise_path + filename, audio_resampled, 22050)
    process_files()