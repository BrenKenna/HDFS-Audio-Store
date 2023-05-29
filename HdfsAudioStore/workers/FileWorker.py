# -*- coding: utf-8 -*-
"""
Created on Mon May 26 17:56 2023

@author: kenna
"""


import os
import time

from HdfsAudioStore.audioHandler import AudioHandler
from HdfsAudioStore.model import AudioInput

def getNow():
    """
    Helper method get now
    """
    return time.time()


class FileWorker:
    """
    Class to support reading audio files from s3 using audio handler
    """
    def __init__(self):
        self.audioHandler = AudioHandler.AudioHandler()


    def downloadAudio(self, audioInputModel: AudioInput.AudioInputModel):
        """
        Download supplied audio
        """

        # Initialize vars
        bucket = audioInputModel.getTrackPath().split('/')[0]
        key = "/".join(audioInputModel.getTrackPath().split('/')[1:-2])
        outPath = str(os.getcwd() + "/tmp/")

        # Fetch track
        os.makedirs(os.path.dirname(outPath), exist_ok = True)
        self.s3Client.download_file(bucket, key, )
        return str(outPath + audioInputModel.getBaseName())


    def fetchAudioFile(self, trackPath: str, owner: str):
        """
        Fetch audio file from storage
        """

        # Download Audio
        audioInput = AudioInput.AudioInputModel(trackPath, owner)
        outFile = self.downloadAudio(audioInput)

        # Build audio model
        audioModels = self.audioHandler.loadAudio(outFile)
        trackMeta = self.audioHandler.makeTrackMeta(
            audioInput.getTrackPath(),
            audioInput.getOwner(),
            getNow()
        )
        audioModel = self.audioHandler.makeAudioModel(
            audioModels["audioSignal"],
            audioModels["audioMeta"],
            trackMeta
        )

        # Return model
        return audioModel