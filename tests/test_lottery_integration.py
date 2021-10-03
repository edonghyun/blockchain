import pytest
import time

from web3 import Web3
from brownie import (
    accounts,
    config,
    exceptions,
    network,
    Lottery,
)
from scripts.deploy_lottery import (
    deploy_lottery,
)
from scripts.helper import (
    get_account,
    get_contract,
    fund_with_link,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def use_skip_in_local_blockchain(func):
    def inner_func(*args, **kwargs):
        if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
            pytest.skip()
        return func(*args, **kwargs)
    return inner_func


@use_skip_in_local_blockchain
def test_can_pick_winner():
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery(
        {
            'from': account,
        },
    )
    lottery.enter(
        {
            'from': account,
            'value': lottery.getEntranceFee(),
        }
    )

    fund_with_link(lottery)
    lottery.endLottery(
        {
            'from': account,
        }
    )
    time.sleep(60)

    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
