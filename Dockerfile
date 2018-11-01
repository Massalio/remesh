FROM python:3.6

ADD . /lio-server

WORKDIR /lio-server

EXPOSE 8000

ENV MONGO_URL mongodb://gmerino:fili123@ds149309.mlab.com

ENV MONGO_PORT 49309/heroku_vmdrr8pj

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD gunicorn -w 4 app:app --log-level=debug
