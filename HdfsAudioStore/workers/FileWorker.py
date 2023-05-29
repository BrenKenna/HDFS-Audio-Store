# -*- coding: utf-8 -*-
"""
Created on Mon May 26 17:56 2023

@author: kenna
"""


import boto3
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
        self.s3Client = boto3.client('s3')


    def downloadAudio(self, audioInputModel: AudioInput.AudioInputModel):
        """
        Download supplied audio
        """

        # Initialize vars
        bucket = audioInputModel.getTrackPath().split('/')[0]
        prefix = "/".join(audioInputModel.getTrackPath().split('/')[1:-1])
        key = str(prefix + "/" + audioInputModel.getBaseName())
        outPath = str(os.getcwd() + "/tmp/")
        outFile = str(outPath + audioInputModel.getBaseName())

        # Fetch track
        os.makedirs(os.path.dirname(outPath), exist_ok = True)
        print("Downloading: Bucket = " + bucket + ", Key = " + key + ", to outFile = " + outFile)
        self.s3Client.download_file(bucket, key, outFile)
        return outFile


    def fetchAudioFile(self, trackPath: str, owner: str):
        """
        Fetch audio file from storage
        """

        # Download Audio
        audioInput = AudioInput.AudioInputModel()
        audioInput.setInput(trackPath, owner)
        outFile = self.downloadAudio(audioInput)

        # Build audio model
        audioModels = self.audioHandler.loadAudio(outFile)
        trackMeta = self.audioHandler.makeTrackMeta(
            audioInput.getTrackName(),
            audioInput.getOwner(),
            getNow()
        )
        # print(audioModels)
        # print(trackMeta)
        audioModel = self.audioHandler.makeAudioModel(
            audioModels["audioSignal"],
            audioModels["audioMetaData"],
            trackMeta
        )

        # Return model
        return audioModel