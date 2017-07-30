flower -A spider.task.workers --logging=info
celery -A spider.task.workers worker -Q login_queue,crawl_history_queue,search_keyword_queue -l info -c 1

