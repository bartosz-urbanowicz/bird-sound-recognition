import os
import pandas as pd
import numpy as np
import shutil

# we cant use built in functions because datasets cannot share segments from the same recording to prevent data leakage

train_size = 0.8
val_size = 0.1
test_size = 0.1

mels_path = "./data/mels/"
dest_path = "./data/final/"

filenames = os.listdir(mels_path)
categories = []
recordings = []
for filename in filenames:
    category = filename.split("_")[0]
    categories.append(category)
    recording = filename.split("_")[0] + "_" + filename.split('_')[1]
    recordings.append(recording)

segments_df = pd.DataFrame({
    "filename": filenames,
    "category": categories,
    "recording": recordings
})


category_names = segments_df["category"].unique()

def allocate_recordings(wanted_segments):
    allocated = []
    sum_segments = 0
    indexes_to_delete = []
    for idx, row in recordings_df.iterrows():
        if sum_segments + row["segments"] <= wanted_segments:
            allocated.append(row)
            sum_segments += row["segments"]
            indexes_to_delete.append(idx)
    recordings_df.drop(indexes_to_delete, inplace=True)
    return pd.DataFrame(allocated)

train_set = pd.DataFrame()
val_set = pd.DataFrame()
test_set = pd.DataFrame()
for category_name in category_names:
    all_segments = len(segments_df[segments_df["category"] == category_name])
    train_wanted_segments = np.ceil(train_size * all_segments)
    val_wanted_segments = np.ceil(val_size * all_segments)
    test_wanted_segments = np.ceil(test_size * all_segments)

    recordings_df = segments_df[segments_df["category"] == category_name].groupby("recording").size().reset_index(name='segments').sort_values(by='segments', ascending=False)
    
    train_set = pd.concat([train_set, allocate_recordings(train_wanted_segments)], axis=0)

    val_set= pd.concat([val_set, allocate_recordings(val_wanted_segments)], axis=0)

    test_set = pd.concat([test_set, recordings_df], axis=0)

# this assumes that directories are already created
for i, row in segments_df.iterrows():
    if row["recording"] in train_set["recording"].values.tolist():
        shutil.copy2(mels_path + row["filename"], dest_path + "train")
    if row["recording"] in val_set["recording"].values.tolist():
        shutil.copy2(mels_path + row["filename"], dest_path + "val")
    if row["recording"] in test_set["recording"].values.tolist():
        shutil.copy2(mels_path + row["filename"], dest_path + "test")