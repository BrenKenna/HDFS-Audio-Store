# -*- coding: utf-8 -*-
"""
Created on Mon May 26 17:56 2023

@author: kenna
"""

import librosa
import numpy as np
import zlib
import soundfile as sf
import os
from time import time


# Model class
from HdfsAudioStore.model import AudioSignal
from HdfsAudioStore.model import AudioMetaData
from HdfsAudioStore.model import TrackMetaData
from HdfsAudioStore.model import AudioModel
from HdfsAudioStore.model import Factory

#
# Decided to drop from here
#   => The thing that creates this can do that
# from hbaseAudio import HBaseAudioStore
#


#
# Maybe better as utils
#   -> Bridge can use this utilities package?
class AudioHandler:
    """
    Class to bridge datastore to audio data. Liken to utility
    """

    def __init__(self):
        """
        Initialize with audio factory
        """
        self.modelFactory = Factory.AudioFactory()


    def loadAudio(self, trackPath):
        """
        Load audio into numpy array
        """

        # Read audio
        wave, sampleRate = librosa.load(trackPath)
        sampleRate = int(sampleRate)
        frameCount = wave.shape[0]
        duration = round(float(frameCount / sampleRate), 2)
        # print("Wave Type:\t" + str(type(wave)))
        # print("Sampling Rate:\t" + str(type(wave)))
        # print("Duration:\t" + str(type(duration)))

        # Construct audio models
        output = {
            "audioSignal": self.modelFactory.makeAudioSignal(self.compressAudioSignal(wave)),
            "audioMetaData": self.modelFactory.makeAudioMeta(sampleRate, frameCount, duration)
        }
        return output


    def makeTrackMeta(self, trackName: str, owner: str, timeStamp: time):
        """
        Request factory to make track meta data object
        """
        return self.modelFactory.makeTrackMeta(trackName, owner, timeStamp)


    def makeAudioMeta(self, sampleRate: int, frameCount: int, duration: float):
        """
        Request factory to make audio meta data object
        """
        return self.modelFactory.makeAudioMeta(sampleRate, frameCount, duration)
    

    def makeAudioModel(
        self,
        audioSignal: AudioSignal.AudioSignal,
        audioMeta: AudioMetaData.AudioMetaData,
        trackMeta: TrackMetaData.TrackMetaData,
    ):
        """
        Return audio model
        """
        return self.modelFactory.makeAudioModel(audioSignal, audioMeta, trackMeta)


    def compressAudioSignal(self, signal: bytes):
        """
        Compress input audio signal
        """
        return zlib.compress(signal)


    def deCompressAudioSignal(self, signal: bytes):
        """
        Decompress input audio signal
        """
        return np.frombuffer(zlib.decompress(signal), dtype = "float32")


    def rebuildAudio(self, comprSignal: bytes):
        """
        Rebuild audio signal from compressed signal
        """
        return self.modelFactory.makeAudioSignal(self.deCompressAudioSignal(comprSignal))


    # Should really decompress signal, 
    #  as the numpy stuff is handled in this class
    def writeAudio(self, audioModel: AudioModel, outPath: str):
        """
        Write audio signal to file
        """

        # Handle outPath could be separate method
        outPath = str(outPath + "/" + audioModel.getTrackMetaData().getTrackName() + ".wav")

        if not os.path.exists(outPath):
            sf.write(
                outPath,
                audioModel.getAudioSignal().getWave(),
                audioModel.getAudioMetaData().getSamplingRate()
            )
            print(f'Audio signal written to {outPath}')
        else:
            print(f'Error file {outPath} already exists.')


    def testWriteAudio(self, audioModel: AudioModel, outPath: str):
        """
        Write audio signal to file
        """

        # Handle outPath could be separate method
        outPath = str(outPath + "/" + audioModel.getTrackMetaData().getTrackName() + ".wav")
        audioSignal = self.rebuildAudio(audioModel.getAudioSignal().getWave())

        if not os.path.exists(outPath):
            sf.write(
                outPath,
                audioSignal.getWave(),
                audioModel.getAudioMetaData().getSamplingRate()
            )
            print(f'Audio signal written to {outPath}')
        else:
            print(f'Error file {outPath} already exists.')