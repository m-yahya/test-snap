# olibox_core
OLI Box Code, Modularized and defined as a snap for ubuntu core

The following modules have to be implemented:

- Main Routine
- MQTT
- Parity
- SSH / remot3.it
- Environmental settings (with user input)
- Various Device Interfacing


# --- 1. Setup/Config ---

## Who am I?
- *OLI_Box_ID (OLI_XX)
- *Project_ID
- *Device_Type

## Where to send Data?
-*MQTT_Broker_IP
-*MQTT_Broker Port
-*MQTT_Broker_SSL (y/n)

## What Data to send?
*activeEnergy Supply/Demand
*activePower Supply/Demand

*activeEnergy sending Interval (default: 900s)
*activePower sending Interval (default: 5s)

## What Data to recieve?
*feedInRate (as an example for PV)	

## What about Blockchain related Information? (experimental!)
- *rpc_port (default: localhost:8545)
- bc_key (default eth.account[0]), use private key! (not user input)
- smart_contract_address1 (not user input)
- smart_contract_abi1 (not user input)
- sending_interval (default: 60s)
- value_to_send (power, energy, input_limit ?)
- smart_contract_function1 (???) do we need to specify or not?
- smart_contract_function2 (???) do we need to specify or not?

- *chain_ID (only for local node)
- *node_Type (Full/Light ...)

## Where to get data from?
- *Modbus TCP/RTU
	- ModbusServerIP
	- Register
	- ...
- *Bluetooth
- *REST_API
	-RestAPI Server
	-...
- *IR_Sensor
	- "blinking_rate"
	- ...
- *D0
......

# --- 2. Function/Modules/Packages ---
## MQTT

- connect to broker
- send Data to Broker ("Publish")
- recieve Data from Broker ("Subscribe")

## BC related functions
 
- start BC Node
- create public-private-keypair
- send transaction
- listen to events

## interfacing

-modbus connect
-modbus readout
-modbus write

-bluetooth connect
-bluetooth readout
-bluetooth write (?)

-restAPI connect
-restAPI readout
-restAPI write

-IR Sensor Readout


DOSE/OLI_22/PV/activeEnergy/Supply
projectID/OLI_ID/deviceType/what data to send?...
DOSE/OLI_35/Meter/.....
DOSE/dfjalsdkfjldskfjölsdfj
DOSE/sfdasdf
DOSE/
DOSE/

# Setup

Install dependencies:
```
pip install -r requirements.txt
```
## Todo

- [x] Add `imports` to `init.py`
- [x] Store user input to file
- [x] Write IR-Sensor values to `json` file