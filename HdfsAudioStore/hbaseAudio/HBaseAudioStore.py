#!/usr/bin/python3


import happybase
import io
import numpy as np
from typing import List, Tuple
import uuid
import time


# Model class
from HdfsAudioStore.model import AudioSignal
from HdfsAudioStore.model import AudioMetaData
from HdfsAudioStore.model import TrackMetaData
from HdfsAudioStore.model import AudioModel
from HdfsAudioStore.model import Factory


class HBaseAudioDataStore:

    """
    A class for storing and retrieving audio data in HBase.
    """
    def __init__(self, table_name: str, host: str, port: int):
        """
        Initializes a connection to HBase and sets the table name.
        """
        self.host = host
        self.port = port
        self.table_name = table_name
        self.connection = happybase.Connection(host, port)
        self.connection.open()
        self.table = self.connection.table(table_name)
        self.state = True


    def __open__(self):
        """
        Opens connection to HBase
        """
        self.connection.close()
        self.connection = happybase.Connection(self.host, self.port)
        self.connection.open()
        self.table = self.connection.table(self.table_name)
        self.__setState__(True)


    def __setState__(self, state: bool):
        """
        Set state
        """
        self.state = state


    def __flipState__(self):
        """
        Flip state
        """
        if self.state is True:
            self.state = False
            self.__open__()
        else:
            self.state = True
            self.__open__()
        return self.state


    def create_table(self):
        """
        Creates an HBase table with column families 'audio' and 'metadata'.
        """
        if self.state is True:
            self.__flipState__()
        families = {
            'audio': dict(max_versions=1),
            'audio_metadata': dict(),
            'track_metadata': dict()
        }
        self.connection.create_table(self.table_name, families)
        self.__flipState__()
        print(f'Table {self.table_name} created.')


    def generate_row_key(audio_id):
        """
        Generates a row key for the HBase table based on the audio id and start time.
        """
        timestamp = time.time()
        random_uuid = uuid.uuid4().hex
        return f"{audio_id}_{timestamp}_{random_uuid}"


    def put_audio_data(self, audio_id: str, audioModel: AudioModel.AudioModel):
        """
        Inserts audio data into HBase.
        """
        if self.state is True:
            self.__flipState__()
        self.table.put(audio_id.encode(), {'audio:': audioModel.getAudioSignal().getWave()})
        self.__flipState__()
        print(f'Audio data with id {audio_id} inserted into {self.table_name}.')


    def put_audio_metadata(self, audio_id: str, audioModel: AudioModel.AudioModel):
        """
        Inserts audio metadata for audio data into HBase.
        """
        if self.state is True:
            self.__flipState__()
        column_values = {f'audio_metadata: {k}': str(v) for k, v in audioModel.getAudioMetaData().toDict()["AudioMetaData"].items()}
        self.table.put(audio_id.encode(), column_values)
        self.__flipState__()
        print(f'Audio Metadata for audio data with id {audio_id} inserted into {self.table_name}.')


    def put_track_metadata(self, audio_id: str, audioModel: AudioModel.AudioModel):
        """
        Inserts track metadata for audio data into HBase.
        """
        if self.state is True:
            self.__flipState__()
        column_values = {f'track_metadata: {k}': str(v) for k, v in audioModel.getTrackMetaData().toDict()["TrackMetaData"].items()}
        self.table.put(audio_id.encode(), column_values)
        self.__flipState__()
        print(f'Track Metadata for audio data with id {audio_id} inserted into {self.table_name}.')


    def get_audio_data(self, audio_id: str) -> bytes:
        """
        Retrieves audio data from HBase.
        """
        if self.state is True:
            self.__flipState__()
        audio_data = self.table.row(audio_id.encode(), columns=[b'audio:'])
        self.__flipState__()
        if audio_data:
            return audio_data[b'audio:']
        else:
            print(f'Audio data with id {audio_id} not found in {self.table_name}.')
            return None


    def get_audio_metadata(self, audio_id: str) -> dict:
        """
        Retrieves audio metadata for audio data from HBase.
        """
        if self.state is True:
            self.__flipState__()
        metadata = self.table.row(audio_id.encode(), columns=[b'audio_metadata:'])
        self.__flipState__()
        if metadata:
            return {k.decode('utf-8').split(':')[1]: v.decode('utf-8') for k, v in metadata.items()}
        else:
            print(f'Audio Metadata for audio data with id {audio_id} not found in {self.table_name}.')
            return None


    def get_track_metadata(self, audio_id: str) -> dict:
        """
        Retrieves track metadata for audio data from HBase.
        """
        if self.state is True:
            self.__flipState__()
        metadata = self.table.row(audio_id.encode(), columns=[b'track_metadata:'])
        self.__flipState__()
        if metadata:
            return {k.decode('utf-8').split(':')[1]: v.decode('utf-8') for k, v in metadata.items()}
        else:
            print(f'Track Metadata for audio data with id {audio_id} not found in {self.table_name}.')
            return None

    def get_audio_slice(self, audio_id: str, start_time: float, end_time: float) -> Tuple[np.ndarray, int]:
        """
        Retrieves a slice of audio data from HBase.
        """
        if self.state is True:
            self.__flipState__()
        audio_data = self.get_audio_data(audio_id)
        self.__flipState__()
        if audio_data is None:
            return None
        
        buffer = io.BytesIO(audio_data)
        audio_array = np.load(buffer)
        sample_rate = int(self.get_audio_metadata(audio_id)['sample_rate'])
        start_index = int(start_time * sample_rate)
        end_index = int(end_time * sample_rate)
        return audio_array[start_index:end_index], sample_rate