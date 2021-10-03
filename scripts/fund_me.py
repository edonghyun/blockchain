from brownie import (
    config,
    network,
    FundMe,
    MockV3Aggregator,
)
from web3 import Web3

from .helper import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()
    activated_nework = network.show_active()
    if activated_nework not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config['networks'][
            activated_nework
        ]['eth_usd_price_feed']
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {
            'from': account,
        },
        publish_source=config['networks'][activated_nework]['verify'],
    )
    print(f'Contract deployed to {fund_me.address}')
    return fund_me


def main():
    deploy_fund_me()
