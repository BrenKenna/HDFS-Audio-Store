
import io
import wave
from typing import Tuple

from pyhive import hive


class HiveAudioClient:
    def __init__(self, host: str, port: int, username: str, database: str) -> None:
        self.conn = hive.Connection(host=host, port=port, username=username, database=database)
        self.cursor = self.conn.cursor()

    def __del__(self) -> None:
        self.conn.close()

    def retrieve_audio(self, table_name: str, row_key: str, column_name: str) -> bytes:
        query = f"SELECT {column_name} FROM {table_name} WHERE row_key = '{row_key}'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result is not None:
            return result[0]
        else:
            raise ValueError(f"No audio data found for row key '{row_key}' in table '{table_name}'")


class WavFileWriter:
    def __init__(self, file_path: str, num_channels: int, sample_width: int, sample_rate: int, compression_type: str,
                 compression_name: str) -> None:
        self.file_path = file_path
        self.num_channels = num_channels
        self.sample_width = sample_width
        self.sample_rate = sample_rate
        self.compression_type = compression_type
        self.compression_name = compression_name

    def write_frames(self, audio_data: bytes) -> None:
        with wave.open(self.file_path, 'wb') as wav_file:
            wav_file.setparams(
                (self.num_channels, self.sample_width, self.sample_rate, 0, self.compression_type, self.compression_name))
            wav_file.writeframes(audio_data)


def retrieve_and_save_audio(hive_retriever: HiveAudioClient, wav_writer: WavFileWriter, table_name: str,
                            row_key: str, column_name: str) -> None:
    audio_data = hive_retriever.retrieve_audio(table_name, row_key, column_name)
    wav_writer.write_frames(io.BytesIO(audio_data).read())


# Usage example
hive_retriever = HiveAudioClient(host='localhost', port=10000, username='your_username', database='your_database')
wav_writer = WavFileWriter(file_path='audio_file.wav', num_channels=1, sample_width=2, sample_rate=16000,
                           compression_type='NONE', compression_name='NONE')
retrieve_and_save_audio(hive_retriever, wav_writer, table_name='audio_table', row_key='your_row_key',
                        column_name='audio_data')
