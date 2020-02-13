
# import os.path
# import time

# import toml

# #from .web3_config import set_web3_provider


# def instantiate_contract():
#     """
#     Create an instance of smart contract.
#     """
#     if os.path.isfile('../../../config.toml'):
#         f = toml.load('../../../config.toml')
#         url, port = f['web3_provider']['url'], f['web3_provider']['port']
#         #web3 = set_web3_provider(url, port)

#         contract_abi = '[{"inputs":[{"internalType":"uint8","name":"_numProposals","type":"uint8"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"delegate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"toVoter","type":"address"}],"name":"giveRightToVote","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint8","name":"toProposal","type":"uint8"}],"name":"vote","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"winningProposal","outputs":[{"internalType":"uint8","name":"_winningProposal","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"}]'
#         contract_address = '0xb75a1f7ebdb4292dce732835ef33af74c19b7e03'
#         account = web3.toChecksumAddress(
#             "0xb75a1f7ebdb4292dce732835ef33af74c19b7e03")

#         web3.eth.defaultAccount = account

#         # Contract Address and abi from other import
#         contract_address = web3.toChecksumAddress(contract_address)
#         contract = web3.eth.contract(address=contract_address, abi=contract_abi)

#         return contract


# contract = instantiate_contract()



# # Web3 Power Send Function
# def web3_power(powerSupply):

#     if os.path.isfile('../../../config.toml'):

#         f = toml.load('../../../config.toml')
#         url, port = f['web3_provider']['url'], f['web3_provider']['port']
#         web3 = set_web3_provider(url, port)

#         try:
#             tx_hash = contract.functions.setInverterPower(
#                 int(powerSupply)).transact()
#             web3.eth.waitForTransactionReceipt(tx_hash)
#             print("Done transaction of power supply: "+str(powerSupply))
#         except Exception as ex:
#             # logger.exception("WEB3_POWER Exception")
#             print(ex)
#             print("Exception in Web3 transaction")
#             tx_hash = contract.functions.setInverterPower(
#                 int(powerSupply)).transact()
#             web3.eth.waitForTransactionReceipt(tx_hash)
#             print("Done transaction of power supply after Exception: "+str(powerSupply))


# def new_dso_value(delay):
#     while 1:
#         try:
#             event_filter = contract.events.NewDsoValue.createFilter(
#                 fromBlock='latest')
#             e = event_filter.get_new_entries()
#             print(e)
#             for event in e:
#                 n = wd.AttributeDict(e[0])
#                 print(n)
#                 event_value = n['args']['value']
#                 event_asset = n['args']['asset']
#                 event_dso = n['args']['dso']
#                 event_time = n['args']['time']
#                 if(event_asset == account):
#                     print("Its my account")
#                     try:
#                         print(str(event_value))
#                         tx_hash = contract.functions.setInverterOutput(
#                             int(event_value)).transact()
#                         web3.eth.waitForTransactionReceipt(tx_hash)
#                         print("Done transaction of inverter output: " +
#                               str(event_value))
#                         print("Setting new output level in Modbus Register....")
#                         writeOutputLevel(event_value)
#                         print("...done.")
#                     except Exception as ex:
#                         logger.exception(
#                             "Exception in NEW_DSO_VALUE Web3 transaction")
#                         print(ex)
#                         print("Exception in Web3 transaction of new_dso_value")
#                         tx_hash = contract.functions.setInverterOutput(
#                             int(event_value)).transact()
#                         web3.eth.waitForTransactionReceipt(tx_hash)
#                         print("Done transaction of inverter output: " +
#                               str(event_value))
#         except Exception as ex:
#             # logger.exception("Exception in NEW_DSO_VALUE")
#             print(ex)
#             print("Exception in new_dso_value")
#         time.sleep(delay)
