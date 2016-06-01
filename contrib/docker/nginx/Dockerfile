FROM nginx:alpine
RUN mkdir /code
WORKDIR /code
#ADD requirements.txt /code/
#RUN pip install -r requirements.txt 
ADD . /code/
RUN cp /code/etc/nginx/conf.d/monu.conf /etc/nginx/conf.d/monu.conf 
CMD sh start.sh
