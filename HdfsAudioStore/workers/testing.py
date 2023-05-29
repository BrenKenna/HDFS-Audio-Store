#!/usr/bin/python3

#################################################
#################################################
# 
# Imports are fine
# 
#################################################
#################################################


# Import modules
import HdfsAudioStore
from HdfsAudioStore.workers import FileWorker
from HdfsAudioStore.workers import DatabaseWorker
from HdfsAudioStore.hbaseAudio.Columns import ColumnFamilyEnum




# Fetch an audio track
audioFileWorker = FileWorker.FileWorker()



# Fetch column family enum values & Construct DB worker
columns = ColumnFamilyEnum.values()
audioDatabaseWorker = DatabaseWorker.DatabaseWorker(
    "audio_table",
    "ip-192-168-2-129.eu-west-1.compute.internal",
    9090
)


