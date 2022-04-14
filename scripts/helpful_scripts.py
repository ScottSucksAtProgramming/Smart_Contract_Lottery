# ------------------------------ Documentation ------------------------------ #
# Module:  helpful_scripts.py
# These scripts are used for deploying smart contracts via solidity and brownie.
#
#
# Modification History
# 04-14-2022 SRK.

# ------------------------------ Resources ------------------------------ #
from brownie import accounts, network, config

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

# ------------------------------ Functions ------------------------------ #
def get_account(index=None, id=None):
    # This functions will let us specify which accounts we want to use for our
    # contract deployment / interactions. We can pass an index for the ganache
    # accounts list. We can pass a specific account stored inside brownie as
    # an id. If we don't pass anything it will test to see if we are on a
    # development or forked blockchain and return the ganache accounts, if not
    # it will then pull from our brownie-config.yaml.
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])
