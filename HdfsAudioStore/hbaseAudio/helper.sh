#!/bin/bash


##################################################
##################################################
# 
# 1). From Basic
# 
##################################################
##################################################


# start shell
hbase shell

# List table
list

'''
TABLE                                                                                                                                               
audio_table                                                                                                                                         
1 row(s)
Took 0.2887 seconds                                                                                                                                 
=> ["audio_table"]
'''


# Get posted audio
get "audio_table", "audio1"

"""
COLUMN                                 CELL                                                                                                         
 audio:                                timestamp=2023-05-06T13:56:37.010, value=\x01\x02\x03\x04\x05                                                
 metadata:duration                     timestamp=2023-05-06T14:00:47.130, value=10                                                                  
 metadata:end_time                     timestamp=2023-05-06T14:00:47.130, value=20220507140010                                                      
 metadata:sample_rate                  timestamp=2023-05-06T14:00:47.130, value=44100                                                               
 metadata:start_time                   timestamp=2023-05-06T14:00:47.130, value=20220507140005                                                      
 metadata:timestamp                    timestamp=2023-05-06T14:00:47.130, value=20220507140000                                                      
1 row(s)
Took 0.1382 seconds 
"""


# Get audio
get "audio_table", "audio1", { COLUMN => "audio" }

"""
COLUMN                                 CELL                                                                                                         
 audio:                                timestamp=2023-05-06T13:56:37.010, value=\x01\x02\x03\x04\x05                                                
1 row(s)
Took 0.3619 seconds
"""


# Get audio metadata
get "audio_table", "audio1", { COLUMN => "metadata:sample_rate" }
get "audio_table", "audio1", { COLUMN => "metadata" }

"""

COLUMN                                 CELL                                                                                                         
 metadata:sample_rate                  timestamp=2023-05-06T14:00:47.130, value=44100                                                               
1 row(s)
Took 0.0068 seconds

COLUMN                                 CELL                                                                                                         
 metadata:duration                     timestamp=2023-05-06T14:00:47.130, value=10                                                                  
 metadata:end_time                     timestamp=2023-05-06T14:00:47.130, value=20220507140010                                                      
 metadata:sample_rate                  timestamp=2023-05-06T14:00:47.130, value=44100                                                               
 metadata:start_time                   timestamp=2023-05-06T14:00:47.130, value=20220507140005                                                      
 metadata:timestamp                    timestamp=2023-05-06T14:00:47.130, value=20220507140000                                                      
1 row(s)
Took 0.0082 seconds  

"""


##################################################
##################################################
# 
# 2). From Updated
# 
##################################################
##################################################


#
describe "audio_data"
get "audio_data", "TheWhispers-And-the-Beat-Goes-On", { COLUMN => "audio_metadata" }

"""

COLUMN FAMILIES DESCRIPTION                                                                                                                                         
{NAME => 'audio', BLOOMFILTER => 'NONE', IN_MEMORY => 'false', VERSIONS => '1', KEEP_DELETED_CELLS => 'FALSE', DATA_BLOCK_ENCODING => 'NONE', COMPRESSION => 'NONE',
 TTL => 'FOREVER', MIN_VERSIONS => '0', BLOCKCACHE => 'false', BLOCKSIZE => '65536', REPLICATION_SCOPE => '0'}                                                      

{NAME => 'audio_meta', BLOOMFILTER => 'NONE', IN_MEMORY => 'false', VERSIONS => '3', KEEP_DELETED_CELLS => 'FALSE', DATA_BLOCK_ENCODING => 'NONE', COMPRESSION => 'N
ONE', TTL => 'FOREVER', MIN_VERSIONS => '0', BLOCKCACHE => 'false', BLOCKSIZE => '65536', REPLICATION_SCOPE => '0'}                                                 

{NAME => 'track_meta', BLOOMFILTER => 'NONE', IN_MEMORY => 'false', VERSIONS => '3', KEEP_DELETED_CELLS => 'FALSE', DATA_BLOCK_ENCODING => 'NONE', COMPRESSION => 'N
ONE', TTL => 'FOREVER', MIN_VERSIONS => '0', BLOCKCACHE => 'false', BLOCKSIZE => '65536', REPLICATION_SCOPE => '0'}                                                 


COLUMN                                     CELL                                                                                                                     
 audio_meta: Duration                      timestamp=2023-05-30T10:58:37.108, value=405.46                                                                          
 audio_meta: FrameCount                    timestamp=2023-05-30T10:58:37.108, value=8940409                                                                         
 audio_meta: SamplingRate                  timestamp=2023-05-30T10:58:37.108, value=22050                                                                           
1 row(s)
Took 0.0324 seconds

"""

# Drop row
deleteall 'audio_table', "TheWhispers-And-the-Beat-Goes-On"

"""
Took 0.3480 seconds
"""


# Drop table
disable 'audio_data'
drop 'audio_data'

"""
Took 1.1937 seconds
Took 0.3350 seconds
"""