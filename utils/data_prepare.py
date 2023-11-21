import os
import json
import sys
from tqdm import tqdm
import pandas as pd
import tensorflow.keras.backend as K
from .data_cleanup import cleanData
from .tensorflow_keras import intermediate_layer_model

def prepare_data(datasets):
    if len(datasets) < 2:
        print("Please provide train and test dataset!")
        sys.exit(1)

    train_data = datasets[0]
    test_data = datasets[1]

    print("Prepraing the Dataset...")
    dirs = os.listdir()

    if 'datasets' not in dirs:
        os.makedirs(name='datasets')
        # Clean the data
        cleanData(inFile=train_data, outFile='datasets/cleaned_train_data')
        cleanData(inFile=test_data, outFile='datasets/cleaned_test_data')
    
    #load the dataset
    df = pd.read_csv('datasets/cleaned_train_data.csv')
    test_df = pd.read_csv('datasets/cleaned_test_data.csv')
    test_data = test_df.iloc[len(
        test_df[test_df['Label'] == 'Benign'])-500:].values.tolist()

    print("Saving the test dataset")
    try:
        with open("datasets/test_data.json", 'w') as f:
            f.write(json.dumps(test_data))
            f.close()
    except Exception as e:
        print(e)

    return df

def generate_embeddings(df):
    # seperate ids and embeddings
    ids = []
    embeddings = []

    # generate embeddings
    if type(df) is list:
        model_res = intermediate_layer_model.predict(K.constant([df]))
        for res in model_res:
            embeddings.append(res.tolist())
    else:   
        print("Generating embeddings...")
        model_res = intermediate_layer_model.predict(K.constant(df.iloc[:,:-1]))

        print("Prepraing the embeddings...")
        for i, res in tqdm(zip(df.iterrows(), model_res), total=len(model_res)):
            benign_or_attack = i[1]['Label'][:3]
            ids.append(benign_or_attack + '_' + str(i[0]))
            embeddings.append(res.tolist())

    return ids, embeddings
