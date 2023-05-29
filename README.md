  

# HDFS Audio Store

Tinkering with storing audio data in hadoop DBs

  

## Problem

Audio files themselves <20MB, meaning storing them directly on HDFS creates small file problem.

  

Additionally, storing WAVs on S3 means they have to be fetched & opened in order to be analyzed.

  

Why not just store them as objects which holds audio signal, and meta data about them inside a database which uses optimized file formats (i.e row/columnar).

  

Storing audio in slices, means that samples can be fetched as needed. Long-term rational is that these slices could then be annotated with some sort of sentiment; genre, etc. Through ML pipeline for instance.

  

## Image

1). Client posts Audio to S3 bucket.

2). Audio files are then fetched by say spark job, which processes & imports into a HDP DB.

3). Client can fetch audio data stored in DB, and return original WAV.

  

## Model

A Track is the model of data to be imported. Composed of an 3 model objects.

  

1). Audio - Holds byte array, later map of byte array chunked by units of time mapped by sampling rate.

2). TrackMetaData - Holds metadata about the track such as name, owner, size, etc.

3). AudioMetaData - Holds metadata about the audio signal such as frame count, sampling rate, duration etc.

  
  

## Supporting

  

1). AudioFactory - Constructing model objects.

2). AudioHandler - Handles audio data as files, numpy conversions.

3). Workers - Ties fetching audio, with the AudioHandler and AudioFactory.

  

## Active/Outstanding

1). Testing DatabaseWorker.

2). Exceptions.

3). Logger.
