import os
import sys
import time

import pika


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

    # noinspection PyUnusedLocal
    def callback(ch, method, properties, body):
        print(f' [x] Received {body.decode()!r}')
        time.sleep(body.count(b'.'))
        print(' [x] Done')
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            # noinspection PyUnresolvedReferences, PyProtectedMember
            os._exit(0)
