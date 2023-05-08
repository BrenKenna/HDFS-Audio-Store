#!/usr/bin/python3


class AudioMetaData:
    """
    Model class for metadata of audio 
    """

    def __init__(self, name, frameCount, duration, sampleRate, owner, postDate):
        """
        Instantiate AudioMetaData class
        """
        self.name = name
        self.frameCount = frameCount
        self.duration = duration
        self.sampleRate = sampleRate
        self.owner = owner
        self.postDate = postDate