# ------------------------------ Documentation ------------------------------ #
# Module:  helpful_scripts.py
# These scripts are used for deploying smart contracts via solidity and brownie.
#
#
# Modification History
# 04-14-2022 SRK.

# ------------------------------ Resources ------------------------------ #
from brownie import (
    accounts,
    network,
    config,
    Contract,
    MockV3Aggregator,
    VRFCoordinatorMock,
    LinkToken,
)

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

# ------------------------------ Functions ------------------------------ #
def get_account(index=None, id=None):
    """This functions will let us specify which accounts we want to use for our
    contract deployment / interactions. We can pass an index for the ganache
    accounts list. We can pass a specific account stored inside brownie as
    an id. If we don't pass anything it will test to see if we are on a
    development or forked blockchain and return the ganache accounts, if not
    it will then pull from our brownie-config.yaml."""
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


# Dictionary that stores the contract type via a named key.
contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    """This function will grab the contract addresses from the brownie config
    if defined, otherwise it will deploy a mock version of that contract and
    return that mock contract.

        Args:
            contract_name (string)

        Returns:
            brownie.network.contract.ProjectContract: The most recently
            deployed version of this contract.
    """
    # Store the contract type as a variable by pulling from the dictionary above.
    contract_type = contract_to_mock[contract_name]
    # If we are on a local blockchain environment then we'll have to deply mock
    # contracts to be able to use the functions.
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        # The most recent contract object will be stored in the variable contract.
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


# Variables needed for the Price Feed Aggregator (MockV3Aggregator)
DECIMALS = 8
INITIAL_VALUE = 200_000_000_000


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    account = get_account()
    print(f"The active network is {network.show_active()}.")
    print("Deploying mock contracts...")
    mock_price_feed = MockV3Aggregator.deploy(
        decimals, initial_value, {"from": account}
    )
    print("Mock Price Feed deplyed!")
    link_token_mock = LinkToken.deploy({"from": account})
    print("Mock Chainlink Token deployed.")
    vrf_coordinator_mock = VRFCoordinatorMock.deploy(
        link_token_mock.address, {"from": account}
    )
    print("Mock Random Number Generator deployed!")
    print("All Mocks Deployed!!")


def fund_with_link(
    contract_address,
    account=None,
    link_token=None,
    amount=100_000_000_000_000_000,  # 0.1 Link
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Contract funded!")
    return tx
