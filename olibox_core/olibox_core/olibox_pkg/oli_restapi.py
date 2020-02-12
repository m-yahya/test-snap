
import datetime
#import urllib.request
import json
import time
import urllib

from .environments import (market_type, oli_restapi_ip, oli_restapi_port,
                           oli_restapi_query, oli_restapi_read_interval)
from .helpers import is_quarter, write_quarter_energy
from .write_json import write_values

#import paho.mqtt.publish as publish


# hardcoded?
url = f'http://{oli_restapi_ip}:{oli_restapi_port}{oli_restapi_query}'
# http://10.1.10.126:1080/api/all/current/now


def connect_restapi():

    try:
        print('Calling Rest API ...')
        raw_res = urllib.request.urlopen(url)
        response = json.load(raw_res)

        res_value = 0
        for dataset in response['datasets']:
            for phase in dataset['phases']:
                for value in phase['values']:
                    res_value += value['data']
        if res_value < 0:
            res_value = 0
            print(res_value)

        print(res_value)
        return(res_value)
    except:
        print(
            f"There was an error reading out the Rest API. Trying again in {oli_restapi_read_interval} seconds...")
        raw_res = urllib.request.urlopen(url)
        response = json.load(raw_res)


def write_restapi_values():
    # Please input your parsing process here
    energy = 0
    clear_energy = True
    is_sent = False

    while True:
        time.sleep(int(oli_restapi_read_interval))
        print(f'connected with {oli_restapi_ip}')
        res_value = connect_restapi()
        # highly custom! we are reading out current! p=V*I, 0.16475 and 300 are offset values!
        power = res_value
        # also dependent on oli_restapi_read_interval: res_value/(oli_restapi_read_interval/3600)
        calculated_energy = res_value/1200
        if res_value > 0:
            power = res_value
        print('Current Energy Value: ' + str(energy) + ' Wh')
        print('Current Power Value:  ' + str(power) + ' W')
        if market_type.lower() == 'consumer':
            print('market type is consumer')

            # write power values
            payload_power = {'activePower_demand': power}
            write_values('power-data.json', payload_power)

            # check quarter time to write energy values
            is_sent, energy, clear_energy = write_quarter_energy('activeEnergy_demand',
                                                                 is_sent, energy, clear_energy, calculated_energy)

        elif market_type.lower() == 'producer':
            print('market type is producer')

            # write power values
            payload_power = {'activePower_supply': power}
            write_values('power-data.json', payload_power)

            # check quarter time to write energy values
            is_sent, energy, clear_energy = write_quarter_energy('activeEnergy_supply',
                                                                 is_sent, energy, clear_energy, calculated_energy)
