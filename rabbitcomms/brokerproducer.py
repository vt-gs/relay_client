import logging
import pika
import json
import time
#from sortedcontainers import SortedDict
from brokerconnector import BrokerConnector

class BrokerProducer(BrokerConnector):
    """BrokerProducer provides basic functionality to support the connection
    needed for a typical Pika to RabbitMQ producer connection.  Individual
    functions could be overridden if alternate or additional functionality is
    desired.  Derived classes would override the "send and/or "publish_message"
    functions.
    """

    def __init__(self, cfg, loggername=None):
        super(BrokerProducer, self).__init__(cfg, loggername)

        self.routing_key = cfg['produce_key']
        self.message_number = 1
        self.app_name = cfg['app_name']

    def on_exchange_declareok(self, frame):
        """Called when the server has finished the creation of the exchange.
        """
        if self.loggername is not None:
            self.logger.debug('Exchange declared successfully')
            self.logger.info('Registering as producer with broker')

    def send(self, msg):
        if self.loggername is not None:
            self.logger.debug('Publishing message bound for "{}"'.format(self.routing_key))

        properties = pika.BasicProperties(app_id=self.app_name,
                                          content_type='application/json')#,
                                          #message_id=id,
                                          #correlation_id=id)
        try:
            self.channel.basic_publish(exchange=self.exchange,
                                       routing_key = self.routing_key,
                                       body = msg,
                                       properties = properties)
        except Exception as e:
            print str(e)
            self.logger.warning('Error with channel.basic_publish()')
            self.logger.warning(str(e))
        #json.dumps(message, ensure_ascii=False),
    def publish_message(self):
        if self.closing:
            return

        if self.delivery_queue:
            # message queue is not empty, send the first (i.e. FIFO) message
            (id, (message,key)) = self.delivery_queue.peekitem(0)



        self.schedule_next_message()

    def stop_producing(self):
        """Tell the broker that we are done and would like to stop producing
        messages.  This will send the Basic.Cancel RPC command and makes a clean
        connection break with the broker.  We'll register a callback that will
        be called when the cancel request is handled.

        IF USING THIS METHOD TO DISCONNECT FROM RMQ SERVER, NOTE THAT THIS
        WILL RECONNECT TO THE RMQ SERVER AFTER A DELAY OF `retry_wait`.  NOT
        RECOMMENDED TO USE THIS METHOD TO CHANGE RMQ SERVERS


        """
        if self.channel:
            if self.loggername is not None:
                self.logger.debug('Stopping Producer')
            self.close_channel()
