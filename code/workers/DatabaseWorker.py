# -*- coding: utf-8 -*-
"""
Created on Mon May 26 17:56 2023

@author: kenna
"""


# Useful modules
import os, sys, re
import time


# System modules
from workers import FileWorker
from audioHandler import AudioHandler
from hbaseAudio import HBaseAudioStore
from model import AudioModel
from hbaseAudio import Columns


class DatabaseWorker:
    """
    Class to support HBaseAudioStore with storing audio files from s3 in it
    """

    def __init__(self, table_name: str, host: str, port: int):

        # Compose supporting modules
        self.fileWorker = FileWorker.FileWorker()
        self.audioHandler = AudioHandler.AudioHandler()
        self.hbaseColumns = Columns.ColumnFamilyEnum()

        # Define HBase config
        self.table_name = table_name
        self.host = host
        self.port = port
        self.hbaseAudioStore = HBaseAudioStore.HBaseAudioDataStore()


    def importTrack(self, trackPath: str, owner: str):
        """
        Import track from s3 into HBase table
        """

        # Download track
        audioModel = self.fileWorker.fetchAudioFile(trackPath, owner)
        type(audioModel)

        # Post audio signal
        self.hbaseAudioStore.put_audio_data(str(owner + "-" + trackPath), audioModel.getAudioSignal())

        # Post audio metadata
        self.hbaseAudioStore.put_audio_metadata()

        # Post tracj metadata
        self.hbaseAudioStore.put_track_metadata()


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
        match column:

            # Audio Signal
            case self.hbaseColumns.AUDIO_SIGNAL:
                audioSignal = self.hbaseAudioStore.get_audio_data(audioId)
                audioSignal = self.audioHandler.rebuildAudio(audioSignal)
                return audioSignal

            # Audio meta
            case self.hbaseColumns.AUDIO_META:
                audioMeta = self.hbaseAudioStore.get_audio_metadata(audioId)
                audioMeta = self.audioHandler.makeTrackMeta(audioMeta)
                return audioMeta

            # Track meta
            case self.hbaseColumns.TRACK_META:
                trackMeta = self.hbaseAudioStore.get_track_metadata(audioId)
                trackMeta = self.audioHandler.makeTrackMeta(trackMeta)
                return trackMeta

            # Fetch all
            case _:

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