FROM python:3.6

ADD . /lio-server

WORKDIR /lio-server

EXPOSE 8000

ENV MONGO_URL mongodb://heroku_2wgm4nnk:mo6e6oh9gdvqlmlv8h61uco9ip@ds249583.mlab.com

ENV MONGO_PORT 49583/heroku_2wgm4nnk

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD gunicorn -w 4 app:app --log-level=debug





