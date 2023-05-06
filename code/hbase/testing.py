# Example implementation with audio data <20 characters
audio_data = b"0123456789abcdefghijklmnopqr"
metadata = {
    "timestamp": "20220507140000",
    "duration": 10,
    "sample_rate": 44100,
    "start_time": "20220507140005",
    "end_time": "20220507140010"
}
data_store = HBaseAudioDataStore("localhost", 9090, "audio_table")
data_store.write_audio_data("audio1", audio_data, metadata)
data_store.write_audio_file("audio1", metadata, "audio1.wav")
read_audio_data = data_store.read_audio_data("audio1", "20220507140005", "20220507140010")
print(read_audio_data == audio_data)
