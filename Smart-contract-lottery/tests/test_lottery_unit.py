
from brownie import Lottery, accounts, config, network
from scripts.deploy import deploy_lottery
from web3 import Web3
from scripts import utils
import pytest

## Pytest only on develop network
def test_get_entrance_fee():
    if network.show_active() not in utils.LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    expected_entrance_fee = Web3.toWei(0.025, 'ether')
    entrance_fee = lottery.getEntranceFee()
    assert entrance_fee == expected_entrance_fee
