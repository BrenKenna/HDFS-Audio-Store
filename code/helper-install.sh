#!/bin/bash

set -ex 

# Install core packages: Audio Validation
sudo yum install -y libsndfile.x86_64 libsndfile-utils.x86_64 libsndfile-devel.x86_64 nfs-utils
sudo pip3 install --target "/usr/lib/python3.7/site-packages/" pysoundfile
sudo pip3 install --target "/usr/lib/python3.7/site-packages/" librosa matplotlib numpy pandas scikit-learn
sudo pip3 install --target "/usr/lib/python3.7/site-packages/" boto3
cd /usr/local/lib/python3.7/site-packages/ && sudo rm -fr dateutil/

# Install the audioValidator
sudo yum install -y git
git clone --recursive https://github.com/BrenKenna/audioValidation.git
cd audioValidation
rm -fr Figs/ spark-emr/ helper.sh README.md links.txt
sudo mv audioValidator/ /usr/lib/python3.7/site-packages/


# Install core packages: HDFS Audio Store
sudo pip3 install --target "/usr/lib/python3.7/site-packages/" pyarrow
sudo pip3 install --target "/usr/lib/python3.7/site-packages/" pyaudio
sudo pip3 install --target "/usr/lib/python3.7/site-packages/" wave
sudo pip3 install --target "/usr/lib/python3.7/site-packages/" pyhive
sudo pip3 install --target "/usr/lib/python3.7/site-packages/"
sudo pip3 install --target "/usr/lib/python3.7/site-packages/"
sudo pip3 install --target "/usr/lib/python3.7/site-packages/"
sudo pip3 install --target "/usr/lib/python3.7/site-packages/"


# Install the hdfs audio store
git clone --recursive https://github.com/BrenKenna/hdfs-audio-store.git
sudo mv hdfs-audio-store/ /usr/lib/python3.7/site-packages/


python --version
pip3 --version