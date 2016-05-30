FROM python:2.7
RUN apt-get update
RUN apt-get install -y mongodb
RUN echo "127.0.0.1 db" >> /etc/hosts
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt 
ADD . /code/
CMD sh start.sh
