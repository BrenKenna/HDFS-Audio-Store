# -*- coding: utf-8 -*-
"""
Created on Mon May 26 16:39 2023

@author: kenna
"""


class TrackMetaData:
    """
    Model class for track meta data
    """

    def __init__(self, trackName: str, owner: str, creationDate: str):
        """
        Construct track meta data from track name, creation date etc
        """
        self.trackName = trackName
        self.owner = owner
        self.creationDate = creationDate


    def getOwner(self):
        """
        Method to retrieve owner of track
        """
        return self.owner


    def getCreationDate(self):
        """
        Method to retrieve creation date
        """
        return self.creationDate


    def getTrackName(self):
        """
        Method to retrieve track name
        """
        return self.trackName