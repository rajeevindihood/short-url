FROM python:3.9-slim as base
RUN mkdir /install
WORKDIR /install
COPY ./requirements-prod.txt /requirements.txt
RUN pip install --prefix=/install -r /requirements.txt

FROM python:3.9-slim as builder
COPY ./app /app
COPY ./setup.py ./

RUN python setup.py bdist_egg --exclude-source-files -k -b build/dist
RUN cp -v ./app/logging.conf build/dist/app

COPY version.txt build/dist/app

FROM python:3.9-slim

RUN mkdir app

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 8000

ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

HEALTHCHECK --interval=30s --timeout=30s --start-period=30s --retries=3 \
  CMD curl --fail-with-body localhost:8000/sys/healthcheck

COPY --from=base /install /usr/local
COPY --from=builder /build/dist/app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000","--env-file", "/app/prod.env"]
