import pika
from typing import Any
from pika.exchange_type import ExchangeType
from pika.adapters.blocking_connection import BlockingChannel


class Rabbit:
    def __init__(self, connection_params: pika.ConnectionParameters):
        self.connection_params = connection_params
        self.message_handlers = []
        self.queues = []

    def channel(self) -> BlockingChannel:
        connection = pika.BlockingConnection(
            self.connection_params)
        channel = connection.channel()
        return channel


    def create_queue(self, queue: Any, passive: bool=False, durable: bool=False, 
                     exclusive: bool=False, auto_delete: bool=False, arguments: Any=None, 
                     exchange: Any=None, routing_key: Any=None, bind_args: Any=None):
        
        res = self.channel().queue_declare(queue, passive, durable, 
                     exclusive, auto_delete, arguments)
        queue_name = res.method.queue
        
        if exchange and routing_key:
            self.channel().queue_bind(queue=queue_name, exchange=exchange, routing_key=routing_key, arguments=bind_args)
        print(f'queue {queue_name} created')
        return queue_name


    def create_exchange(self, exchange: str, exchange_type: ExchangeType|str, passive: bool=False, durable: bool=False, 
                        auto_delete: bool=False, internal: bool=False, arguments=None):
        self.channel().exchange_declare(exchange, exchange_type, passive, durable, 
                        auto_delete, internal, arguments)


    def publish(self, exchange: str, routing_key: str, body: str, properties=None, 
                mandatory: bool=False):
        
        with self.channel() as channel:
            channel.basic_publish(exchange, routing_key, body, properties, mandatory)
            channel.close()
        print('Message was sent')


    def message_handler(self, queue: str, auto_ack: bool=False, exclusive: bool=False, consumer_tag:Any=None, arguments:Any=None,
                        queue_passive: bool=False, queue_durable: bool=False, queue_auto_delete: bool=False, 
                        queue_arguments: Any=None, queue_exclusive: bool=False, queue_exchange: Any=None, 
                        queue_routing_key: Any=None, queue_bind_args: Any=None):
        def decorator(func):
            
            handler = {
                'queue': queue,
                'on_message_callback': func,
                'auto_ack': auto_ack,
                'exclusive': exclusive,
                'consumer_tag': consumer_tag,
                'arguments': arguments
            }

            queue_dict = {
                'queue': queue,
                'passive': queue_passive,
                'durable': queue_durable,
                'auto_delete': queue_auto_delete,
                'exclusive': queue_exclusive,
                'arguments': queue_arguments,
                'exchange': queue_exchange,
                'routing_key': queue_routing_key,
                'bind_args': queue_bind_args
            }

            self.message_handlers.append(handler)
            self.queues.append(queue_dict)

            return func
        return decorator


    def run(self):
        with self.channel() as channel:
            for queue in self.queues:
                self.create_queue(**queue)

            for message_handler in self.message_handlers:
                channel.basic_consume(**message_handler)

            channel.start_consuming()

