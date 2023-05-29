# -*- coding: utf-8 -*-
"""
Created on Mon May 26 16:39 2023

@author: kenna
"""

import os

class AudioInputModel:

    def __init__(self):
        """
        Initilize model class
        """
        self.trackName = None
        self.trackPath = None
        self.baseName = None
        self.audioType = None
        self.owner = None

    def setTrackName(self, trackName: str):
        """
        Set track name
        """
        self.trackName = trackName

    def getTrackName(self):
        """
        Get track name
        """
        return self.trackName

    def setTrackPath(self, trackPath: str):
        """
        Set track path
        """
        self.trackPath = trackPath
        self.setBaseName( os.path.basename(trackPath) )
        self.setAudioType( self.getBaseName().split('.')[-1] )
        self.setTrackName( self.getBaseName().replace( self.getAudioType(), "") )

    def getTrackPath(self):
        """
        Get track path
        """
        return self.trackPath

    def setOwner(self, owner: str):
        """
        Set owner
        """
        self.owner = owner

    def getOwner(self):
        """
        Get owner
        """
        return self.owner

    def setBaseName(self, baseName: str):
        """
        Set basename
        """
        self.baseName = baseName

    def getBaseName(self):
        """
        Get basename
        """
        return self.baseName

    def setAudioType(self, audioType: str):
        """
        Set audioType
        """
        self.audioType = audioType

    def getAudioType(self):
        """
        Get audio type
        """
        return self.audioType

    def toDict(self):
        """
        Return object as dict
        """
        return {
            "trackName": self.trackName,
            "trackPath": self.trackPath,
            "baseName": self.baseName,
            "audioType": self.audioType,
            "owner": self.owner
        }

    def setInput(self, trackPath: str, owner: str ):
        """
        Set attributes from input
        """
        self.setTrackPath(trackPath)
        self.setOwner(owner)