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
# 3). Database Worker - Writing
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


################################################
################################################
# 
# 4). ColumnFamily Enum
# 
################################################
################################################


# Import
from HdfsAudioStore.hbaseAudio.Columns import ColumnFamilyEnum


# Fetch column family enum values 
print(ColumnFamilyEnum.values())
[ enum.toLower() for enum in ColumnFamilyEnum ]

"""
['Audio Signal', 'Audio Meta', 'Track Meta', 'All']
['audio signal', 'audio meta', 'track meta', 'all']

"""


# Search
[ ColumnFamilyEnum.hasQuery(query) for query in [ "Audio Signal", "Audio Meta", "Track Meta", "Donald Duck" ] ]
[ ColumnFamilyEnum.queryEnum(query) for query in [ "Audio Signal", "Audio Meta", "Track Meta", "Donald Duck" ] ]

"""
[True, True, True, False]

[<ColumnFamilyEnum.AUDIO_SIGNAL: 'Audio Signal'>, <ColumnFamilyEnum.AUDIO_META: 'Audio Meta'>, <ColumnFamilyEnum.TRACK_META: 'Track Meta'>, None]
"""


# Direct check
for query in [ "Audio Signal", "Audio Meta", "Track Meta" ]:
    msgs = []
    msgs.append(f'{query} is Audio Signal = {ColumnFamilyEnum.isAudio(query)}')
    msgs.append(f'{query} is Audio MetaData = {ColumnFamilyEnum.isAudioMeta(query)}')
    msgs.append(f'{query} is Track MetaData = {ColumnFamilyEnum.isTrackMeta(query)}')
    msgs.append(f'{query} is All = {ColumnFamilyEnum.isAll(query)}')
    print(msgs)

"""

['Audio Signal is Audio Signal = True', 'Audio Signal is Audio MetaData = False', 'Audio Signal is Track MetaData = False', 'Audio Signal is All = False']
['Audio Meta is Audio Signal = False', 'Audio Meta is Audio MetaData = True', 'Audio Meta is Track MetaData = False', 'Audio Meta is All = False']
['Track Meta is Audio Signal = False', 'Track Meta is Audio MetaData = False', 'Track Meta is Track MetaData = True', 'Track Meta is All = False']

"""


################################################
################################################
# 
# 5). HBaseAudioStore
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
    "audio_data",
    "cluster.audio-validation.ie",
    9090
)


# Fetch data
rowKey = "TheWhispers-And-the-Beat-Goes-On"
dir(audioDatabaseWorker.hbaseAudioStore)
audioDatabaseWorker.hbaseAudioStore.get_audio_metadata(rowKey)


audioDatabaseWorker.hbaseAudioStore.__flipState__()
metadata = audioDatabaseWorker.hbaseAudioStore.table.row(rowKey.encode(), columns=[b'audio_metadata'])

"""
{b'audio_metadata: Duration': b'405.46', b'audio_metadata: FrameCount': b'8940409', b'audio_metadata: SamplingRate': b'22050'}

get "audio_data", "TheWhispers-And-the-Beat-Goes-On", { COLUMNS => "track_metadata" }

COLUMN                                     CELL                                                                                                                      
 audio_metadata: Duration                  timestamp=2023-05-31T10:12:17.394, value=405.46                                                                           
 audio_metadata: FrameCount                timestamp=2023-05-31T10:12:17.394, value=8940409                                                                          
 audio_metadata: SamplingRate              timestamp=2023-05-31T10:12:17.394, value=22050

COLUMN                                     CELL                                                                                                                      
 track_metadata: Owner                     timestamp=2023-05-31T10:12:17.400, value=The Whispers                                                                     
 track_metadata: Timestamp                 timestamp=2023-05-31T10:12:17.400, value=1685527936.5559332                                                               
 track_metadata: TrackName                 timestamp=2023-05-31T10:12:17.400, value=And-the-Beat-Goes-On 
"""




################################################
################################################
# 
# 6). Database Worker - Reading
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
    "audio_data",
    "cluster.audio-validation.ie",
    9090
)


# Import track
owner, trackPath = ("The Whispers","band-cloud-audio-validation/real/And-the-Beat-Goes-On.wav")
audioDatabaseWorker.importTrack(trackPath, owner, "audio_1")

"""
Downloading: Bucket = band-cloud-audio-validation, Key = real/And-the-Beat-Goes-On.wav, to outFile = /home/hadoop/tmp/And-the-Beat-Goes-On.wav
RowKey: TheWhispers-And-the-Beat-Goes-On
Audio data with id TheWhispers-And-the-Beat-Goes-On inserted into audio_table.
Audio Metadata for audio data with id TheWhispers-And-the-Beat-Goes-On inserted into audio_table.
Track Metadata for audio data with id TheWhispers-And-the-Beat-Goes-On inserted into audio_table.
"""


# Fetch audio signal
rowKey = "TheWhispers-And-the-Beat-Goes-On"
audioSignal = audioDatabaseWorker.getTrack(rowKey, "Audio Signal")
print(type(audioSignal))

"""
<class 'HdfsAudioStore.model.AudioSignal.AudioSignal'>
"""


# Fetch audio meta data
rowKey = "TheWhispers-And-the-Beat-Goes-On"
audioMeta = audioDatabaseWorker.getTrack(rowKey, "Audio Meta")
print(type(audioMeta))

"""
Audio Metadata for audio data with id TheWhispers-And-the-Beat-Goes-On not found in audio_data.

Audio MetaData Results:
 {'Duration': '405.46', 'FrameCount': '8940409', 'SamplingRate': '22050'}

<class 'HdfsAudioStore.model.AudioMetaData.AudioMetaData'>
"""

# Fetch track meta data
rowKey = "TheWhispers-And-the-Beat-Goes-On"
trackMeta = audioDatabaseWorker.getTrack(rowKey, "Track Meta")
print(type(audioMeta))

"""
Track Meta Data Results:
 {'Owner': 'The Whispers', 'Timestamp': '1685527936.5559332', 'TrackName': 'And-the-Beat-Goes-On'}

<class 'HdfsAudioStore.model.AudioMetaData.AudioMetaData'>
"""


# Fetch audio model
rowKey = "TheWhispers-And-the-Beat-Goes-On"
audioModel = audioDatabaseWorker.getTrack("TheWhispers-And-the-Beat-Goes-On", "All")
print(type(audioModel))

"""
<class 'HdfsAudioStore.model.AudioModel.AudioModel'>
"""