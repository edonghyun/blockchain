import os

from brownie import (
    accounts,
    config,
    network,
    SimpleStorage,
)

from .helper import get_account


def deploy_simple_storage():
    account = get_account()
    simple_storage = SimpleStorage.deploy({
        'from': account,
    })
    stored_value = simple_storage.retrieve()
    transaction = simple_storage.store(15, {'from': account})
    transaction.wait(1)
    updated_stored_value = simple_storage.retrieve()


def main():
    deploy_simple_storage()
