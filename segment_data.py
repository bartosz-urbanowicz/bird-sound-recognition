from pydub import AudioSegment
from pydub.utils import make_chunks
import os

recordings_path = "./data/xeno-canto/"
segmented_path = "./data/segmented/"

wanted_chunk_size = 5
min_chunk_size = 5

print("segmenting files")
success_count = 0
fail_count = 0
for dir_name in os.listdir(recordings_path):
    for file_name in os.listdir(recordings_path + dir_name):
        try:
            file = AudioSegment.from_mp3(recordings_path + dir_name + "/" + file_name)
            if not os.path.exists(segmented_path + dir_name):
                os.makedirs(segmented_path + dir_name)  
            chunks = make_chunks(file, wanted_chunk_size * 1000)
            for i, chunk in enumerate(chunks):
                if chunk.duration_seconds >= min_chunk_size:
                    chunk_name =  segmented_path + dir_name + "/" + file_name[:-4] + "_" + str(i) + ".mp3"
                    chunk.export(chunk_name, format="mp3")
            success_count += 1
        except Exception as e:
            fail_count += 1
            print("error processing file", recordings_path + dir_name + "/" + file_name)
print("segmenting completed,  failed", str(fail_count) + "/" + str(fail_count + success_count))
