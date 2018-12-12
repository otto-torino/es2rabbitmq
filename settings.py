import os

from dotenv import load_dotenv
load_dotenv()

# Elastic Search
ES = {
    'HOST': os.getenv('ES_HOST', 'localhost'),
    'PORT': os.getenv('ES_PORT', 9200),
    'INDEX': os.getenv('ES_INDEX', None),
    'USERNAME': os.getenv('ES_USERNAME', None),
    'SECRET': os.getenv('ES_SECRET', None)
}

# RabbitMQ
RBMQ = {
    'HOST': os.getenv('RBMQ_HOST', 'localhost'),
    'PORT': os.getenv('RBMQ_PORT', 5672),
    'QUEUE': os.getenv('RBMQ_QUEUE', None)
}
