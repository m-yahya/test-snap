
import datetime
import json
import os
import sys
import time

import paho.mqtt.client as mqtt
import toml

from .environments import *
from .helpers import is_quarter, mqtt_publish, mqtt_reconnect
from .smartcontract_config import web3_power
from .write_json import read_values

# MQTT basic Functions

# dont touch


def on_log(client, userdata, level, buf):
    print("log: ", buf)

# dont touch


def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected flags"+"result code"+str(rc)+"client_id ")
    client.connected_flag = False

# dont touch


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True
        print("connected OK")
        # client.subscribe("OLI_6/activePower")
    else:
        print("Bad Connection Returned code=", rc)

# dont touch


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


print(oli_box_id)
# making this global because it requires in other functions as well
client_id = f'OLI_{oli_box_id}_PUB'

client = mqtt.Client(client_id)


def config_mqtt():
    print('Configuring MQTT Client and connecting to Broker...')
    mqtt.Client.connected_flag = False

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.on_log = on_log
    client.username_pw_set(mqtt_username, mqtt_password)

    client.tls_set(ssl_cert_path)
    client.loop_start()
    try:
        client.connect(mqtt_broker_ip, int(mqtt_broker_port), keepalive=60)
        while not client.connected_flag:
            print("In wait loop")
            time.sleep(1)
    except Exception as e:
        print(f"Connection Failed {e}")
        sys.exit("quitting")
    print('...done.')
    return client


# touch this! mqtt information inside toml

def mqtt_power():

    while 1:
        time.sleep(int(power_sending_interval))
        # read power data from json file
        file = '../../tmp/power-data.json'
        if os.path.isfile(file) and os.stat(file).st_size != 0:

            try:
                mqtt_publish(client, file)
            except Exception as e:
                print(f"MQTT_POWER Exception {e}")
                # logger.exception("MQTT_POWER Exception")
                mqtt_reconnect()


def mqtt_energy():

    while 1:
        file = '../../tmp/energy-data.json'
        time.sleep(60)
        if os.path.isfile(file) and os.stat(file).st_size != 0:

            try:
                if is_quarter() is True:
                    mqtt_publish(client, file)
            except Exception as e:
                print(f"Socket Error {e}")
                mqtt_reconnect()

    # client.loop_stop()
    # client.disconnect
