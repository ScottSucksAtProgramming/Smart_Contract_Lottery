# ------------------------------ Documentation ------------------------------ #
# Module:  test_lottery.py
# Will test our Lottery.sol contracts.
#
#
# Modification History
# 4-12-2022 SRK

# ------------------------------ Resources ------------------------------ #
from brownie import Lottery, accounts, config, network
from web3 import Web3

# ------------------------------ Functions ------------------------------ #
def test_get_entrance_fee():
    # This will ensure that the entrance fee we pull from the Chainlink Aggregator
    # is correct (based of math we've done at the time).
    account = accounts[0]
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account},
    )
    assert lottery.getEntranceFee() > Web3.toWei(0.016, "ether")
    assert lottery.getEntranceFee() < Web3.toWei(0.018, "ether")
