# -*- coding: utf-8 -*-
"""
Created on Mon May 26 17:56 2023

@author: kenna
"""

from model import Factory
import librosa
import numpy as np
import zlib
import soundfile as sf
import os
import boto3

class AudioHandler:
    """
    Class to bridge datastore to audio data. Liken to utility
    """

    def __init__(self):
        """
        Initialize with audio factory
        """
        self.modelFactory = Factory.AudioFactory()
        self.s3Client = s3Client = boto3.client('s3')


    def loadAudio(self, trackPath):
        """
        Load audio into numpy array
        """

        # Read audio
        wave, sampleRate = librosa.load(trackPath)
        frameCount = wave.shape[0]
        duration = round(float(frameCount / sampleRate), 2)

        # Construct audio models
        output = {
            "audioSignal": self.modelFactory.makeAudioSignal(self.compressAudioSignal),
            "audioMetaData": self.modelFactory.makeAudioMeta(sampleRate, frameCount, duration)
        }
        return output


    def compressAudioSignal(self, signal: bytes):
        """
        Compress input audio signal
        """
        return zlib.compress(signal)


    def deCompressAudioSignal(self, signal: bytes):
        """
        Decompress input audio signal
        """
        return zlib.decompress(signal)


    def rebuildAudio(self, comprSignal: bytes)
        """
        Rebuild audio signal from compressed signal
        """
        return np.frombuffer(comprSignal, dtype="float32")


    def writeAudio(self, audioSignal: bytes, outPath: str):
        """
        Write audio signal to file
        """
        if not os.path.exists(outPath):
            sf.write(
                outPath,
                self.audioSignal,
                self.sampleRate
            )
            print(f'Audio signal written to {outPath}')
        else:
            print(f'Error file {outPath} already exists.')


    def fetchAudio(self, bucket: str, key: str, outPath: str):

        # Initialize vars
        fileName = os.path.basename(key)
        trackName = fileName.replace(".wav", "")
        outPath = str(os.getcwd() + "/tmp/")
        trackPath = str(outPath + fileName)

        # Fetch track
        os.makedirs(os.path.dirname(outPath), exist_ok = True)
        self.s3Client.download_file(bucket, key, str(outPath + fileName))
        return {
            'trackName': trackName,
            'trackPath': trackPath
        }