# es2rabbitmq

A cli script to enqueue ids of Elastic Search documents published after a given date in RabbitMQ

## Usage

Clone the repo, install the requirements, create a `.env` file with all the connection settings and run the cli

	$ git clone https://github.com/otto-torino/es2rabbitmq
	$ cd es2rabbitmq
	$ python3 -m venv .virtualenv
	$ source .virtualenv/bin/activate
	$ pip install -r requirements.txt
	$ vim .env
	$ python cli.py -d AAAA-MM-DD

The `.env` file should contain the following configurations:

	# Elastic Search
	ES_HOST = 'localhost'
	ES_PORT = 9200
	ES_INDEX = 'name_of_the_es_index'
	ES_USERNAME = 'user'
	ES_SECRET = 'password'

	# RabbitMQ
	RBMQ_HOST = 'localhost'
	RBMQ_PORT = 5672
	RBMQ_QUEUE = 'name_of_rabbitmq_queue'

Some default are set:

	# Elastic Search
	ES_HOST = 'localhost'
	ES_PORT = 9200

	# RabbitMQ
	RBMQ_HOST = 'localhost'
	RBMQ_PORT = 5672
