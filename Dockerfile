FROM python:3.6-alpine

ARG MQTT_SERVER

ARG BLEBOX_ADDRESS

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV MQTT_SERVER=$MQTT_SERVER BLEBOX_ADDRESS=$BLEBOX_ADDRESS

CMD [ "python3", "./main.py" ]
