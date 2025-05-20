import pika

from broker.rabbit import Rabbit

connection_params = pika.ConnectionParameters(host='rabbit', 
                                              credentials=pika.PlainCredentials('rabbitmq', 'rabbitmq'), 
                                              connection_attempts=5)
rabbit = Rabbit(connection_params)


