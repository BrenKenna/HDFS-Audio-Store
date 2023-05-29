#!/bin/bash

set -ex 

# Install core packages: Audio Validation
WORKDIR=$(pwd)
sudo yum -y install gcc-c++
sudo yum install -y python3-devel.x86_64
sudo pip3 install --upgrade pip
sudo yum install -y libsndfile.x86_64 libsndfile-utils.x86_64 libsndfile-devel.x86_64 nfs-utils
sudo pip3 install --target "/usr/lib/python3.7/site-packages/" pysoundfile
sudo pip3 install --target "/usr/lib/python3.7/site-packages/" librosa matplotlib numpy pandas scikit-learn
sudo pip3 install --target "/usr/lib/python3.7/site-packages/" boto3
cd /usr/local/lib/python3.7/site-packages/ && sudo rm -fr dateutil/

# Install the audioValidator
cd $WORKDIR
sudo yum install -y git
git clone --recursive https://github.com/BrenKenna/audioValidation.git
cd audioValidation
rm -fr Figs/ spark-emr/ helper.sh README.md links.txt
sudo mv audioValidator/ /usr/lib/python3.7/site-packages/


# Install core packages: HDFS Audio Store
sudo pip3 install --target "/usr/lib/python3.7/site-packages/" pyarrow

# Dropped because its used by hdfs client, have librosa
# sudo pip3 install --target "/usr/lib/python3.7/site-packages/" pyaudio
sudo pip3 install --target "/usr/lib/python3.7/site-packages/" wave
sudo pip3 install --target "/usr/lib/python3.7/site-packages/" pyhive
sudo pip3 install --target "/usr/lib/python3.7/site-packages/" typing
sudo pip3 install --target "/usr/lib/python3.7/site-packages/" happybase


# Install the hdfs audio store
git clone --recursive https://github.com/BrenKenna/hdfs-audio-store.git
sudo mv hdfs-audio-store/ /usr/lib/python3.7/site-packages/
sudo mv /usr/lib/python3.7/site-packages/hdfs-audio-store/code /usr/lib/python3.7/site-packages/HdfsAudioStore


# Revert to older urlib3
cd /usr/lib/python3.7/site-packages/
sudo rm -fr urllib*
sudo /usr/bin/pip3 install "urllib3>=1.26.0,<2.0.0"
python --version
pip3 --version