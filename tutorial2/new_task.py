import sys

import pika


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

    message = ' '.join(sys.argv[1:]) or 'Hello World!'
    channel.basic_publish(exchange='', routing_key='task_queue', body=bytes(message, 'utf8'),
                          properties=pika.BasicProperties(
                              delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
                          ))
    print(f' [x] Sent {message!r}')
    connection.close()


if __name__ == '__main__':
    main()
