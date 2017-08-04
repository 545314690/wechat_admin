from spider.config.conf import get_kafka_info

from spider.util.KafkaUtil import MyKafkaProducer

kafka_info = get_kafka_info()
kafka_producer = MyKafkaProducer(kafka_info.get('host'), kafka_info.get('port'),
                                 kafka_info.get('topics').get('topic_wechat'))