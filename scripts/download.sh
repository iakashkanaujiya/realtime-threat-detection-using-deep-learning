#!/bin/bash
dataset_dir="datasets/"
echo "Prepraing to download the dataset..."

dataset_urls=(
    "https://cse-cic-ids2018.s3.ca-central-1.amazonaws.com/Processed%20Traffic%20Data%20for%20ML%20Algorithms/Thursday-22-02-2018_TrafficForML_CICFlowMeter.csv"
    "https://cse-cic-ids2018.s3.ca-central-1.amazonaws.com/Processed%20Traffic%20Data%20for%20ML%20Algorithms/Friday-23-02-2018_TrafficForML_CICFlowMeter.csv"
)

if [ -d "$dataset_dir" ]; then
    echo "Dataset already downloaded"
else
    echo "Downloading training dataset..."
    wget -q --show-progress -O "training_dataset.csv" ${dataset_urls[0]}
    echo "Downloading testing dataset..."
    wget -q --show-progress -O "testing_dataset.csv" ${dataset_urls[1]}
    echo "Download Success!"
fi

model_dir="it_threat_model/"
echo "Prepraing to download the Tensorflow prtrained Model..."

if [ -d "$model_dir" ]; then
    echo "Model already downloaded"
else
    wget -q --show-progress -O model.zip "https://drive.google.com/uc?export=download&id=1ahr5dYlhuxS56M6helUFI0yIxxIoFk9o"
    echo "Unzipping the model.zip"
    unzip -q model.zip
    echo "Deleting model.zip file"
    rm -rf model.zip
fi

echo "Success!"






