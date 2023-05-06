#!/usr/bin/python3

import io
import os
import pyaudio
import wave

from hdfs import InsecureClient

class HdfsAudioClient:
    def __init__(self, host: str, port: int, path: str):
        self.client = InsecureClient(f"http://{host}:{port}", user=os.environ["USER"])
        self.path = path

    def get_audio_data(self, offset: int, duration: int) -> bytes:
        with self.client.read(self.path, offset=offset, length=duration) as reader:
            return reader.read()

if __name__ == '__main__':
    # Initialize HDFS client
    hdfs_client = HdfsAudioClient('localhost', 9870, '/path/to/audio.wav')

    # Retrieve audio data
    offset = 10000
    duration = 5000
    audio_data = hdfs_client.get_audio_data(offset, duration)

    # Convert to WAV and save to file
    wav_filename = 'retrieved_audio.wav'
    with wave.open(wav_filename, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(44100)
        wav_file.writeframes(audio_data)

    # Play the WAV file
    chunk_size = 1024
    p = pyaudio.PyAudio()
    with wave.open(wav_filename, 'rb') as wav_file:
        stream = p.open(format=p.get_format_from_width(wav_file.getsampwidth()),
                        channels=wav_file.getnchannels(),
                        rate=wav_file.getframerate(),
                        output=True)
        data = wav_file.readframes(chunk_size)

        while data:
            stream.write(data)
            data = wav_file.readframes(chunk_size)

        stream.stop_stream()
        stream.close()

    p.terminate()
