 ps -ef|grep flower |grep -v grep |awk '{print $2}' |xargs kill -9

