
import atexit
import threading
import time

import toml

import olibox_core.olibox_core.core_modules as mod
import olibox_core.olibox_core.olibox_pkg as pkg

# load user input

print('Welcome to OLIBOX Core v0.1!')
print('Authors: Muhammad Yahya & Felix Förster @ OLI Systems 2020')
print('Contact: github.com/olisystems')
print('info@my-oli.com')


def init():
    pkg.init()


def read_modbusTCP():
    # get modbus reading code from modbus module and save information into either a .txt file OR a python variable
    # values from config.toml: modbus_ip, modbus_registers,
    # return
    pass


def read_ir():
    # get modbus reading code from modbus module and save information into either a .txt file OR a python variable
    # values from config.toml: impulse_rate
    # return
    pass


def read_restful():
    # get modbus reading code from modbus module and save information into either a .txt file OR a python variable
    # values from config.toml: restful_ip, restful_port, username, password, path
    # return
    pass


def connect_mqtt():
    client = pkg.config_mqtt()
    return client


def send_mqtt_power():
    pkg.mqtt_power()


def send_mqtt_energy():
    pkg.mqtt_energy()


def write_restapi_data():
    pkg.write_restapi_values()


@atexit.register
def main():
    connect_mqtt()

    x = threading.Thread(target=send_mqtt_power, args=())
    y = threading.Thread(target=send_mqtt_energy, args=())
    z = threading.Thread(target=write_restapi_data, args=())
    print('1st done')

    x.start()
    y.start()
    z.start()
    print('2nd done')
    pkg.main_ir()


if __name__ == '__main__':
    init()
