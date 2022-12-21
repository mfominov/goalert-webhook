FROM python:3.6.12-slim

ENV FLASK_APP="main.py"

WORKDIR /opt/app

ADD requirements.txt .

RUN apt-get update && \
  apt-get install -y curl && \
  pip3 install -r requirements.txt && \
  rm -rf /var/lib/apt/lists/*

ADD . .

EXPOSE 8080
HEALTHCHECK  --interval=5m --timeout=3s \
  CMD curl --fail http://localhost:8080/health || exit 1

ENTRYPOINT [ "python", "main.py" ]