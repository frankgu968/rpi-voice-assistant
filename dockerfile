FROM python:alpine

COPY ./requirements.txt .

RUN apk add --no-cache portaudio-dev && \
    apk add --no-cache --virtual .build-deps alpine-sdk linux-headers && \
    pip3 install -r requirements.txt && \
    apk del .build-deps

COPY ./assets /app/assets
COPY ./src /app/src/

WORKDIR /app
ENTRYPOINT [ "python3", "/app/src/main.py" ]