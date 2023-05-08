# -*- coding: utf-8 -*-
"""
Created on Mon May 26 16:39 2023

@author: kenna
"""

import AudioSignal
import AudioMetaData
import TrackMetaData

class AudiolModel:
    """
    Model class for audio data stored in database
    """

    def __init__(self, audioSignal: AudioSignal, audioMetaData: AudioMetaData, trackMetaData: TrackMetaData):
        """
        Construct a record to be stored in audio database
        """
        self.audioSignal = audioSignal
        self.audioMetaData = audioMetaData
        self.trackMetaData = trackMetaData


    def getTrackMetaData(self):
        """
        Method to retrieve track meta data attribute
        """
        return self.trackMetaData


    def getAudioMetaData(self):
        """
        Method to retrieve audio meta data attribute
        """
        return self.audioMetaData


    def getAudioSignal(self):
        """
        Method to retrieve audio signal attribute
        """
        return self.audioSignal