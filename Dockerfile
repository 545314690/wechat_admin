FROM python:3.6-slim
VOLUME /app
COPY * /app/
RUN apt-get update && \
    apt-get install libmysqlclient-dev libxml2-dev libxslt1-dev -y && \
    cd /app && \
    pip install --upgrade pip && \
    pip install -r requirements.txt
ENTRYPOINT ["./startup.sh"]
EXPOSE 8000
EXPOSE 5555