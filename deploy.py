from solcx import compile_standard, install_solc
from web3 import Web3
from dotenv import load_dotenv
import json
import os

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Compile our solidity contract

install_solc("0.6.0")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*" : {
                    "*" : ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0"
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# Get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# Get ABI
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# Connecting to Ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
chain_id = 1337
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
private_key = os.getenv("PRIVATE_KEY")

# Create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
# 1. Build a transaction
transaction = SimpleStorage.constructor().buildTransaction({
    "gasPrice":w3.eth.gas_price,
    "chainId":chain_id, 
    "from":my_address, 
    "nonce":nonce
})
# 2. Sign a transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# 3. Send a transaction
print("Deploying contract")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!")

# Working with the contract, we'll need
# Contract Address
# Contract ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Call -> Simulate making the call and getting a return value
# Transact -> Actually make a state change

# Get initial value of favorite_number
print(simple_storage.functions.retrieve().call())
#Set a value for favorite number (build, sign and send the transaction)
print("Updating contract...")
store_transaction = simple_storage.functions.store(75).buildTransaction({
    "gasPrice":w3.eth.gas_price,
    "chainId":chain_id,
    "from":my_address,
    "nonce":nonce +1
})
signed_store_tx = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
send_store_tx = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Updated!")
