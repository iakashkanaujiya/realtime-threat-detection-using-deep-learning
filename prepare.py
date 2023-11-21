import sys
from toolz import pipe
from utils.data_prepare import prepare_data, generate_embeddings
from utils.chroma import store_data

if __name__ == '__main__':
    if len(sys.argv) > 2:
        datasets = [sys.argv[1], sys.argv[2]]
    else:
        datasets = ['training_dataset.csv', 'testing_dataset.csv']
    
    # creating a pipline
    result = pipe(
        datasets,
        prepare_data,
        generate_embeddings,
        store_data
    )

    if result == True:
        print("Success!")
        print("System is ready for testing...")
