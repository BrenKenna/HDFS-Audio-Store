# -*- coding: utf-8 -*-
"""
Created on Mon May 26 17:56 2023

@author: kenna
"""


from enum import Enum

class ColumnFamilyEnum(Enum):
    AUDIO_SIGNAL = 'Audio Signal'
    AUDIO_META = 'Audio Meta'
    TRACK_META = 'Track Meta'
    ALL = 'All'


    def values():
        """
        Return enum values as string array
        """
        return [ member.value for member in ColumnFamilyEnum]


    def queryVal(query: str):
        """
        Return whether enum has queried value
        """
        for member in ColumnFamilyEnum:
            if ColumnFamilyEnum.toLower(member.value) == query.lower():
                return True
            else:
                return False


    def toLower(input: Enum):
        """
        Return enum in lower case
        """
        return input.lower()


    def isAudio(query: str):
        """
        Verify if query is Audio Signal
        """
        return ColumnFamilyEnum.AUDIO_SIGNAL.toLower(ColumnFamilyEnum.AUDIO_SIGNAL) == query.lower()


    def isAudioMeta(query: str):
        """
        Verify if query is Audio Meta data
        """
        return ColumnFamilyEnum.toLower(ColumnFamilyEnum.AUDIO_META) == query.lower()


    def isTrackMeta(query: str):
        """
        Verify if query is Audio Meta data
        """
        return ColumnFamilyEnum.toLower(ColumnFamilyEnum.AUDIO_TRACK) == query.lower()


    def isAll(query: str):
        """
        Verify if query is Audio Meta data
        """
        return ColumnFamilyEnum.toLower(ColumnFamilyEnum.ALL) == query.lower()