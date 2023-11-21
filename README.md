# Real Time Threat Detection using Deep Learning

Real Time Threat Detection using Deep Learning, Apache Kafka, and Vector Embedding

## Getting Started

Before starting, ensure that [Zookeeper](https://hub.docker.com/_/zookeeper) and [confluentinc/kafka](https://github.com/confluentinc/confluent-kafka-python) Docker images are installed and running on your system.

### 1. Install Python Dependencies

Download and install the required Python modules:

```bash
pip install -r requirements.txt
```

### 2. Download Dataset and Deep Learning Model

Run the following script to download the necessary dataset files and the Deep Learning Model for generating embeddings:

```bash
bash scripts/download.sh
```

### 3. Prepare the Training and Testing Data

Run the following command to prepare the training and testing data. You can explicitly specify the training and testing datasets, or the system will find them automatically.

This script prepares and cleans the training and testing datasets, storing them in the datasets directory. 

Additionally, the Python script generates vector embeddings for the datasets, storing them in the ChromaDB vector database. Please note that this process may take some time.

```bash
python prepare.py --training training_dataset.csv --testing testing_dataset.csv
```

### 4. Run the Producer

Use `producer.py` to simulate incoming network traffic: This script will simulate the incoming network traffic similar to real network traffic.

```bash
python producer.py
```

### 5. Run the Consumer

Simultaneously run `consumer.py` to log and monitor the incoming network traffic: This script will montior the every network event, and scan them to find the thread on the network.

```bash
python consumer.py
```

## Notes
In this program, an original dataset is employed to generate synthetic network events. This enables the simulation of network traffic flow, allowing for the monitoring and logging of incoming network traffic.