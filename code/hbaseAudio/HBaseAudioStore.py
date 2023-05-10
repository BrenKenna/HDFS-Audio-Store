#!/usr/bin/python3


import happybase
import io
import numpy as np
from typing import List, Tuple
import uuid
import time
import datetime


class HBaseAudioDataStore:

    """
    A class for storing and retrieving audio data in HBase.
    """
    def __init__(self, table_name: str, host: str, port: int):
        """
        Initializes a connection to HBase and sets the table name.
        """
        self.table_name = table_name
        self.connection = happybase.Connection(host, port)
        self.connection.open()
        self.table = self.connection.table(table_name)


    def __del__(self):
        """
        Closes the connection to HBase.
        """
        self.connection.close()

    def __open__(self):
        """
        Opens connection to HBase
        """
        self.connection.open()

    def create_table(self):
        """
        Creates an HBase table with column families 'audio' and 'metadata'.
        """
        families = {
            'audio': dict(max_versions=1),
            'audio_meta': dict(),
            'track_meta': dict()
        }
        self.connection.create_table(self.table_name, families)
        print(f'Table {self.table_name} created.')


    def generate_row_key(audio_id):
        """
        Generates a row key for the HBase table based on the audio id and start time.
        """
        timestamp = time.time()
        random_uuid = uuid.uuid4().hex
        return f"{audio_id}_{timestamp}_{random_uuid}"


    def put_audio_data(self, audio_id: str, audio_data: bytes):
        """
        Inserts audio data into HBase.
        """
        self.table.put(audio_id.encode(), {'audio:': audio_data})
        print(f'Audio data with id {audio_id} inserted into {self.table_name}.')


    def put_audio_metadata(self, audio_id: str, audio_metadata: dict):
        """
        Inserts audio metadata for audio data into HBase.
        """
        column_values = {f'audio_meta:{k}': str(v) for k, v in audio_metadata.items()}
        self.table.put(audio_id.encode(), column_values)
        print(f'Metadata for audio data with id {audio_id} inserted into {self.table_name}.')


    def put_track_metadata(self, audio_id: str, track_metadata: dict):
        """
        Inserts track metadata for audio data into HBase.
        """
        column_values = {f'audio_meta:{k}': str(v) for k, v in track_metadata.items()}
        self.table.put(audio_id.encode(), column_values)
        print(f'Metadata for audio data with id {audio_id} inserted into {self.table_name}.')


    def get_audio_data(self, audio_id: str) -> bytes:
        """
        Retrieves audio data from HBase.
        """
        audio_data = self.table.row(audio_id.encode(), columns=[b'audio:'])
        if audio_data:
            return audio_data[b'audio:']
        else:
            print(f'Audio data with id {audio_id} not found in {self.table_name}.')
            return None


    def get_audio_metadata(self, audio_id: str) -> dict:
        """
        Retrieves audio metadata for audio data from HBase.
        """
        metadata = self.table.row(audio_id.encode(), columns=[b'audio_metadata:'])
        if metadata:
            return {k.decode('utf-8').split(':')[1]: v.decode('utf-8') for k, v in metadata.items()}
        else:
            print(f'Metadata for audio data with id {audio_id} not found in {self.table_name}.')
            return None


    def get_track_metadata(self, audio_id: str) -> dict:
        """
        Retrieves track metadata for audio data from HBase.
        """
        metadata = self.table.row(audio_id.encode(), columns=[b'track_metadata:'])
        if metadata:
            return {k.decode('utf-8').split(':')[1]: v.decode('utf-8') for k, v in metadata.items()}
        else:
            print(f'Metadata for audio data with id {audio_id} not found in {self.table_name}.')
            return None

    def get_audio_slice(self, audio_id: str, start_time: float, end_time: float) -> Tuple[np.ndarray, int]:
        """
        Retrieves a slice of audio data from HBase.
        """
        audio_data = self.get_audio_data(audio_id)
        if audio_data is None:
            return None
        
        buffer = io.BytesIO(audio_data)
        audio_array = np.load(buffer)
        sample_rate = int(self.get_audio_metadata(audio_id)['sample_rate'])
        start_index = int(start_time * sample_rate)
        end_index = int(end_time * sample_rate)
        return audio_array[start_index:end_index], sample_rate