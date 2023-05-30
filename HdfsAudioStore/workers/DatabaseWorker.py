# -*- coding: utf-8 -*-
"""
Created on Mon May 26 17:56 2023

@author: kenna
"""

# System modules
from HdfsAudioStore.workers import FileWorker
from HdfsAudioStore.audioHandler import AudioHandler
from HdfsAudioStore.hbaseAudio import HBaseAudioStore
from HdfsAudioStore.model import AudioModel
from HdfsAudioStore.hbaseAudio import Columns


class DatabaseWorker:
    """
    Class to support HBaseAudioStore with storing audio files from s3 in it
    """

    def __init__(self, table_name: str, host: str, port: int, createTable = False):

        # Compose supporting modules
        self.fileWorker = FileWorker.FileWorker()
        self.audioHandler = AudioHandler.AudioHandler()
        self.hbaseColumns = Columns.ColumnFamilyEnum

        # Define HBase config
        self.table_name = table_name
        self.host = host
        self.port = port
        self.hbaseAudioStore = HBaseAudioStore.HBaseAudioDataStore(self.table_name, self.host, self.port)
        self.createTable = createTable
        if createTable is True:
            self.hbaseAudioStore.create_table()

    def importTrack(self, trackPath: str, owner: str, audio_id: str):
        """
        Import track from s3 into HBase table
        """

        # Download track
        audioModel = self.fileWorker.fetchAudioFile(trackPath, owner)
        type(audioModel)

        # Post audio signal
        dict = audioModel.getTrackMetaData().toDict()["TrackMetaData"]
        rowKey = str(dict["Owner"].replace(" ", "") + "-" + dict["TrackName"])
        print("RowKey:\t" + rowKey)
        self.hbaseAudioStore.put_audio_data(rowKey, audioModel)

        # Post audio metadata
        self.hbaseAudioStore.put_audio_metadata(audioModel)

        # Post tracj metadata
        self.hbaseAudioStore.put_track_metadata(audioModel)


    def handleColumnFamily(self, column: str):
        """
        Check if column choice is valid
        """
        return self.hbaseColumns.queryVal(str)


    # What columns? Supported by enum => AudioSignal, AudioMeta, TrackMeta, ALL
    def getTrack(self, audioId: str, column: str):
        """
        Fetch audio model from DB
        """

        # Explode if invalid
        isValid = self.handleColumnFamily(column)
        if isValid is False:
            return None

        # Fetch required data
        if self.hbaseColumns.isAudio(column):
            audioSignal = self.hbaseAudioStore.get_audio_data(audioId)
            audioSignal = self.audioHandler.rebuildAudio(audioSignal)
            return audioSignal

        # Audio meta
        elif self.hbaseColumns.isAudioMeta(column):
            audioMeta = self.hbaseAudioStore.get_audio_metadata(audioId)
            audioMeta = self.audioHandler.makeTrackMeta(audioMeta)
            return audioMeta

        # Track meta
        elif self.hbaseColumns.isTrackMeta(column):
            trackMeta = self.hbaseAudioStore.get_track_metadata(audioId)
            trackMeta = self.audioHandler.makeTrackMeta(trackMeta)
            return trackMeta

        # Fetch all
        else:

            # Construct components
            audioSignal = self.hbaseAudioStore.get_audio_data(audioId)
            audioSignal = self.audioHandler.rebuildAudio(audioSignal)
            audioMeta = self.hbaseAudioStore.get_audio_metadata(audioId)
            audioMeta = self.audioHandler.makeTrackMeta(audioMeta)
            trackMeta = self.hbaseAudioStore.get_track_metadata(audioId)
            trackMeta = self.audioHandler.makeTrackMeta(trackMeta)

            # Construct & return audio model
            audioModel = AudioModel.AudioModel(audioSignal, audioMeta, trackMeta)
            return audioModel


    def fetchTrack(self, trackName: str, owner: str, outPath: str):
        """
        Fetch wav from DB
        """

        # Get track
        audioId = str(owner + "-" + trackName)
        audioModel = self.getTrack(audioId)

        # Write track
        #  only if output
        self.audioHandler.writeAudio(audioModel, outPath)