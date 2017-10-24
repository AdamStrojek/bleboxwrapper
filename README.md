# Blebox Wrapper

Simple wrapper for BleBox WiFi switches that allow control them using MQTT server. MQTT communication was created based
on topics used in Sonoff-Tasmota firmware for Sonoff switches.

## Suported devices

Currently this devices are supported:

- BleBox switchBox

## Planned features

- [ ] Support for BleBox switchBoxD
- [ ] Check periodically for current switch status and publish it on MQTT server


## Configuration

Whole configuration for wrapper is made base on environment variables. Available options:

- BLEBOX_ADDRESS (*required*) - IP address of BleBox WiFi switch
- MQTT_SERVER (*required*) - IP address or domain of MQTT server
- MQTT_PORT (default: 1883, optional) - port of MQTT server
- MQTT_TOPIC_ID (default: _blebox_, optional) - used in topics that are subscribed by wrapper 
- MQTT_CLIENT_ID (default: _BleBox Wrapper_, optional) - client name for MQTT, important only if you run multiple
 instances of this wrapper


## Requirements

This project was created for Python 3.6. Should work on other version even on 2.7, but this was not tested due to
priority on 3.6 version. All required libraries can be installed via `pip` and are placed in `requirements.txt` file.


## How to install

There are many ways to install this wrapper. Preferred is to use it via [Docker](https://www.docker.com/) containers.
This allowed me to use it on my NAS server from [QNAP](https://www.qnap.com/) using
[Container Station](https://www.qnap.com/solution/container_station/en/).

### Docker
Just type this command in main directory:

```commandline
$ docker build -t bleboxwrapper .
$ docker run -it --rm --name bleboxapp bleboxwrapper
```

## Credits
Author of this project is Adam Strojek
g