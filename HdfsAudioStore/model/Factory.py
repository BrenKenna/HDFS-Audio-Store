# -*- coding: utf-8 -*-
"""
Created on Tues May 09 11:11 2023

@author: kenna
"""

from time import time


from HdfsAudioStore.audioHandler import AudioHandler
from HdfsAudioStore.model import AudioSignal as audS
from HdfsAudioStore.model import AudioMetaData as audMD
from HdfsAudioStore.model import TrackMetaData as tMD
from HdfsAudioStore.model import AudioModel as audMod

class AudioFactory:
    """
    Class responsible for instantiating model objects
    """

    def __init__(self):
        """
        Initialize with object counters
        """
        self.audioMetaCount = 0
        self.trackMetaCount = 0
        self.audioSignalCount = 0
        self.audioModelCount = 0


    # Could be private
    def makeAudioSignal(self, comprSignal: bytes):
        """
        Instantiate an AudioSignal object from compressed audio byte array
        """
        self.audioSignalCount += 1
        return audS.AudioSignal(comprSignal)


    # Could be private
    def makeAudioMeta(self, sampleRate: int, frameCount: int, duration: float):
        """
        Instantiate an AudioMetaData object
        """
        self.audioMetaCount += 1
        return audMD.AudioMetaData(sampleRate, frameCount, duration)


    # Could be private
    def makeTrackMeta(self,trackName: str, owner: str, nowTimeStamp: time):
        """
        Instantiate a TrackMetaData object
        """
        self.trackMetaCount += 1
        return tMD.TrackMetaData(trackName, owner, nowTimeStamp)


    # Could be private
    def makeAudioModel(self, audioSignal: audS.AudioSignal, audioMeta: audMD.AudioMetaData, trackMeta: tMD.TrackMetaData):
        """
        Instantiate an AudioModel object
        """
        self.audioModelCount += 1
        return audMod.AudioModel(audioSignal, audioMeta, trackMeta)


    # Should be public
    # AudioHandler can read audio, know numpy, and provide bytes
    def constructDataStoreModel(
            self, trackName: str, owner: str, nowTimeStamp: time,
            waveBytes: bytes, sampleRate: int, frameCount: int,
            duration: float
        ):
        """
        Construct an audio data store model from input
        """
        audioSignal = self.makeAudioSignal(waveBytes)
        audioMeta = self.makeAudioMeta(sampleRate, frameCount, duration)
        trackMeta = self.makeTrackMeta(trackName, owner, nowTimeStamp)
        return self.makeAudioModel(audioSignal, audioMeta, trackMeta)