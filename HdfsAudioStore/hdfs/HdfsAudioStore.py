#!/usr/bin/python3

import pyarrow as pa
import pyarrow.parquet as pq

class HdfsAudioDataStore:
    def __init__(self, uri: str):
        self.fs = pa.fs.HadoopFileSystem.from_uri(uri)

    def write_audio_data(self, audio_file_path: str, audio_data: bytes):
        audio_file = pa.memory_map(audio_file_path, mode='w+', size=len(audio_data))
        audio_file.write(audio_data)
        audio_file.close()
        with self.fs.open(audio_file_path, 'wb') as out_file:
            with pa.input_stream(audio_data) as in_stream:
                out_file.write(in_stream.read())

    def read_audio_data(self, audio_file_path: str) -> bytes:
        with self.fs.open(audio_file_path, 'rb') as audio_file:
            return audio_file.read()

    def delete_audio_data(self, audio_file_path: str):
        self.fs.delete(audio_file_path)


if __name__ == '__main__':
    audio_store = HdfsAudioDataStore('hdfs://localhost:8020')
    audio_file_path = '/audio/audio_file_1'
    audio_data = b'\x01\x02\x03\x04\x05'
    audio_store.write_audio_data(audio_file_path, audio_data)
    retrieved_audio_data = audio_store.read_audio_data(audio_file_path)
    print(retrieved_audio_data)
    audio_store.delete_audio_data(audio_file_path)
