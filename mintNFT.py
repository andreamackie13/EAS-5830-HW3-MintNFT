from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from eth_account.messages import encode_defunct
import eth_account
import random
import json 
import os

RPC = "https://api.avax-test.network/ext/bc/C/rpc"
w3 = Web3(Web3.HTTPProvider(RPC))
w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

private_key = "0x7403db68b5d5c4c3c143be2f693c32b50fc6ef91eb7e314e94da5b30602dde16"
acc = eth_account.Account.from_key(private_key)
address = acc.address

print("Addy", address)

contract_address = "0x85ac2e065d4526FBeE6a2253389669a12318A412"

with open("NFT.abi", "r") as NFTabi: 
  data = json.load(NFTabi)
ABI = data["abi"] if isinstance(data,dict) and "abi" in data else data

contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=ABI)

nonce_bytes = os.urandom(32)

tx = contract.functions.claim(address, nonce_bytes).build_transaction({
  "from": address,
  "nonce": w3.eth.get_transaction_count(address),
  "chainId": 43113,
  "maxFeePerGas": w3.to_wei("50", "gwei"),
  "maxPriorityFeePerGas": w3.to_wei("2", "gwei"),
  "gas": 250_000,
})

signed_tx = acc.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
minted = w3.eth.wait_for_transaction_receipt(tx_hash)
print("minted", minted.status)
