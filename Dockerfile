FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add python3-dev gcc libc-dev libffi-dev openssl curl

COPY . /opt/mtls/
WORKDIR /opt/mtls/


RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r /opt/mtls/requirements.txt

RUN chmod +x /opt/mtls/docker-entrypoint.sh

#RUN touch /opt/mtls/logs/debug.log

EXPOSE 5000
ENTRYPOINT ["/opt/mtls/docker-entrypoint.sh"]
