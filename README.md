# HDFS Audio Store
Tinkering with storing audio data in hadoop DBs


## Problem
Audio files themselves <64MB, meaning storing them on HDF creates small file problem.
Additionally, storing WAVs on S3 means they have to be fetched & opened in order to be analyzed.
Why not just store them as objects which holds audio signal, and meta data about them.
Storing audio in slices, means that samples can be fetched as needed.
Also opens up annotating those slices if required.


## Image
1). Client posts Audio to S3 bucket.
2). Audio is fetched by say spark job, which processes & imports into a HDP DB
3). Client can fetch audio data stored in DB, or S3 if un-processed.


## Model
A Track is the model of data to be imported. Composed of an 3 model objects.
1). Audio - Holds byte array, later map of byte array chunked by units of time mapped by sampling rate.
2). TrackMetaData - Holds metadata about the track such as name, owner, size, etc.
3). AudioMetaData - Holds metadata about the audio signal such as frame count, sampling rate, duration etc.