# -*- coding: utf-8 -*-
"""
Created on Mon May 26 16:39 2023

@author: kenna
"""

class AudioSignal:
    """
    Model class for audio signals
    """
    def __init__(self, wave: bytes):
        """
        Construct audio model from audio signal
        """
        self.wave = wave


    def getWave(self):
        """
        Method to retrieve audio signal
        """
        return self.wave


    def toDict(self):
        """
        Return attributes as dictionary
        """
        return {
            "AudioSignal": {
                "Audio": self.wave
            }
        }