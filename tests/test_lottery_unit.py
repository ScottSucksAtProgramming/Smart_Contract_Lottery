# ------------------------------ Documentation ------------------------------ #
# Module: test_lottery.py
# Will test our Lottery.sol contracts.
#
#
# Modification History
# 4-12-2022 SRK

# ------------------------------ Resources ------------------------------ #
from webbrowser import get
from brownie import Lottery, accounts, config, network, exceptions
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    fund_with_link,
    get_contract,
)
from web3 import Web3
import pytest

# ------------------------------ Functions ------------------------------ #
def test_get_entrance_fee():
    # Only perform test if on a live blockchain.
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    # Act
    entrance_fee = lottery.getEntranceFee()
    # Assert
    expected_entrance_fee = Web3.toWei(0.016, "ether")
    assert entrance_fee == entrance_fee


def test_cant_enter_unless_started():
    # Arrange
    # Only perform test if on a live blockchain.
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    # Act and Assert
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})


def test_can_start_and_enter_lottery():
    # Arrange
    # Only perform test if on a live blockchain.
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    # Act
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    # Assert
    assert lottery.players(0) == account


def test_can_end_lottery():
    # Arrange
    # Only perform test if on a live blockchain.
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    # Act
    lottery.endLottery({"from": account})
    # Assert
    expect_lottery_status = 2
    assert lottery.lottery_state() == expect_lottery_status


def test_can_pick_winner_correctly():
    # Arrange
    # Only perform test if on a live blockchain.
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=1), "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=2), "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    # Act
    transaction = lottery.endLottery({"from": account})
    request_id = transaction.events["RequestedRandomness"]["requestID"]
    STATIC_RNG = 777
    # Since we're testing the ability for out lottery to pick out the correct winner we
    # want to feed it a static number that we will know the answer to. In this case
    # its 777. 777 / 3 = 250 (remainder 0) meaning the first person to enter the
    # lottery has won.
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, STATIC_RNG, lottery.address, {"from": account}
    )
    # Assert
    starting_balance_of_account = account.balance()
    balance_of_lottery = lottery.balance()
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account.balance() == starting_balance_of_account + balance_of_lottery
