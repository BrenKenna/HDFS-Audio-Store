#!/usr/bin/python3
"""
Created on Mon May 26 17:56 2023

@author: kenna
"""

# Import required modules
import json

# Import system modules
from HdfsAudioStore.workers import DatabaseWorker
from HdfsAudioStore.audioHandler import AudioHandler


# Write json
def writeJSON(data: dict, outJson: str):
    """
    Helper method to write json files
    """
    with open(outJson, 'w') as outfile:
        json.dump(data, outfile)
    outfile.close()


class HBaseMain:
    """
    Entry point for main application using HBaseMain orientated database worker
    """

    def __init__(self, table_name: str, host: str, port: int, create_table = False):
        """
        Initialize HBaseMain
        """
        self.audioHandler = AudioHandler.AudioHandler()
        self.table_name = table_name
        self.host = host
        self.port = port
        if create_table is True:
            self.audioDatabaseWorker = DatabaseWorker.DatabaseWorker(self.table_name, self.host, self.port, createTable = True)
        else:
            self.audioDatabaseWorker = DatabaseWorker.DatabaseWorker(self.table_name, self.host, self.port)


    def importTrack(self, trackPath: str, owner: str, rowKey: str = None):
        """
        Import a track
        """
        print(f'Main-HBase Wrapper: Using rowKey = {rowKey}')
        if rowKey is None:
            return self.audioDatabaseWorker.importTrack(trackPath, owner, audio_id = None)
        else:
            return self.audioDatabaseWorker.importTrack(trackPath, owner, audio_id = rowKey)


    def fetchAudioSignal(self, rowKey: str):
        """
        Fetch audio signal
        """
        return self.audioDatabaseWorker.getTrack(rowKey, "Audio Signal")


    def fetchAudioMetaData(self, rowKey: str):
        """
        Fetch audio metadata
        """
        return self.audioDatabaseWorker.getTrack(rowKey, "Audio Meta")


    def fetchTrackMetaData(self, rowKey: str):
        """
        Fetch track metadata
        """
        return self.audioDatabaseWorker.getTrack(rowKey, "Track Meta")


    def fetchAudioModel(self, rowKey: str):
        """
        Fetch audio model
        """
        return self.audioDatabaseWorker.getTrack(rowKey, "All")


    def writeAudio(self, rowKey: str, outPath: str):
        """
        Fetch audio model from DB and write to local storage
        """

        # Fetch model and write wav
        audioModel = self.fetchAudioModel(rowKey)
        self.audioHandler.writeAudio(audioModel, outPath)

        # Write audio metadata
        writeJSON(audioModel.getAudioMetaData().toDict(), str(outPath + "/AudioMetaData.json"))

        # Write track metadata
        writeJSON(audioModel.getTrackMetaData().toDict(), str(outPath + "/TrackMetaData.json"))