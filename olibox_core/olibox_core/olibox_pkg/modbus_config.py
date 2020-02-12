from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

modbus_client = ModbusTcpClient('localhost', port=5020)
connection = modbus_client.connect()

# Read the modbus power function


def readPower():
    try:
        requestP = modbus_client.read_holding_registers(10, 2, unit=1)
        print(requestP.registers)
        power_demand = requestP.registers[0]
        power_supply = requestP.registers[1]
    except Exception as ex:
        # logger.exception("READPOWER Exception")
        print(ex)
        print("Exception in Modbus Reading")
        requestP = modbus_client.read_holding_registers(10, 2, unit=1)
        power_demand = requestP.registers[0]
        power_supply = requestP.registers[1]
    return power_demand, power_supply

# Read the modbus energy function


def readEnergy():
    try:
        requestE = modbus_client.read_holding_registers(20, 2, unit=1)
        print(requestE.registers)
        energy_demand = requestE.registers[0]
        energy_supply = requestE.registers[1]
    except Exception as ex:
        # logger.exception("READENERGY Exception")
        print(ex)
        print("Exception in Modbus Reading")
        requestE = modbus_client.read_holding_registers(20, 2, unit=1)
        energy_demand = requestE.registers[0]
        energy_supply = requestE.registers[1]
    return energy_demand, energy_supply


# Write new output level to modbus register


def writeOutputLevel(event_value):
    try:
        writeO = modbus_client.write_register(40, event_value, unit=1)
        print(writeO)
        # print(writeO.registers)
    except Exception as ex:
        # logger.exception("WRITEOUPUTLEVEL Exception")
        print(ex)
        print("Exception in ModbusReading")
    return event_value
