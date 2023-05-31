################################################
################################################
# 
# Test App
# 
################################################
################################################


# Help page
hdfs-audio-store-app.py --help

"""
usage: hdfs-audio-store-app.py [-h] [-t TABLE_NAME] [-s HOST] [-p PORT]
                               [-a ACTION] [-r READ_DATA] [-i IMPORT_DATA]
                               [-c CREATE_TABLE]

App to get and post audio data into HBase table

optional arguments:
  -h, --help            show this help message and exit
  -t TABLE_NAME, --table_name TABLE_NAME
                        HBase table
  -s HOST, --host HOST  HBase DB host
  -p PORT, --port PORT  HBase DB port
  -a ACTION, --action ACTION
                        IMPORT | EXPORT action to take on DB
  -r READ_DATA, --export_data READ_DATA
                        Data for READ operation format rowKey='' outPath=''
  -i IMPORT_DATA, --import_data IMPORT_DATA
                        Data for IMPORT operation format trackPath=,owner=
  -c CREATE_TABLE, --create_table CREATE_TABLE
                        Create table
"""



# Export audio from DB
hdfs-audio-store-app.py \
    --table_name "audio_data" \
    --host "cluster.audio-validation.ie" \
    --port "9090" \
    --action "export" \
    --export_data "rowKey='TheWhispers-And-the-Beat-Goes-On' outPath='tmp'"

ls tmp/*
cat tmp/*json

'''
Audio signal written to tmp/And-the-Beat-Goes-On.wav

tmp/And-the-Beat-Goes-On.wav  tmp/AudioMetaData.json  tmp/TrackMetaData.json

{"AudioMetaData": {"SamplingRate": "22050", "FrameCount": "8940409", "Duration": "405.46"}}
{"TrackMetaData": {"TrackName": "And-the-Beat-Goes-On", "Owner": "The Whispers", "Timestamp": "1685527936.5559332"}}
'''



# Import audio from s3
hdfs-audio-store-app.py \
    --table_name "audio_data" \
    --host "cluster.audio-validation.ie" \
    --port "9090" \
    --action "import" \
    --import_data "trackPath='band-cloud-audio-validation/real/Give-Me-The-Night.wav' owner='GeorgeBenson'"


rm tmp/Give-Me-The-Night.wav
hdfs-audio-store-app.py \
    --table_name "audio_data" \
    --host "cluster.audio-validation.ie" \
    --port "9090" \
    --action "export" \
    --export_data "rowKey='GeorgeBenson-Give-Me-The-Night' outPath='tmp'"
ls -lh tmp/*

"""

Downloading: Bucket = band-cloud-audio-validation, Key = real/Give-Me-The-Night.wav, to outFile = /home/hadoop/tmp/Give-Me-The-Night.wav
Audio data with id GeorgeBenson-Give-Me-The-Night inserted into audio_data.
Audio Metadata for audio data with id GeorgeBenson-Give-Me-The-Night inserted into audio_data.
Track Metadata for audio data with id GeorgeBenson-Give-Me-The-Night inserted into audio_data.

Audio signal written to tmp/Give-Me-The-Night.wav
-rw-rw-r-- 1 hadoop hadoop   91 May 31 13:24 tmp/AudioMetaData.json
-rw-r--r-- 1 hadoop hadoop 9.5M May 31 13:24 tmp/Give-Me-The-Night.wav
-rw-rw-r-- 1 hadoop hadoop  113 May 31 13:24 tmp/TrackMetaData.json
"""