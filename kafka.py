import time
import json
import pandas as pd
from confluent_kafka import Producer, Consumer, KafkaError
from utils.data_prepare import generate_embeddings
from utils.chroma import fetch_query

# Create a topic
bootstrap_servers = 'localhost:9092'
topic = 'threat-scan'

# prodcuer
def delivery_report(err, msg):
    """Delivery report callback called on producing messages."""
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(
            msg.topic(), msg.partition()))


def produce_message(bootstrap_servers, topic, messages):
    """Produce a message to the Kafka topic."""
    producer_conf = {'bootstrap.servers': bootstrap_servers}
    producer = Producer(producer_conf)

    try:
        # Produce message to the specified topic
        for message in messages:
            producer.produce(topic, value=json.dumps(
                message), callback=delivery_report)
            producer.poll(1)
            time.sleep(1)

        # Wait for any outstanding messages to be delivered and delivery reports received
        producer.flush()
    except Exception as e:
        print('Error producing message: {}'.format(str(e)))
    finally:
        producer.flush()  # Make sure any outstanding messages are delivered
        producer.poll(1)  # Give it a little time to deliver messages if any

# consumer
def consume_messages(bootstrap_servers, group_id, topics):
    """Consume messages from the specified topics."""
    consumer_conf = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': group_id,
        # Start consuming from the beginning of the topic if no offset is stored
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(consumer_conf)

    # Subscribe to topics
    consumer.subscribe(topics)

    try:
        while True:
            # Poll for messages
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event - not an error
                    continue
                else:
                    print('Error: {}'.format(msg.error()))
                    break

            # Print the received message value
            value = json.loads(msg.value())[:-1]
            _ , embeddings = generate_embeddings(value)
            result = fetch_query(embeddings, 1)

            if (result['ids'][0][0][:3] != 'Ben'):
                print('\033[31mSystem is at risk 💀 \n {}\033[0m'.format(result))
                print('\n')
            else:
                print('\033[32mSystem is safe ✅ \033[0m')
                print('\n')

            time.sleep(1)

    except KeyboardInterrupt:
        print("KeyboardInterrupt: Stopping the consumer...")
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()
