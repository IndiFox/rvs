FROM ubuntu:latest
LABEL maintainer="Alexander Marchuk"
RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential gunicorn
COPY . /app
WORKDIR /app 
RUN pip3 install -r requirements.txt

EXPOSE 5000
RUN chmod +x boot.sh
ENTRYPOINT ["./boot.sh"]