from kombu import Connection, Exchange, Queue, Producer

def send_message(connection_string, payload):
    name = 'celery_sender_queue'
    with Connection(connection_string) as conn:
        with conn.channel() as channel:
            producer = Producer(channel)

            exchange = Exchange(name, type="direct", durable=True)
            queue = Queue(name, exchange=exchange, routing_key=name, durable=True)
            producer.publish(payload, serializer='json',
                             exchange=exchange, routing_key=name, 
                             declare=[exchange, queue])