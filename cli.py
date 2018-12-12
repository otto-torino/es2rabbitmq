import argparse
import sys

import pika
from dateutil.parser import parse
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

from settings import ES, RBMQ

try:
    import builtins
except ImportError:
    from future import builtins
if sys.version_info[0] < 3:
    ConnectionError = OSError

parser = argparse.ArgumentParser(
    description='Enqueues all documents back to given date to RabbitMQ')
parser.add_argument(
    "-d",
    "--date",
    dest="from_date",
    required=True,
    help="enqueue back to this date, string format, parsed by python-dateutil")

args = parser.parse_args()

try:
    # rabbitmq connection
    conn = pika.BlockingConnection(
        pika.ConnectionParameters(RBMQ.get('HOST'), RBMQ.get('PORT')))
    queue_name = RBMQ.get('QUEUE')
    channel = conn.channel()
    channel.queue_declare(queue=queue_name, durable=True)  # idempotent!
# elasticsearch connection
    es = Elasticsearch(
        [ES.get('HOST')],
        http_auth=(ES.get('USERNAME'), ES.get('SECRET')),
        port=ES.get('PORT'),
        use_ssl=False,
        verify_certs=False,
    )
    index_current = ES.get('INDEX')
    date = parse(args.from_date)
    query = {
        'bool': {
            'filter': {
                'range': {
                    'date_publish': {
                        'gte': date.strftime("%Y-%m-%d %H:%M:%S")
                    }
                }
            }
        }
    }

    confirm = False
    total = es.count(
        index=index_current, doc_type='article', body={'query': query})

    print("""
    Enqueue docs:
    %d documents will be enqueued from %s!
    """ % (total.get('count'), str(date)))

    if not confirm:
        confirm = 'yes' in builtins.input("""
    Do you really want to do this? Write 'yes' to confirm: {yes}""".format(
            yes='yes' if confirm else ''))

    if not confirm:
        print("Did not type yes. Thus aborting.\n")
        sys.exit(1)

    print("\nEnqueuing...")
# es query
    request = scan(
        es, query={
            'query': query,
            '_source': [
                'url',
            ]
        }, index=index_current)
    for r in request:
        # append to queue
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=r.get('_id'),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))
    print("Done!")
except Exception as error:
    sys.stderr.write("Error: %s\n" % error)
    sys.exit(1)
