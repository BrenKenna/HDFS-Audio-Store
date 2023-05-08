# -*- coding: utf-8 -*-
"""
Created on Mon May 26 17:56 2023

@author: kenna
"""


############################################
############################################
# 
# 1). Audio Handler
# 
############################################
############################################


# Import required modules
import os, sys, argparse
import json
import librosa 
import numpy as np
import shutil
import zlib
import time
import boto3
"""
ImportError: urllib3 v2.0 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with OpenSSL 1.0.2k-fips  26 Jan 2017. See: https://github.com/urllib3/urllib3/issues/2168

 --> Uninstalled urllib3, then installed compliant version
 sudo pip3 install --target "/usr/lib/python3.7/site-packages/" "urllib3<1.27,>=1.25.4"
"""
s3Client = boto3.client('s3')


# Vars
bucket = "band-cloud-audio-validation"
prefix = "real"
object = "And-the-Beat-Goes-On.wav"
key = str(prefix + "/" + object)


# Fetch audio
outPath = str(os.getcwd() + "/tmp/")
trackPath = str(outPath + object)
os.makedirs(os.path.dirname(outPath), exist_ok = True)
s3Client.download_file(bucket, key, str(outPath + object)


# Load track: Wave = 8940409, ByteArray = 35761636
wave, sampleRate = librosa.load(trackPath)
frameCount = 8940409
duration = round(float(frameCount / sampleRate), 2)


# Compress & decompress
comprSignal = zlib.compress(wave.tobytes())
rebuiltBytes = zlib.decompress(comprSignal)
reBuiltSignal = np.frombuffer(rebuiltBytes, dtype="float32")
reBuiltSignal == wave

"""
array([ True,  True,  True, ...,  True,  True,  True])


Best chunk the audio array, then convert to compressed byte array
    => Chunk to 30s snippets StreamProducer from aws_code in AudioValidator
    => Story for another day
"""



############################################
############################################
# 
# 2). Model Class Construction
#
# - Will likey store all in one file
# 
############################################
############################################

# Import
import AudioSignal as audS
import AudioMetaData as audMD
import TrackMetaData as tMD
import AudioModel as audMod


# Vars
object = "And-the-Beat-Goes-On.wav"
trackName = "And-the-Beat-Goes-On"
owner = "The Whispers"
nowTimeStamp = time.time()
wave, sampleRate = librosa.load(trackPath)
frameCount = wave.shape[0]
duration = round(float(frameCount / sampleRate), 2)


# Instantiate AudioSignal
audioSignal = audS.AudioSignal(comprSignal)
audioMeta = audMD.AudioMetaData(sampleRate, frameCount, duration)
trackMeta = tMD.TrackMetaData(trackName, owner, nowTimeStamp)


# Construct audio model
audioModel = audMod.AudioModel(audioSignal, audioMeta, trackMeta)

"""
<AudioModel.AudioModel object at 0x7ff189ab3d90>
"""