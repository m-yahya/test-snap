try:
    import RPi.GPIO as GPIO
    rpi = True
except:
    rpi = False
    print("Error importing RPi.GPIO!  This module runs only on Raspberry Pi.")

import datetime
import json
import os
import sys
import time

import paho.mqtt.client as mqtt
import toml

import _thread as thread

from .environments import *
from .oli_mqtt import client, config_mqtt
from .write_json import write_values

# Number of pulses used to measure Energy
pulseCount = 0
#Power and Energy
power = 0
elapsedkWh = 0
# Number of pulses per hour
ppwh = int(ir_impulse_rate) / 1000
pulseTime = 0
pulse_pin = 7
bounce = 50
p = 0
e = 0

# write power values to json file


def write_power_values():

    while 1:
        time.sleep(int(power_writing_interval))
        # pload = {datetime.datetime.utcnow().replace(microsecond=0): p}
        power_load = {'activePower_bidirect': p}
        print(f'Power load is {power_load}')
        # save power values
        try:
            write_values('power-data.json', power_load)
        except Exception as e:
            print(e)


temp_value = 0

# write energy values to json file


def write_energy_values():

    global temp_value

    while 1:
        time.sleep(60)
        p_energy = e-temp_value
        energy_load = {'activeEnergy_bidirect': p_energy}
        print(f'Bidirect energy in the last 15 min {energy_load}')
        # save energy values
        try:
            write_values('energy-data.json', energy_load)
            temp_value = e
        except Exception as err:
            print(err)


def eventHandler(channel):
    onPulse(1)


def onPulse(channel):
    global pulseTime
    global pulseCount
    global lastTime
    global e
    global p
    lastTime = pulseTime
    pulseTime = time.time()
    pulseCount += 1
    power = (3600.0/(pulseTime-lastTime))/ppwh
    p = power
    elapsedkWh = (1.0*pulseCount/(ppwh*1000))
    e = elapsedkWh
    print("pulseTime: "+str(pulseTime))
    print("lastTime: "+str(lastTime))
    # lastTime=pulseTime
    print("power: "+str(power))
    print("elapsedkWh: "+str(elapsedkWh))
    # print("PulseTime"+str(pulseTime))
    # print("lastTime"+str(lastTime))
    return elapsedkWh


def main_ir():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pulse_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    thread.start_new_thread(write_power_values, ())
    thread.start_new_thread(write_energy_values, ())
    GPIO.add_event_detect(pulse_pin, GPIO.RISING,
                          callback=eventHandler, bouncetime=bounce)
    while True:
        try:
            if rpi:
                continue
            else:
                onPulse(1)
        except KeyboardInterrupt:
            print("Unable to start threads")
            GPIO.cleanup()
