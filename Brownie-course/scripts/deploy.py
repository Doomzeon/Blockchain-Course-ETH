
from brownie import accounts, config, SimpleStorage, network
import os
# On brownie run it wil launch a main() brownie run scripts/deploy.py
# Is neede ganache-cli installed by yarn or nmp


def deploy_simple_storage():
    # account = accounts.load('doomzeon') # pas 1234
    #account = accounts.add(os.getenv("PRIVATE_KEY"))
    #account = accounts.add(config['wallets']['from_key'])
    account = get_account()
    simple_storage = SimpleStorage.deploy({"from": account})
    print(simple_storage)
    stored_value = simple_storage.retrieve()
    print(stored_value)
    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)
    uptade_tored_value = simple_storage.retrieve()
    print(uptade_tored_value)


def get_account():
    if(network.show_active() == "development"):
        return accounts[0]
    else:
        return accounts.add(config['wallets']['from_key'])


def main():
    deploy_simple_storage()
