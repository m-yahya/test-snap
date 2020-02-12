import click
import toml

from .helpers import prompt_ethereum, prompt_ir_impulse, prompt_modbus


@click.command()
@click.option('--mqtt-broker-ip', prompt='MQTT broker IP', help='MQTT broker IP')
@click.option('--mqtt-broker-port', prompt='MQTT broker port', help='Mqtt broker port')
@click.option('--ssl-cert-path', prompt='What is the path of the SSL certficate?', default='/etc/ssl/certs/ca-certificates.crt')
@click.option('--mqtt-username', prompt='MQTT username')
@click.option('--mqtt-password', prompt='MQTT password', hide_input=True, confirmation_prompt=True)
@click.option('--send-power-data/--no-power-data', prompt='Do you want to send random power data (for testing purpose)?')
@click.option('--send-energy-data/--no-energy-data', prompt='Do you want to send random energy data (for testing purpose)?')
@click.option('--energy-sending-interval', prompt='What is the interval for sending energy data in seconds?', default=900, help='Active energy sending interval')
@click.option('--power-sending-interval', prompt='What is the interval for sending power data in seconds?', default=5, help='Active power sending interval')
@click.option('--oli-box-id', prompt='oli box id', help='Oli box ID')
@click.option('--project-id', prompt='project id', help='Project ID')
@click.option('--device-type', prompt='What kind of device is this OLI Box connected to?', help='Meter, PV, AC, EV, ChargingStation, Battery')
@click.option('--market-type', prompt='What kind of market is this OLI Box connected to?', help='Producer, Consumer, Prosumer')
@click.option('--use-ethereum/--no-ethereum', prompt='Do you want to use Ethereum?', callback=prompt_ethereum)
@click.option('--use-modbus-tcp/--no-modbus-tcp', prompt='do you want to use ModbusTCP?', callback=prompt_modbus)
@click.option('--use-ir/--no-ir', prompt='Do you want to use IR Sensor?', callback=prompt_ir_impulse)
@click.option('--oli-restapi-ip', prompt='REST API IP', help='REST API IP address')
@click.option('--oli-restapi-query', prompt='REST API query parameter', help='REST API query parameters')
@click.option('--oli-restapi-port', prompt='REST API Port', help='REST API port')
@click.option('--oli-restapi-read-interval', prompt='What is the interval for reading values in seconds?', help='Time interval (seconds) to read REST API values')
@click.option('--oli-restapi-send-interval', prompt='What is the interval for sending values in seconds?', help='Time interval (seconds) to send REST API values')
def init(mqtt_broker_ip,
         mqtt_broker_port,
         ssl_cert_path,
         mqtt_username,
         mqtt_password,
         send_power_data,
         send_energy_data,
         energy_sending_interval,
         power_sending_interval,
         oli_box_id,
         project_id,
         device_type,
         market_type,
         use_ethereum,
         use_modbus_tcp,
         use_ir,
         oli_restapi_ip,
         oli_restapi_query,
         oli_restapi_port,
         oli_restapi_read_interval,
         oli_restapi_send_interval):

    use_ethereum, rpc_endpoint, rpc_port = use_ethereum

    use_modbus_tcp, modbus_server_ip, modbus_server_port, modbus_server_energy_demand_register, modbus_server_power_demand_register, modbus_server_energy_supply_register, modbus_server_power_supply_register = use_modbus_tcp

    use_ir, ir_impulse_rate, power_writing_interval, energy_writing_interval = use_ir

    config = f"""

     # This is a OLI Box TOML config file.
     title = "OLI BOX Config"

     [mqtt_connection]
     mqtt_broker_ip = '{mqtt_broker_ip}'
     mqtt_broker_port = '{mqtt_broker_port}'
     ssl_cert_path = '{ssl_cert_path}'
     mqtt_username = '{mqtt_username}'
     mqtt_password = '{mqtt_password}'
     send_power_data = '{send_power_data}'
     send_energy_data = '{send_energy_data}'
     energy_sending_interval = '{energy_sending_interval}'
     power_sending_interval = '{power_sending_interval}'

     [olibox_config]
     oli_box_id = '{oli_box_id}'
     project_id = '{project_id}'
     device_type = '{device_type}'
     market_type = '{market_type}'

     [ethereum]
     use_ethereum = '{use_ethereum}'
     rpc_endpoint = '{rpc_endpoint}'
     rpc_port = '{rpc_port}'

     [modbusTCP]
     use_modbustcp = '{use_modbus_tcp}'
     modbus_server_ip = '{modbus_server_ip}'
     modbus_server_port = '{modbus_server_port}'
     modbus_server_energy_demand_register = '{modbus_server_energy_demand_register}'
     modbus_server_power_demand_register = '{modbus_server_power_demand_register}'
     modbus_server_energy_supply_register = '{modbus_server_energy_supply_register}'
     modbus_server_power_supply_register = '{modbus_server_power_supply_register}'

     [ir_sensor]
     use_ir = '{use_ir}'
     ir_impulse_rate = '{ir_impulse_rate}'
     power_writing_interval = '{power_writing_interval}'
     energy_writing_interval = '{energy_writing_interval}'

     [rest_api]
     oli_restapi_ip = '{oli_restapi_ip}'
     oli_restapi_port = '{oli_restapi_port}'
     oli_restapi_read_interval = '{oli_restapi_read_interval}'
     oli_restapi_send_interval = '{oli_restapi_send_interval}'
     """
    parsed_config = toml.loads(config)
    formatted_config = toml.dumps(parsed_config)

    with open('../../config.toml', 'w') as f:
        f.write(formatted_config)
