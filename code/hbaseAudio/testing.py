#!/usr/bin/python3

#################################################
#################################################
# 
# Pretty much sound
#  - Row key should be <id>-<timestamp>
# 
#################################################
#################################################


# Import modules
import HdfsAudioStore
from HdfsAudioStore.hbaseAudio import HBaseAudioStore


# Instantiate and create table
data_store = HBaseAudioStore.HBaseAudioDataStore("audio_table", "ip-192-168-2-241.eu-west-1.compute.internal", 9090)
data_store.create_table()

"""
Table audio_table created.
"""

# Post data
audio_data = b'\x01\x02\x03\x04\x05'
metadata = {
    "timestamp": "20220507140000",
    "duration": 10,
    "sample_rate": 44100,
    "start_time": "20220507140005",
    "end_time": "20220507140010"
}
data_store.put_audio_data("audio1", audio_data)

"""
Audio data with id audio1 inserted into audio_table.
"""


# Put meta data
data_store.put_audio_metadata("audio1", metadata)

"""
Metadata for audio data with id audio1 inserted into audio_table.
"""

# Get audio data
fetchedAudio = data_store.get_audio_data("audio1")
fetchedMeta = data_store.get_audio_metadata("audio1")

"""
b'\x01\x02\x03\x04\x05'

Metadata for audio data with id audio1 not found in audio_table
"""


data_store.write_audio_file("audio1", metadata, "audio1.wav")
read_audio_data = data_store.read_audio_data("audio1", "20220507140005", "20220507140010")
print(read_audio_data == audio_data)
