ps -ef|grep 'python manage.py runserver'|grep -v grep|awk '{print $2}'|xargs kill -9
