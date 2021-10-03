import json
import os

from dotenv import load_dotenv
from solcx import compile_standard
from web3 import Web3

load_dotenv()

with open('./contracts/SimpleStorage.sol', 'r') as f:
    simple_storage_file = f.read()

compiled_sol = compile_standard(
    {
        'language': 'Solidity',
        'sources': {
            'SimpleStorage.sol': {
                'content': simple_storage_file,
            },
        },
        'settings': {
            'outputSelection': {
                '*': {
                    '*': [
                        'abi',
                        'metadata',
                        'evm.bytecode',
                        'evm.sourceMap'
                    ],
                },
            },
        },
    },
    solc_version='0.8.0',
)

with open('compiled_code.json', 'w+') as f:
    json.dump(compiled_sol, f)


bytecode = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage'][
    'evm'
]['bytecode']['object']

abi = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['abi']

w3 = Web3(Web3.HTTPProvider(
    'https://kovan.infura.io/v3/c63c0466eb0e4b53a5751908eca9f3ad'))
chain_id = 42
my_address = '0x6e112b0d636934a71708e175C64EAAf7D57A5f94'
private_key = os.getenv('PRIVATE_KEY')

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = w3.eth.getTransactionCount(my_address)

# build a transaction
# sign a transaction
# send a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        'chainId': chain_id,
        'from': my_address,
        'nonce': nonce,
    }
)

signed_transaction = w3.eth.account.sign_transaction(
    transaction,
    private_key=private_key,
)

transaction_hash = w3.eth.send_raw_transaction(
    signed_transaction.rawTransaction)

transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
simple_storage = w3.eth.contract(
    address=transaction_receipt.contractAddress,
    abi=abi,
)


print(simple_storage.functions.retrieve().call())
print(simple_storage.functions.store(15).call())

store_transaction = simple_storage.functions.store(15).buildTransaction({
    'chainId': chain_id,
    'from': my_address,
    'nonce': nonce+1,
})
signed_store_transaction = w3.eth.account.sign_transaction(
    store_transaction,
    private_key=private_key,
)
send_store_transaction = w3.eth.send_raw_transaction(
    signed_store_transaction.rawTransaction
)
transaction_receipt = w3.eth.wait_for_transaction_receipt(
    send_store_transaction)

print(simple_storage.functions.retrieve().call())
