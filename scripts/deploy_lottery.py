import time

from brownie import (
    network,
    config,
    Lottery,
)

from .helper import (
    get_contract,
    get_account,
    fund_with_link,
)


def deploy_lottery():
    account = get_account()
    activated_network = network.show_active()
    print(activated_network)
    lottery = Lottery.deploy(
        get_contract('eth_usd_price_feed').address,
        get_contract('vrf_coordinator').address,
        get_contract('link_token').address,
        config['networks'][activated_network]['fee'],
        config['networks'][activated_network]['keyhash'],
        {
            'from': account,
        },
        publish_source=config['networks'][activated_network]['verify'],
    )
    print('Deployed lottery!')

    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_transaction = lottery.startLottery({
        'from': account,
    })
    starting_transaction.wait(1)
    print('The lottery is started !')


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    transaction = lottery.enter(
        {
            'from': account,
            'value': value,
        }
    )
    transaction.wait(1)
    print('You entered the lottery !')


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    transaction = fund_with_link(lottery.address)
    transaction.wait(1)

    ending_transaction = lottery.endLottery(
        {
            'from': account,
        }
    )
    ending_transaction.wait(1)
    time.sleep(60)
    print(f'{lottery.recentWinner()} is the new winner !')


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
