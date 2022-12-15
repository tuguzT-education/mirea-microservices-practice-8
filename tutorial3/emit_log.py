import pika
import sys


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    message = ' '.join(sys.argv[1:]) or 'info: Hello World!'
    channel.basic_publish(exchange='logs', routing_key='', body=bytes(message, 'utf8'))
    print(f' [x] Sent {message!r}')
    connection.close()


if __name__ == '__main__':
    main()
