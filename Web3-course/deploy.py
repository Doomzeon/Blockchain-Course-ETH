from web3 import Web3
from solcx import compile_standard, install_solc
import json
import os
from dotenv import load_dotenv
load_dotenv()
install_solc("0.6.0")
# This lines are going to open the file and read it
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# to compile sol files we need compiler pip3 install py-solc-x =>see documentation for mor optioins


# Comiple Solidity file to "machine level code"
compiled_sol = compile_standard(
    {"language": "Solidity",
     "sources": {
         "SimpleStorage.sol": {"content": simple_storage_file}
     },
     "settings": {
         "outputSelection": {
             "*": {
                 "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
             }
         }
     }}, solc_version="0.6.0"
)

# Write compile file of solidity inside file json to see everything
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# To deploy contract with have to have abi and bytecode

# 1. get bytecode from json file to deploy solidity contract
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]


# 2. Get abi from json file to deploy solidity contract
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# Intall ganache and pip3 install web3

# Connecting to ganache with web3
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337
my_adress = "0xd02Ee64Dc4D186583553273A2c3479ba9a58bd7D"

# put private key inside .env file
# write export PRIVATE_KEY=0x75f5ca2885eb1cd77461054f580c26e9ff1cda6075f3383578d5b5ee9abad097
# "0x75f5ca2885eb1cd77461054f580c26e9ff1cda6075f3383578d5b5ee9abad097"
private_key = os.getenv("PRIVATE_KEY")

# Deploy contract on local Ganache blockchain with 1 node:

# 1. Create contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
print(SimpleStorage)

# 2. Get nonce
nonce = w3.eth.getTransactionCount(my_adress)
print(nonce)

# 3. Build transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_adress, "nonce": nonce})
print(transaction)

# 4. Sign a transaction
signet_txn = w3.eth.account.sign_transaction(transaction, private_key)
print(signet_txn)

# 5. Send signed transaction
tx_hash = w3.eth.send_raw_transaction(signet_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# To work with the contract we need
# 1. Contract adress and abi
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# to interact with the contract we can 1. Call => simalte making call and getting return value, we can not make state changes with the call (blue buttons in remix)
# 2. Transact => Make a state changes like orange button
# Call example
print(simple_storage.functions.retrieve().call())

# Transact example
# fOR EVERY TRANSACTION WE HAVE TO HAVE ANOTHER NOCE NUMBER
# We are creating new transaction with changing the number
store_transaction = simple_storage.functions.store(15).buildTransaction({
    "chainId": chain_id, "from": my_adress, "nonce": nonce+1
})

signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key)
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)

print(simple_storage.functions.retrieve().call())
