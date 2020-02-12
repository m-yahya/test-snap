import datetime
import json
import time

import click

from .environments import *
from .write_json import write_values

# click helper function to prompt for Ethereum


def prompt_ethereum(ctx, param, use_ethereum):
    rpc_endpoint = 'localhost'
    rpc_port = 8545
    if use_ethereum:
        rpc_endpoint = click.prompt(
            'Ethereum Client RPC Endpoint', default='localhost')
        rpc_port = click.prompt('Ethereum Client RPC Port', default=8545)
    print("For further specifications (ABI, contract address ...) please modify ethereum.py!")
    return (use_ethereum, rpc_endpoint, rpc_port)

# click helper function to prompt for modbus


def prompt_modbus(ctx, param, use_modbus_tcp):
    modbus_server_ip = False
    modbus_server_port = False
    modbus_server_energy_demand_register = False
    modbus_server_power_demand_register = False
    modbus_server_energy_supply_register = False
    modbus_server_power_supply_register = False

    if use_modbus_tcp:
        modbus_server_ip = click.prompt('enter modbus server ip')
        modbus_server_port = click.prompt('enter modbus server port')
        modbus_server_energy_demand_register = click.prompt(
            'energy demand register')
        modbus_server_power_demand_register = click.prompt(
            'power demand register')
        modbus_server_energy_supply_register = click.prompt(
            'energy supply register')
        modbus_server_power_supply_register = click.prompt(
            'power supply register')
    return (use_modbus_tcp, modbus_server_ip, modbus_server_port, modbus_server_energy_demand_register,
            modbus_server_power_demand_register, modbus_server_energy_supply_register, modbus_server_power_supply_register)

# click helper function to prompt for ir


def prompt_ir_impulse(ctx, param, use_ir):
    ir_impulse_rate = 10000
    power_writing_interval = 3
    energy_writing_interval = 900
    if use_ir:
        ir_impulse_rate = click.prompt('enter IR impulse rate', default=10000)
        power_writing_interval = click.prompt(
            'enter time (sec) for writing power values', default=3)
        energy_writing_interval = click.prompt(
            'enter time (sec) for writing energy values', default=900)
    return (use_ir, ir_impulse_rate, power_writing_interval, energy_writing_interval)

# quarter time check


def is_quarter():
    min = datetime.datetime.utcnow().replace(microsecond=0).minute

    if min == 00 or min == 15 or min == 30 or min == 45:
        return True
    else:
        return False

# mqtt publish


def mqtt_publish(client, file):
    prefix = f'{project_id.upper()}/OLI_{oli_box_id}/{device_type.upper()}'

    with open(file) as f:
        data = json.load(f)
        keys = data.keys()

        for key in keys:
            # get the last name & capitalize it
            last = key.split('_').pop().capitalize()
            # split the name and remove last
            key_list = key.split('_')
            key_list.pop()
            # empty place holder to append key_list items
            strl = ''
            for el in key_list:
                strl += el + '/'

            suffix = f'{strl}{last}'
            topic = f'{prefix}/{suffix}'

            # retrieve value to send
            value = data[key]
            payload_key = suffix.replace('/', '')

            payload = {'timestamp': int(
                round(time.time()*1000)), payload_key: int(value)}
            payload = json.dumps(payload)
            client.publish(topic,
                           payload=payload)
            print(f"Done publishing {payload_key}")

# function to run in exception


def mqtt_reconnect():
    time.sleep(10)
    client.paho.Client(client_id)
    client.username_pw_set(mqtt_username, mqtt_password)
    client.tls_set(ssl_cert_path)
    client.connect(mqtt_broker_ip, mqtt_broker_port)


# send rest api energy values at quarter time
def write_quarter_energy(key, is_sent, energy, clear_energy, calculated_energy):
    # check quarter time to write energy values
    if is_quarter() is True:
        # check if energy is not already sent for the quarter time
        if is_sent is False:
            print("Writing Energy Value to at quarter-time .json")
            is_sent = True
            payload_energy = {key: energy}
            write_values('energy-data.json', payload_energy)
        # reset energy in quarter time after write
        elif clear_energy is True:
            clear_energy = False
            energy = calculated_energy
        # sum energy after write and reset
        else:
            energy += calculated_energy

    else:
        # reset flags
        if is_sent is True and clear_energy is False:
            is_sent = False
            clear_energy = True
            energy += calculated_energy
        else:
            energy += calculated_energy
    return is_sent, energy, clear_energy
