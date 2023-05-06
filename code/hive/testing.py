#!/usr/bin/python3


# Test HBase Audio Data Store
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


# Test Hive Audio Data Store
audio_store = HiveAudioDataStore('localhost', 10000, 'default', 'audio_data')
audio_file_id = 'audio_file_1'
start_time = '2023-05-06T12:30:00'
end_time = '2023-05-06T12:40:00'
retrieved_audio_data = audio_store.query_audio_data(audio_file_id, start_time, end_time)
print(retrieved_audio_data)
audio_store.close()


# Test HDFS Audio Data Store
audio_store = HdfsAudioDataStore('hdfs://localhost:8020')
audio_file_path = '/audio/audio_file_1'
audio_data = b'\x01\x02\x03\x04\x05'
audio_store.write_audio_data(audio_file_path, audio_data)
retrieved_audio_data = audio_store.read_audio_data(audio_file_path)
print(retrieved_audio_data)
audio_store.delete_audio_data(audio_file_path)