# coding:utf-8
import datetime
import json

import redis

from spider.config.conf import get_redis_args

redis_args = get_redis_args()


class Cookies(object):
    rd_con = redis.StrictRedis(host=redis_args.get('host'), port=redis_args.get('port'),
                               password=redis_args.get('password'), db=redis_args.get('cookies'))

    rd_con_broker = redis.StrictRedis(host=redis_args.get('host'), port=redis_args.get('port'),
                                      password=redis_args.get('password'), db=redis_args.get('broker'))

    @classmethod
    def store_cookies(cls, name, cookies):
        pickled_cookies = json.dumps(
            {'cookies': cookies, 'loginTime': datetime.datetime.now().timestamp()})
        cls.rd_con.hset('account', name, pickled_cookies)
        cls.rd_con.lpush('account_queue', name)

    @classmethod
    def fetch_cookies(cls):
        for i in range(cls.rd_con.llen('account_queue')):
            name = cls.rd_con.rpop('account_queue').decode('utf-8')
            if name:
                j_account = cls.rd_con.hget('account', name)
                if j_account:
                    j_account = j_account.decode('utf-8')
                    cls.rd_con.lpush('account_queue', name)  # 当账号不存在时，这个name也会清除，并取下一个name
                    account = json.loads(j_account)
                    login_time = datetime.datetime.fromtimestamp(account['loginTime'])
                    if datetime.datetime.now() - login_time > datetime.timedelta(hours=12):
                        cls.rd_con.hdel('account', name)
                        continue  # 丢弃这个过期账号,account_queue会在下次访问的时候被清除,这里不清除是因为分布式的关系
                    return name, account['cookies']
            else:
                return None

    @classmethod
    def delete_cookies(cls, name):
        cls.rd_con.hdel('account', name)
        return True

    @classmethod
    def check_login_task(cls):
        if cls.rd_con_broker.llen('login_queue') > 0:
            cls.rd_con_broker.delete('login_queue')


class Urls(object):
    rd_con = redis.StrictRedis(host=redis_args.get('host'), port=redis_args.get('port'),
                               password=redis_args.get('password'), db=redis_args.get('urls'))
    rd_con_2level = redis.StrictRedis(host=redis_args.get('host'), port=redis_args.get('port'),
                                      password=redis_args.get('password'), db=redis_args.get('2level_urls'))

    expires = redis_args.get('expires')

    @classmethod
    def store_crawl_url(cls, url, result):
        cls.rd_con.set(url, result)

    '''
    详情页的去重、失败页面的保存
    '''

    # 保存爬取过的url
    @classmethod
    def store_crawled_url(cls, url, key='crawled_url'):
        cls.rd_con.sadd(key, url)

    # 判断是否爬取过
    @classmethod
    def is_crawled_url(cls, url, key='crawled_url'):
        return cls.rd_con.sismember(key, url)

    # 保存保存失败的url
    @classmethod
    def store_save_failed_url(cls, url, key='crawl_save_failed_url'):
        cls.rd_con.sadd(key, url)

    # 保存爬取失败的url
    @classmethod
    def store_crawl_failed_url(cls, url, key='crawl_failed_url'):
        cls.rd_con.sadd(key, url)

    '''
    二级页面的去重、失败页面的保存
    '''

    # 保存爬取过的url
    # @param value 默认1 . 1 代表爬取成功 , 0 代表爬取失败
    # @param expires 过期时间 . 爬取成功的设置过期时间 ,爬取失败不设置过期时间
    @classmethod
    def store_crawled_2level_url(cls, url, value=1, expires=expires):
        if (value != 1):
            expires = None
        cls.rd_con_2level.set(url, value, ex=expires)

    # 判断是否爬取过
    @classmethod
    def is_crawled_2level_url(cls, url):
        return cls.rd_con_2level.exists(url)


class IdNames(object):
    rd_con = redis.StrictRedis(host=redis_args.get('host'), port=redis_args.get('port'),
                               password=redis_args.get('password'), db=redis_args.get('id_name'))

    @classmethod
    def store_id_name(cls, user_name, user_id):
        cls.rd_con.set(user_name, user_id)

    @classmethod
    def fetch_uid_by_name(cls, user_name):
        user_id = cls.rd_con.get(user_name)
        if user_id:
            return user_id.decode('utf-8')
        return ''
