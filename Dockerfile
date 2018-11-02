FROM python:3.6

ADD . /lio-server

WORKDIR /lio-server

EXPOSE 8000

ENV MONGO_URL mongodb://lioneldagnino:chori?dame20@ds149593.mlab.com

ENV MONGO_PORT 49593/rmm_server

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD gunicorn -w 4 app:app --log-level=debug
