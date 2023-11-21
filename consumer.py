from kafka import consume_messages

# Create a topic
bootstrap_servers = 'localhost:9092'
topic = 'thread-scan'

if __name__ == '__main__':
    consume_messages(bootstrap_servers, 'my-group', [topic])