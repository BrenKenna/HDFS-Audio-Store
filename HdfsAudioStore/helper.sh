#!/bin/bash

################################################
################################################
# 
# 1). Test App
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




################################################
################################################
# 
# 2). Tinkering
# 
# https://stackoverflow.com/questions/40277405/split-command-in-hbase-shell
# 
################################################
################################################


#
# Create pre-split table
#  Okish outlier region has ~4 fold less data than others, others similar
#    => Good enough for intentions on scenario replications
sudo hbase shell

```

create 'split_audio_table', 'audio', 'audio_metadata', 'track_metadata', { SPLITS => [ 'audio_1', 'audio_3', 'audio_6', 'audio_9' ] }

get_splits 'split_audio_table'

```



# Import audio from s3
table_name="split_audio_table"
count=0
awk 'NR >= 2' /usr/lib/python3.7/site-packages/HdfsAudioStore/workers/test-data.txt | while read line
    do
    
    # Set vars
    count=$(($count+1))
    owner=$(echo $line | cut -d , -f 1 | sed 's/ //g')
    trackPath=$(echo $line | cut -d , -f 2)


    # Import track
    echo -e "\\n\\nProcessing track from '${owner}':\\t${trackPath}"
    hdfs-audio-store-app.py \
        --table_name "split_audio_table_c" \
        --host "cluster.audio-validation.ie" \
        --port "9090" \
        --action "import" \
        --import_data "trackPath='${trackPath}' owner='${owner}'" \
        --rowKey "audio_${count}"
    rm -f tmp/*
done


"""


Processing track from 'TheWhispers':    band-cloud-audio-validation/real/And-the-Beat-Goes-On.wav
Downloading: Bucket = band-cloud-audio-validation, Key = real/And-the-Beat-Goes-On.wav, to outFile = /home/hadoop/tmp/And-the-Beat-Goes-On.wav
Audio data with id TheWhispers-And-the-Beat-Goes-On inserted into audio_table.
Audio Metadata for audio data with id TheWhispers-And-the-Beat-Goes-On inserted into audio_table.
Track Metadata for audio data with id TheWhispers-And-the-Beat-Goes-On inserted into audio_table.


Processing track from 'RobZombie':      band-cloud-audio-validation/real/Feel-So-Numb.wav
Downloading: Bucket = band-cloud-audio-validation, Key = real/Feel-So-Numb.wav, to outFile = /home/hadoop/tmp/Feel-So-Numb.wav
Audio data with id RobZombie-Feel-So-Numb inserted into audio_table.
Audio Metadata for audio data with id RobZombie-Feel-So-Numb inserted into audio_table.
Track Metadata for audio data with id RobZombie-Feel-So-Numb inserted into audio_table.


Processing track from 'KISS':   band-cloud-audio-validation/real/God-of-Thunder.wav
Downloading: Bucket = band-cloud-audio-validation, Key = real/God-of-Thunder.wav, to outFile = /home/hadoop/tmp/God-of-Thunder.wav
Audio data with id KISS-God-of-Thunder inserted into audio_table.
Audio Metadata for audio data with id KISS-God-of-Thunder inserted into audio_table.
Track Metadata for audio data with id KISS-God-of-Thunder inserted into audio_table.


Processing track from 'Melechesh':      and-cloud-audio-validation/real/Grand-Gathas-of-Baal-Sin.wav
Downloading: Bucket = and-cloud-audio-validation, Key = real/Grand-Gathas-of-Baal-Sin.wav, to outFile = /home/hadoop/tmp/Grand-Gathas-of-Baal-Sin.wav

botocore.exceptions.ClientError: An error occurred (404) when calling the HeadObject operation: Not Found


Processing track from 'StevieWonder':   band-cloud-audio-validation/real/Sir-Duke.wav
Downloading: Bucket = band-cloud-audio-validation, Key = real/Sir-Duke.wav, to outFile = /home/hadoop/tmp/Sir-Duke.wav
Audio data with id StevieWonder-Sir-Duke inserted into audio_table.
Audio Metadata for audio data with id StevieWonder-Sir-Duke inserted into audio_table.
Track Metadata for audio data with id StevieWonder-Sir-Duke inserted into audio_table.


Processing track from 'BrothersJohnson':        band-cloud-audio-validation/real/Stomp.wav
Downloading: Bucket = band-cloud-audio-validation, Key = real/Stomp.wav, to outFile = /home/hadoop/tmp/Stomp.wav
Audio data with id BrothersJohnson-Stomp inserted into audio_table.
Audio Metadata for audio data with id BrothersJohnson-Stomp inserted into audio_table.
Track Metadata for audio data with id BrothersJohnson-Stomp inserted into audio_table.


Processing track from 'RobZombie':      band-cloud-audio-validation/real/Superbeast.wav
Downloading: Bucket = band-cloud-audio-validation, Key = real/Superbeast.wav, to outFile = /home/hadoop/tmp/Superbeast.wav
Audio data with id RobZombie-Superbeast inserted into audio_table.
Audio Metadata for audio data with id RobZombie-Superbeast inserted into audio_table.
Track Metadata for audio data with id RobZombie-Superbeast inserted into audio_table.


Processing track from 'Melechesh':      band-cloud-audio-validation/real/Tempest-Temper-Enlil-Enraged.wav
Downloading: Bucket = band-cloud-audio-validation, Key = real/Tempest-Temper-Enlil-Enraged.wav, to outFile = /home/hadoop/tmp/Tempest-Temper-Enlil-Enraged.wav
Audio data with id Melechesh-Tempest-Temper-Enlil-Enraged inserted into audio_table.
Audio Metadata for audio data with id Melechesh-Tempest-Temper-Enlil-Enraged inserted into audio_table.
Track Metadata for audio data with id Melechesh-Tempest-Temper-Enlil-Enraged inserted into audio_table.


Processing track from 'Dissection':     band-cloud-audio-validation/real/Thorns-of-Crimson-Death.wav
Downloading: Bucket = band-cloud-audio-validation, Key = real/Thorns-of-Crimson-Death.wav, to outFile = /home/hadoop/tmp/Thorns-of-Crimson-Death.wav
Audio data with id Dissection-Thorns-of-Crimson-Death inserted into audio_table.
Audio Metadata for audio data with id Dissection-Thorns-of-Crimson-Death inserted into audio_table.
Track Metadata for audio data with id Dissection-Thorns-of-Crimson-Death inserted into audio_table.


Processing track from 'BlackSabbath':   band-cloud-audio-validation/real/Wishing-Well.wav
Downloading: Bucket = band-cloud-audio-validation, Key = real/Wishing-Well.wav, to outFile = /home/hadoop/tmp/Wishing-Well.wav
Audio data with id BlackSabbath-Wishing-Well inserted into audio_table.
Audio Metadata for audio data with id BlackSabbath-Wishing-Well inserted into audio_table.
Track Metadata for audio data with id BlackSabbath-Wishing-Well inserted into audio_table.

"""