#!/usr/bin/python3

#################################################
#################################################
# 
# 1). Imports
# 
#################################################
#################################################


# Import modules
import HdfsAudioStore
from HdfsAudioStore.workers import FileWorker
from HdfsAudioStore.workers import DatabaseWorker
from HdfsAudioStore.hbaseAudio.Columns import ColumnFamilyEnum


# Test AudioInput
from HdfsAudioStore.model import AudioInput
audioInput = AudioInput.AudioInputModel()
owner, trackPath = ("The Whispers", "band-cloud-audio-validation/real/And-the-Beat-Goes-On.wav")
audioInput.setInput(trackPath, owner)
audioInput.toDict()

"""
{
    'trackName': 'And-the-Beat-Goes-On',
    'trackPath': 'band-cloud-audio-validation/real/And-the-Beat-Goes-On.wav',
    'baseName': 'And-the-Beat-Goes-On.wav',
    'audioType': 'wav',
    'owner': 'The Whispers'
}
"""


################################################
################################################
# 
# 2). File Worker
# 
################################################
################################################


# Import modules
from HdfsAudioStore.workers import FileWorker
from HdfsAudioStore.workers import DatabaseWorker
from HdfsAudioStore.hbaseAudio.Columns import ColumnFamilyEnum


# Fetch an audio track
audioFileWorker = FileWorker.FileWorker()
owner, trackPath = ("The Whispers","band-cloud-audio-validation/real/And-the-Beat-Goes-On.wav")
audioModel = audioFileWorker.fetchAudioFile(trackPath, owner)
print(audioModel)
print(audioModel.__dict__)
print(audioModel.toDict().keys())
print(audioModel.toDict()["AudioMetaData"])
print(audioModel.toDict()["TrackMetaData"])
print(dir(audioModel))


"""

Downloading: Bucket = band-cloud-audio-validation, Key = real/And-the-Beat-Goes-On.wav, to outFile = /home/hadoop/tmp/And-the-Beat-Goes-On.wav

{
    'audioSignal': <HdfsAudioStore.model.AudioSignal.AudioSignal object at 0x7fa9cb0f3b10>,
    'audioMetaData': <HdfsAudioStore.model.AudioMetaData.AudioMetaData object at 0x7fa9cb0cf950>
}

<HdfsAudioStore.model.TrackMetaData.TrackMetaData object at 0x7fa9cb0f3c50>

{
    'audioSignal': <HdfsAudioStore.model.AudioSignal.AudioSignal object at 0x7fd3f24bb650>,
    'audioMetaData': <HdfsAudioStore.model.AudioMetaData.AudioMetaData object at 0x7fd3ee306e10>,
    'trackMetaData': <HdfsAudioStore.model.TrackMetaData.TrackMetaData object at 0x7fd3f24e4a50>
}
dict_keys(['AudioSignal', 'AudioMetaData', 'TrackMetaData'])
{
    'SamplingRate': 22050,
    'FrameCount': 8940409,
    'Duration': 405.46
}
{
    'TrackName': 'And-the-Beat-Goes-On',
    'Owner': 'The Whispers',
    'Timestamp': 1685370300.8801775
}
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'audioMetaData', 'audioSignal', 'getAudioMetaData', 'getAudioSignal', 'getTrackMetaData', 'toDict', 'trackMetaData']

"""


# Test writing WAV from AudioHandler
from HdfsAudioStore.audioHandler import AudioHandler
import os
from datetime import datetime

audioHandler = AudioHandler.AudioHandler()
audioHandler.writeAudio(audioModel, "tmp")

os.remove("tmp/And-the-Beat-Goes-On.wav")
audioHandler.testWriteAudio(audioModel, "tmp")
datetime.fromtimestamp(os.path.getctime("tmp/And-the-Beat-Goes-On.wav"))

"""

Error file tmp/And-the-Beat-Goes-On.wav already exists.
Audio signal written to tmp/And-the-Beat-Goes-On.wav
datetime.datetime(2023, 5, 30, 8, 43, 2, 525133)

===> Can get the below if the compressed signal is passed
    -> Perhaps AudioSignal has a state
    -> Compression/Decompression actions changes this
    -> Breaks point of use though as the DatabaseWorker should request this from AudioHandler

-> PySoundFile input validation not that great, is a dynamic language...

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib/python3.7/site-packages/HdfsAudioStore/audioHandler/AudioHandler.py", line 121, in writeAudio
    audioModel.getAudioMetaData().getSamplingRate()
  File "/usr/lib/python3.7/site-packages/soundfile.py", line 429, in write
    channels = data.shape[1]
IndexError: tuple index out of range
"""


################################################
################################################
# 
# 3). Database Worker
# 
################################################
################################################


# Import modules
import HdfsAudioStore
from HdfsAudioStore.workers import FileWorker
from HdfsAudioStore.workers import DatabaseWorker
from HdfsAudioStore.hbaseAudio.Columns import ColumnFamilyEnum


# Fetch column family enum values & Construct DB worker
columns = ColumnFamilyEnum.values()
audioDatabaseWorker = DatabaseWorker.DatabaseWorker(
    "audio_table",
    "cluster.audio-validation.ie",
    9090
)

"""
Table audio_data created.
"""

# Import track
owner, trackPath = ("The Whispers","band-cloud-audio-validation/real/And-the-Beat-Goes-On.wav")
audioDatabaseWorker.importTrack(trackPath, owner, "audio_1")


"""

Downloading: Bucket = band-cloud-audio-validation, Key = real/And-the-Beat-Goes-On.wav, to outFile = /home/hadoop/tmp/And-the-Beat-Goes-On.wav
RowKey: TheWhispers-And-the-Beat-Goes-On
Audio data with id TheWhispers-And-the-Beat-Goes-On inserted into audio_table.
Metadata for audio data with id TheWhispers-And-the-Beat-Goes-On inserted into audio_table.
Metadata for audio data with id TheWhispers-And-the-Beat-Goes-On inserted into audio_table.

____________________________________

Troubleshooting notes

=> Get below with default config, changing on master produces second. Fine if config is rolled across nodes
hbase.client.keyvalue.maxsize=0 
Hbase_thrift.IllegalArgument: IllegalArgument(message=b'java.lang.IllegalArgumentException: KeyValue size too large

Hbase_thrift.IOError: 
IOError(message=b'org.apache.hadoop.hbase.client.RetriesExhaustedWithDetailsException: Failed 1 action: org.apache.hadoop.hbase.DoNotRetryIOException: Cell[TheWhispers-And-the-Beat-Goes-On/audio:/LATEST_TIMESTAMP/Put/vlen=33201903/seqid=0] 
with size 33201964 exceeds limit of 10485760 bytes

Not picking up 75000000 after setting on master & restarting
    => Rolling config update is needed here

"""



