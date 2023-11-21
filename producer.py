from kafka import produce_message
import json
import random

# Create a topic
bootstrap_servers = 'localhost:9092'
topic = 'thread-scan'

if __name__ == '__main__':
    try:
        with open('datasets/test_data.json', 'r') as f:
            test_data = json.loads(f.read())
            f.close()
    except FileNotFoundError as e:
        print(e)
        exit(1)
    finally:
        print("You can total {} network request".format(len(test_data)))

        try:
            n_req = int(input(("Enter the number of request you want to generate: ")))
        except Exception as e:
            print("Invalid input, we're taking only 100 requests")
            n_req = 100

        #shuffle the data
        random.shuffle(test_data)
        if n_req > len(test_data): n_req = 100

        #produce message
        produce_message(bootstrap_servers, topic, test_data[:n_req])