import tqdm
import chromadb

client = chromadb.PersistentClient(path='database/')
collections = client.list_collections()
collection_exists = False

if ('it_threat' not in [coll.name for coll in collections]):
    collection = client.create_collection(name='it_threat')
else:
    collection_exists = True
    collection = client.get_collection(name='it_threat')

#store the data to the database
def store_data(data) -> bool:
    ids, embeddings = data
    print("Storing data embeddings into database....")
    #if collection already exists do not insert again
    if collection_exists:
        print("Collection already exists....")
        return True
    
    # creating batches of the data to insert into the vector database
    batch_size = 2000
    num_batches = len(ids) // batch_size

    # trim the data
    ids = ids[num_batches * batch_size : ]
    embeddings = embeddings[num_batches * batch_size : ]

    # Add collection to the database in batches
    for i in tqdm(range(0, len(ids), batch_size), total=len(ids)):
        collection.add(
            embeddings=embeddings[i:i+batch_size], ids=ids[i:i+batch_size])
    
    return True

#fetch the query
def fetch_query(query_embedding: list[list], n_results: int):
    result = collection.query(
        query_embeddings=query_embedding, n_results=n_results)
    return result
