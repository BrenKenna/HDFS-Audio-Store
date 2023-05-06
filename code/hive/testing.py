
audio_store = HiveAudioDataStore('localhost', 10000, 'default', 'audio_data')
audio_file_id = 'audio_file_1'
start_time = '2023-05-06T12:30:00'
end_time = '2023-05-06T12:40:00'
retrieved_audio_data = audio_store.query_audio_data(audio_file_id, start_time, end_time)
print(retrieved_audio_data)
audio_store.close()