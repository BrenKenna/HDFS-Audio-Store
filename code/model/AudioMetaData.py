# -*- coding: utf-8 -*-
"""
Created on Mon May 26 16:39 2023

@author: kenna
"""

class AudioMetaData:
    """
    Model class for meta data about an audio signal
    """

    def __init__(self, samplingRate: int, frameCount: int, duration: float):
        """
        Construct an audio meta data object
        """
        self.samplingRate = samplingRate
        self.frameCount = frameCount
        self.duration = duration


    def getDuration(self):
        """
        Method to retrieve duration in human time
        """
        return self.duration


    def getFrameCount(self):
        """
        Method to retrieve frame count
        """
        return self.frameCount


    def getSamplingRate(self):
        """
        Method to retrieve sampling rate
        """
        return self.samplingRate