from brownie import SimpleStorage, accounts


def test_deploy():
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    storing_value = simple_storage.retrieve()
    assert storing_value == 0
