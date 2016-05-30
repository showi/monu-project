FROM python:2.7
RUN apt-get update
RUN apt-get install -y mongodb
RUN apt-get clean
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt 
ADD . /code/
CMD sh start.sh
