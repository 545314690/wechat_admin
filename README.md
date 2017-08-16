# wechat_admin
#安装SQL-python依赖
sudo apt-get install libmysqlclient-dev
sudo apt-get install python3-dev
flower -A spider.task.workers -l info
celery -A spider.task.workers worker -Q login_queue,crawl_history_queue,search_keyword_queue -l info -c 1 -Ofair

#118上启动节点
celery multi start 118-login -A spider.task.workers -Q login_queue -l info -c 1 -Ofair -n

celery multi start 118-w1 -A spider.task.workers -Q search_keyword_queue,user_list_crawl_queue,wechat_user_crawl_queue,wechat_url_crawl_queue -l info -c 1 -Ofair -n

celery multi start 118-w2 -A spider.task.workers -Q wechat_crawl_queue -l info -c 1 -Ofair -n

#182上启动节点
celery multi start 182-w1 -A spider.task.workers -Q search_keyword_queue,user_list_crawl_queue,wechat_user_crawl_queue,wechat_url_crawl_queue -l info -c 1 -Ofair -n

celery multi start 182-w2 -A spider.task.workers -Q wechat_crawl_queue -l info -c 1 -Ofair -n

celery multi start 182-w3 -A spider.task.workers -Q wechat_crawl_queue -l info -c 1 -Ofair -n
