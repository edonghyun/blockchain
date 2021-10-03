from brownie import (
    accounts,
    config,
    network,
    interface,
    Contract,
    LinkToken,
    MockV3Aggregator,
    VRFCoordinatorMock,
)
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = [
    'mainnet-fork',
    'mainnet-fork-dev',
]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    'development',
    'ganache-local',
]

DECIMALS = 8
INITIAL_VALUE = Web3.toWei(20000000000, 'ether')


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if(network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS):
        return accounts[0]
    return accounts.add(config['wallets']['from_key'])


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    if len(MockV3Aggregator) <= 0:
        account = get_account()
        MockV3Aggregator.deploy(
            decimals,
            initial_value,
            {
                'from': account,
            }
        )
        link_token = LinkToken.deploy(
            {
                'from': account,
            }
        )
        VRFCoordinatorMock.deploy(
            link_token.address,
            {
                'from': account,
            }
        )
    print('Mocks deployed !')


contract_to_mock = {
    'eth_usd_price_feed': MockV3Aggregator,
    'vrf_coordinator': VRFCoordinatorMock,
    'link_token': LinkToken,
}


def get_contract(contract_name):
    '''
        this function will grab the contract address from the brownie config
        if defined, otherwise, it will deploy a mock version of that contract,
        and return that mock contract.

            Args:
                contract_name (string)

            Returns:
                brownie.network.contract.ProjectContract: 
                The most recently deployed veresion of this contract.
    '''
    contract_type = contract_to_mock[contract_name]
    activated_network = network.show_active()
    if activated_network in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            # MockV3Aggregator.length
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config['networks'][activated_network][contract_name]
        # address
        # ABI
        contract = Contract.from_abi(
            contract_type._name,
            contract_address,
            contract_type.abi,
        )
    return contract


def fund_with_link(
    contract_address,
    account=None,
    link_token=None,
    amount=100000000000000000  # 0.1 LINK
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract('link_token')

    link_token_contract = interface.LinkTokenInterface(link_token.address)
    transaction = link_token_contract.transfer(
        contract_address, amount, {'from': account})
    transaction.wait(1)

    print('Fund contract !')
    return transaction
