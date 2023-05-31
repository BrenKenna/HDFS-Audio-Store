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
        return [ enum.value for enum in ColumnFamilyEnum]


    def hasQuery(query: str):
        """
        Return whether enum has queried value
        """
        data = ColumnFamilyEnum.queryEnum(query)
        return data is None


    def queryEnum(query: str):
        """
        Return enum matching query
        """
        for enum in ColumnFamilyEnum:
            if ColumnFamilyEnum.toLower(enum) == query.lower():
                return enum
        return None


    def toLower(input: Enum):
        """
        Return enum in lower case
        """
        return input.value.lower()


    def isAudio(query: str):
        """
        Verify if query is Audio Signal
        """
        return ColumnFamilyEnum.toLower(ColumnFamilyEnum.AUDIO_SIGNAL) == query.lower()


    def isAudioMeta(query: str):
        """
        Verify if query is Audio Meta data
        """
        return ColumnFamilyEnum.toLower(ColumnFamilyEnum.AUDIO_META) == query.lower()


    def isTrackMeta(query: str):
        """
        Verify if query is Audio Meta data
        """
        return ColumnFamilyEnum.toLower(ColumnFamilyEnum.TRACK_META) == query.lower()


    def isAll(query: str):
        """
        Verify if query is Audio Meta data
        """
        return ColumnFamilyEnum.toLower(ColumnFamilyEnum.ALL) == query.lower()