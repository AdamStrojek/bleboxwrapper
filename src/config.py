import configargparse


def generate_config():
    parser = configargparse.ArgParser('bleboxwrapper', default_config_files=['~/.bleboxwrapper'])

    mqtt_group = parser.add_argument_group('MQTT', 'MQTT Server settings')

    mqtt_group.add_argument('-h', '--mqtt-host', required=True, help="MQTT Host address", env_var='MQTT_HOST')
    mqtt_group.add_argument('-p', '--mqtt-port', default=1883, type=int, help="MQTT Port", env_var='MQTT_PORT')

    mqtt_group.add_argument('--mqtt-client-id', default='BleBox Wrapper', help="MQTT Client ID", env_var='MQTT_CLIENT_ID')
    mqtt_group.add_argument('--mqtt-topic-id', default='blebox', help="MQTT topic ID used by subscription", env_var='MQTT_TOPIC_ID')

    parser.add_argument('-b', '--blebox-address', help="Address to BleBox device", env_var='BLEBOX_ADDRESS')
    parser.add_argument('-v', '--verbose', help="Versbose mode", action='count', env_var='VERBOSE')

    return parser
