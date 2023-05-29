# -*- coding: utf-8 -*-
"""
Created on Mon May 26 17:56 2023

@author: kenna
"""


from enum import Enum

class ColumnFamilyEnum(Enum):
    AUDIO_SIGNAL = 'audio signal'
    AUDIO_META = 'audio meta'
    TRACK_META = 'track meta'
    ALL = 'all'


    def queryVal(self, query: str):
        """
        Return whether enum has queried value
        """
        for member in ColumnFamilyEnum:
            if self.toLower(member.value) == query.lower():
                return True
            else:
                return False


    def toLower(self, input: Enum.value):
        """
        Return enum in lower case
        """
        return input.__str__().lower()


    def isAudio(self, query: str):
        """
        Verify if query is Audio Signal
        """
        return self.toLower(self.AUDIO_SIGNAL) == query.lower()


    def isAudioMeta(self, query: str):
        """
        Verify if query is Audio Meta data
        """
        return self.toLower(self.AUDIO_META) == query.lower()


    def isTrackMeta(self, query: str):
        """
        Verify if query is Audio Meta data
        """
        return self.toLower(self.AUDIO_TRACK) == query.lower()

    def isAll(self, query: str):
        """
        Verify if query is Audio Meta data
        """
        return self.toLower(self.ALL) == query.lower()
