FROM python:3.9-slim as base
RUN mkdir /install
WORKDIR /install
COPY ./requirements.txt /requirements.txt
RUN pip install --prefix=/install -r /requirements.txt

FROM python:3.9-slim as builder
COPY ./app /app
COPY ./setup.py ./

RUN python setup.py bdist_egg --exclude-source-files -k -b build/dist

RUN cp -v ./app/prod.env build/dist/app
RUN cp -v ./app/logging.conf build/dist/app
RUN cp -rv ./app/api build/dist/app/api

COPY version.txt build/dist/app

FROM python:3.9-slim

RUN mkdir app

RUN apt-get update
RUN apt-get install -y vim

EXPOSE 8000

COPY --from=base /install /usr/local
COPY --from=builder /build/dist/app /app

ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000","--env-file", "/app/prod.env"]






