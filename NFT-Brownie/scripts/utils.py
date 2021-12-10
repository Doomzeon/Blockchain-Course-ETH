from brownie import network, accounts, config

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ['development', "ganache-locale"]
FORKED_BLOCKCHAIN_ENVIRONMENTS = ['mainnet-fork', 'mainnet-fork-dev']


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if(network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_BLOCKCHAIN_ENVIRONMENTS):
        return accounts[0]

    return accounts.add(config['wallets']['from_key'])