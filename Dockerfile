FROM pypy:2-6.0.0-slim

ADD . /app
WORKDIR /app

RUN pypy setup.py install

ENTRYPOINT ["iqfeed"]
