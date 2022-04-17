# ------------------------------ Documentation ------------------------------ #
# Module: test_lottery.py
# Will test our Lottery.sol contracts.
#
#
# Modification History
# 4-12-2022 SRK

# ------------------------------ Resources ------------------------------ #
from brownie import Lottery, accounts, config, network
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS
from web3 import Web3
import pytest

# ------------------------------ Functions ------------------------------ #
def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    # Act
    entrance_fee = lottery.getEntranceFee()
    # Assert
    expected_entrance_fee = Web3.toWei(0.016, "ether")
    assert entrance_fee == entrance_fee
