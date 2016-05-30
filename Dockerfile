FROM python:2.7
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt 
ADD . /code/
CMD python monu/mdb/install_data.py
CMD python httpd
