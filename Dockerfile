FROM ubuntu:latest

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

RUN pip3 install requests
RUN pip3 install beautifulsoup4
RUN pip3 install -U python-dotenv
RUN pip3 install lxml
RUN pip3 install redis

WORKDIR /home/ubuntu
COPY . /home/ubuntu

# ENTRYPOINT ["python3"]
