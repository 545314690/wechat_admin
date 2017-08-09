# -*- coding: utf-8 -*-
from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import json

from spider.config.conf import get_kafka_conf
from spider.loggers.log import logger

DEFAULT_CONFIG = {
    'value_serializer': lambda v: json.dumps(v).encode('utf-8'),
    'value_deserializer': lambda m: json.loads(m.decode('ascii'))
}

class MyKafkaProducer():
    '''
    使用kafka的生产模块
    '''
    value_serializer = lambda v: json.dumps(v).encode('utf-8')
    # 定义静态变量实例
    __singleton = None

    def __init__(self, host, port, topic, value_serializer=None):
        if (value_serializer == None):
            value_serializer = DEFAULT_CONFIG['value_serializer']
        self.host = host
        self.port = port
        self.topic = topic
        bootstrap_servers = '{host}:{port}'.format(
            host=self.host,
            port=self.port
        )
        self.producer = KafkaProducer(bootstrap_servers = bootstrap_servers, value_serializer=value_serializer)

    def send(self, message):
        try:
            producer = self.producer
            producer.send(self.topic, message)
            producer.flush()
        except KafkaError as e:
            logger.info(e)

    @staticmethod
    def get_instance():
        if MyKafkaProducer.__singleton is None:
            kafka_info = get_kafka_conf()
            kafka_producer = MyKafkaProducer(kafka_info.get('host'), kafka_info.get('port'),
                                             kafka_info.get('topics').get('topic_wechat'))
            MyKafkaProducer.__singleton = kafka_producer
        return MyKafkaProducer.__singleton


class MyKafkaConsumer():
    '''
    使用Kafka—python的消费模块
    '''

    def __init__(self, host, port, topic, groupid, value_deserializer=None):
        self.host = host
        self.port = port
        self.topic = topic
        self.groupid = groupid
        if (value_deserializer == None):
            value_deserializer = DEFAULT_CONFIG['value_deserializer']
        self.consumer = KafkaConsumer(self.topic, group_id=self.groupid,
                                      bootstrap_servers='{host}:{port}'.format(
                                          host=self.host,
                                          port=self.port), value_deserializer=value_deserializer)

    def consume(self):
        try:
            for message in self.consumer:
                # print json.loads(message.value)
                yield message
        except KeyboardInterrupt as e:
            logger.info(e)


def main():
    '''
    测试consumer和producer
    :return:
    '''
    ##测试生产模块
    # producer = Kafka_producer("127.0.0.1", 9092, "ranktest")
    # for id in range(10):
    #    params = '{abetst}:{null}---'+str(i)
    #    producer.sendjsondata(params)
    ##测试消费模块
    # 消费模块的返回格式为ConsumerRecord(topic=u'ranktest', partition=0, offset=202, timestamp=None,
    # \timestamp_type=None, key=None, value='"{abetst}:{null}---0"', checksum=-1868164195,
    # \serialized_key_size=-1, serialized_value_size=21)
    #
    # kafka_producer = MyKafkaProducer.get_instance()
    #
    # kafka_producer.send({'a': '1111111'})

    # consumer = MyKafkaConsumer('192.168.0.161', 9092, "foobar", 'test-python-ranktest')
    # message = consumer.consume()
    # for i in message:
    #     print(i.value)


# if __name__ == '__main__':
#     main()
