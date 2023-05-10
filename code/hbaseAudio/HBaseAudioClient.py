# -*- coding: utf-8 -*-
"""
Created on Mon May 09 18:38 2023

@author: kenna
"""

# Import interfaces
from audioHandler import AudioHandler
import HBaseAudioStore


# May drop in favor of workers
class HBaseAudioClient:
    """
    Class for get/posting audio to HBase table
    """

    def __init__(self, table_name: str, host: str, port: int):
        """
        Instantiate HBaseAudioClient with HBaseAudioDataStore and AudioHandler.
        Holds references to table name, host and port (logging) 
        """
        self.table_name = table_name
        self.host = host
        self.port = port
        self.hbaseAudioStore = HBaseAudioStore.HBaseAudioDataStore(table_name, host, port)
        self.audioHandler = AudioHandler.AudioHandler()

    def reconnect(self):
        """
        Reinstantiate AudioDataStore because it is unstable, exceptions thrown after 1 query
        """
        self.hbaseAudioStore.__del__() # Closes connection
        self.hbaseAudioStore = HBaseAudioStore.HBaseAudioDataStore(self.table_name, self.host, self.port)

    def importAudio_aws(self, bucket: str, key: str, outPath: str):
        """
        Import audio from an s3 bucket, given owner id
        """
        
        # Download audio/wav from s3
        trackData = self.audioHandler.fetchAudio(bucket, key, outPath)
