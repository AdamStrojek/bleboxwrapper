import os
import logging

import paho.mqtt.client as mqtt
import requests


logger = logging.getLogger('bleboxwrapper')

VERBOSE = os.environ.get('VERBOSE', 0)
VERBOSE = VERBOSE in (1, True, 'on', 'yes', 'true', 'y', '1')


def info(text):
    print(text)

if VERBOSE:
    logger.setLevel(logging.DEBUG)

    def debug(text):
        print(text)
else:
    logger.setLevel(logging.INFO)

    def debug(text):
        pass


MQTT_SERVER = os.environ.get('MQTT_SERVER', None)
MQTT_PORT = os.environ.get('MQTT_PORT', '1883')

MQTT_CLIENT_ID = os.environ.get('MQTT_CLIENT_ID', 'BleBox Wrapper')
MQTT_TOPIC_ID = os.environ.get('MQTT_TOPIC_ID', 'blebox')

BLEBOX_ADDRESS = os.environ.get('BLEBOX_ADDRESS', None)


conf_error = False

if not MQTT_SERVER:
    logger.error("MQTT_SERVER is required")
    conf_error = True

try:
    MQTT_PORT = int(MQTT_PORT)
except TypeError:
    logger.error("MQTT_PORT need to be integer")
    conf_error = True

if not BLEBOX_ADDRESS:
    logger.error("BLEBOX_ADDRESS is required")
    conf_error = True

if conf_error:
    exit(1)


topic_subscribe = "cmnd/{topic_id}/power".format(topic_id=MQTT_TOPIC_ID)
topic_publish = "stat/{topic_id}/power".format(topic_id=MQTT_TOPIC_ID)

debug("Topic subscribe: {}".format(topic_subscribe))
debug("Topic publish: {}".format(topic_publish))

blebox_url_base = 'http://{blebox_address}/{{cmd}}'.format(blebox_address=BLEBOX_ADDRESS)
blebox_url = {
    b'on': blebox_url_base.format(cmd='s/1'),
    b'off': blebox_url_base.format(cmd='s/0'),
    b'toggle': blebox_url_base.format(cmd='s/'),
}

info("Blebox Wrapper")
info("Device IP: {}".format(BLEBOX_ADDRESS))
info("Starting...")

response = requests.get(blebox_url_base.format(cmd='api/device/state'))
response.raise_for_status()

data = response.json()
blebox_name = data['device']['deviceName']
blebox_type = data['device']['type']
info("Connected to Blebox: {0}".format(blebox_name))
debug(response.content)

if blebox_type != "switchBox":
    logger.error("Currently only switchBox is supported")
    exit(2)


# The callback for when a subscribed message is received from the server.
def on_command(client, userdata, msg):
    info("Power state change requested to {}".format(msg.payload))
    response = requests.get(blebox_url[msg.payload])
    if response.ok:
        data = response.json()
        debug(response.content)
        state = {
            0: 'off',
            1: 'on',
        }[data[0]['state']]
        client.publish(topic_publish, payload=state)
    else:
        logger.error("Problem during sending command")


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    info("Connected to MQTT server")

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic_subscribe)


def on_message(client, userdata, msg):
    info("Some unsupported message {}".format(msg.topic))


client = mqtt.Client(client_id=MQTT_CLIENT_ID)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, MQTT_PORT)
client.message_callback_add(topic_subscribe, on_command)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
