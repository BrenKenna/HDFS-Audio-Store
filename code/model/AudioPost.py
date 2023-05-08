#!/usr/bin/python3


class AudioPost:
    """
    Model class for audio data posted to DB
    """

    def __init__(self, audio: str, metadata: AudioMetaData):
        self.audio = audio,
        self.metadata = metadata