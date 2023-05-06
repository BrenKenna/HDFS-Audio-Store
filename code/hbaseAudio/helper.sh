#!/bin/bash

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