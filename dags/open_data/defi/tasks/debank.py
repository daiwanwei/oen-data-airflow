import json
from datetime import datetime

from ..common import get_addresses_for_index
from ..debank import get_balance_data, get_project_data_by_user
from ..load import load_assets_to_db
from ..transform import transform_balance_data, transform_project_data
from ...utils.db_utils import get_db_conn_from_env


def get_user_balances_task_logic(exec_time: datetime, dir_path: str) -> list[str]:
    import json
    addresses = get_addresses_for_index()
    data_path = []
    for address in addresses:
        try:
            data = get_balance_data(address)
            timestamp = int(exec_time.timestamp())
            data['exec_time'] = exec_time.strftime('%Y-%m-%d %H:%M:%S')
            data['owner'] = address
            data_json = json.dumps(data)
            path = f'{dir_path}/user_data_{address}_{timestamp}.json'
            with open(path, 'w') as f:
                f.write(data_json)
            data_path.append(path)
        except Exception as e:
            print(f'get user({address}) data failed')
            print(e)
        print(f'get user({address}) data success, path: {path}')
    return data_path


def get_project_balances_task_logic(exec_time: datetime, dir_path: str) -> list[str]:
    import json
    addresses = get_addresses_for_index()
    data_path = []
    for address in addresses:
        try:
            # data = get_project_data_by_user(address)
            data = get_project_data_fake()
            timestamp = int(exec_time.timestamp())
            data['exec_time'] = exec_time.strftime('%Y-%m-%d %H:%M:%S')
            data['owner'] = address
            data_json = json.dumps(data)
            path = f'{dir_path}/project_data_{address}_{timestamp}.json'
            with open(path, 'w') as f:
                f.write(data_json)
            data_path.append(path)
        except Exception as e:
            print(f'get user({address}) data failed')
            print(e)
        print(f'get user({address}) data success, path: {path}')
    return data_path


def parse_user_balances_task_logic(output_csv: str, balance_data_paths: list[str]):
    output_list = []
    for path in balance_data_paths:
        print(f'parse {path}')
        with open(path, 'r') as f:
            balance_data = json.load(f)
        owner = balance_data['owner']
        recorded_at = balance_data['exec_time']
        balance_list = transform_balance_data(owner, balance_data['data'])
        output_list.extend(balance_list)
    save_balances_to_csv(output_csv, recorded_at, output_list)


def parse_project_balances_task_logic(output_csv: str, balance_data_paths: list[str]):
    output_list = []
    for path in balance_data_paths:
        print(f'parse {path}')
        with open(path, 'r') as f:
            balance_data = json.load(f)
        owner = balance_data['owner']
        recorded_at = balance_data['exec_time']
        for project in balance_data['data']:
            balance_list = transform_project_data(owner, project)
            output_list.extend(balance_list)
    save_balances_to_csv(output_csv, recorded_at, output_list)


def save_balances_to_csv(output_csv: str, recorded_at: str, balance_list: list):
    import pandas as pd
    owner_address_list = []
    chain_list = []
    symbol_list = []
    usd_value_list = []
    amount_list = []
    price_list = []
    asset_type_list = []
    is_debt_list = []
    project_list = []
    recorded_at_list = []
    for balance in balance_list:
        owner_address_list.append(balance['owner_address'])
        chain_list.append(balance['chain'])
        symbol_list.append(balance['symbol'])
        usd_value_list.append(balance['usd_value'])
        amount_list.append(balance['amount'])
        price_list.append(balance['price'])
        asset_type_list.append(balance['asset_type'])
        is_debt_list.append(balance['is_debt'])
        project_list.append(balance['project'])
        recorded_at_list.append(recorded_at)
    df = pd.DataFrame({
        'owner_address': owner_address_list,
        'chain': chain_list,
        'symbol': symbol_list,
        'usd_value': usd_value_list,
        'amount': amount_list,
        'price': price_list,
        'asset_type': asset_type_list,
        'is_debt': is_debt_list,
        'project': project_list,
        'recorded_at': recorded_at_list
    })
    df.to_csv(output_csv, index=False)


def load_asset_balances_to_db_task(csv_file: str):
    conn = get_db_conn_from_env()
    load_assets_to_db(conn, csv_file)


def get_project_data_fake():
    return {
        "_cache_seconds": 0,
        "_seconds": 0.038390398025512695,
        "_use_cache": False,
        "data": [
            {
                "chain": "arb",
                "dao_id": "aave",
                "has_supported_portfolio": True,
                "id": "arb_aave3",
                "is_tvl": False,
                "is_visible_in_defi": None,
                "logo_url": "https://static.debank.com/image/project/logo_url/avax_aave3/9459cb86efd13145537eab8104e923bf.png",
                "name": "Aave V3",
                "platform_token_id": None,
                "portfolio_item_list": [
                    {
                        "asset_dict": {
                            "0x82af49447d8a07e3bd95bd0d56f35241523fbab1": 0.2001053595294188,
                            "0xaf88d065e77c8cc2239327c5edb3a432268e5831": -200.327382
                        },
                        "asset_token_list": [
                            {
                                "amount": 0.2001053595294188,
                                "chain": "arb",
                                "decimals": 18,
                                "display_symbol": None,
                                "id": "0x82af49447d8a07e3bd95bd0d56f35241523fbab1",
                                "is_core": True,
                                "is_verified": True,
                                "is_wallet": True,
                                "logo_url": "https://static.debank.com/image/arb_token/logo_url/0x82af49447d8a07e3bd95bd0d56f35241523fbab1/61844453e63cf81301f845d7864236f6.png",
                                "name": "Wrapped Ether",
                                "optimized_symbol": "WETH",
                                "price": 2061.09,
                                "protocol_id": "",
                                "symbol": "WETH",
                                "time_at": 1622346702.0
                            },
                            {
                                "amount": -200.327382,
                                "chain": "arb",
                                "decimals": 6,
                                "display_symbol": None,
                                "id": "0xaf88d065e77c8cc2239327c5edb3a432268e5831",
                                "is_core": True,
                                "is_verified": True,
                                "is_wallet": True,
                                "logo_url": "https://static.debank.com/image/arb_token/logo_url/0xaf88d065e77c8cc2239327c5edb3a432268e5831/fffcd27b9efff5a86ab942084c05924d.png",
                                "name": "USD Coin",
                                "optimized_symbol": "USDC",
                                "price": 1.0,
                                "protocol_id": "",
                                "symbol": "USDC",
                                "time_at": 1667248932.0
                            }
                        ],
                        "detail": {
                            "borrow_token_list": [
                                {
                                    "amount": 200.327382,
                                    "chain": "arb",
                                    "decimals": 6,
                                    "display_symbol": None,
                                    "id": "0xaf88d065e77c8cc2239327c5edb3a432268e5831",
                                    "is_core": True,
                                    "is_verified": True,
                                    "is_wallet": True,
                                    "logo_url": "https://static.debank.com/image/arb_token/logo_url/0xaf88d065e77c8cc2239327c5edb3a432268e5831/fffcd27b9efff5a86ab942084c05924d.png",
                                    "name": "USD Coin",
                                    "optimized_symbol": "USDC",
                                    "price": 1.0,
                                    "protocol_id": "",
                                    "symbol": "USDC",
                                    "time_at": 1667248932.0
                                }
                            ],
                            "health_rate": 1.7504248439606602,
                            "supply_token_list": [
                                {
                                    "amount": 0.2001053595294188,
                                    "chain": "arb",
                                    "decimals": 18,
                                    "display_symbol": None,
                                    "id": "0x82af49447d8a07e3bd95bd0d56f35241523fbab1",
                                    "is_core": True,
                                    "is_verified": True,
                                    "is_wallet": True,
                                    "logo_url": "https://static.debank.com/image/arb_token/logo_url/0x82af49447d8a07e3bd95bd0d56f35241523fbab1/61844453e63cf81301f845d7864236f6.png",
                                    "name": "Wrapped Ether",
                                    "optimized_symbol": "WETH",
                                    "price": 2061.09,
                                    "protocol_id": "",
                                    "symbol": "WETH",
                                    "time_at": 1622346702.0
                                }
                            ]
                        },
                        "detail_types": [
                            "lending"
                        ],
                        "name": "Lending",
                        "pool": {
                            "adapter_id": "aave3_proxy_lending",
                            "chain": "arb",
                            "controller": "0x794a61358d6845594f94dc1db02a252b5b4814ad",
                            "id": "0x794a61358d6845594f94dc1db02a252b5b4814ad",
                            "index": None,
                            "project_id": "arb_aave3",
                            "time_at": 1647010881
                        },
                        "proxy_detail": {},
                        "stats": {
                            "asset_usd_value": 412.43515547248984,
                            "debt_usd_value": 200.327382,
                            "net_usd_value": 212.10777347248984
                        },
                        "update_at": 1699697125.0
                    }
                ],
                "site_url": "https://app.aave.com",
                "tag_ids": [
                    "debt"
                ],
                "tvl": 203955424.16334045
            },
            {
                "chain": "arb",
                "dao_id": "beefy",
                "has_supported_portfolio": True,
                "id": "arb_beefy",
                "is_tvl": False,
                "is_visible_in_defi": None,
                "logo_url": "https://static.debank.com/image/project/logo_url/arb_beefy/98a5cc0f4596cbdeb9abe5125ae7e9e7.png",
                "name": "Beefy",
                "platform_token_id": "0x99c409e5f62e4bd2ac142f17cafb6810b8f0baae",
                "portfolio_item_list": [
                    {
                        "asset_dict": {
                            "0x17fc002b466eec40dae837fc4be5c67993ddbd6f": 6.635970703942071,
                            "0x2f2a2543b76a4166549f7aab2e75bef0aefc5b0f": 0.0017050159551977174,
                            "0x82af49447d8a07e3bd95bd0d56f35241523fbab1": 0.02813320830356541,
                            "0xaf88d065e77c8cc2239327c5edb3a432268e5831": 16.542601652398815,
                            "0xda10009cbd5d07dd0cecc66161fc93d7c9000da1": 6.3824766324520965,
                            "0xf97f4df75117a78c1a5a0dbb814af92458539fb4": 0.23220561474085502,
                            "0xfa7f8980b0f1e64a2062791cc3b0871572f1f7f0": 0.31171129344884024,
                            "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9": 3.309008139775368,
                            "0xfea7a6a0b346362bf88a9e4a88416b77a57d6c2a": 6.490497253876655e-07,
                            "0xff970a61a04b1ca14834a43f5de4533ebddb5cc8": 48.769345882583224
                        },
                        "asset_token_list": [
                            {
                                "amount": 0.0017050159551977174,
                                "chain": "arb",
                                "decimals": 8,
                                "display_symbol": None,
                                "id": "0x2f2a2543b76a4166549f7aab2e75bef0aefc5b0f",
                                "is_core": True,
                                "is_verified": True,
                                "is_wallet": True,
                                "logo_url": "https://static.debank.com/image/arb_token/logo_url/0x2f2a2543b76a4166549f7aab2e75bef0aefc5b0f/d3c52e7c7449afa8bd4fad1c93f50d93.png",
                                "name": "Wrapped BTC",
                                "optimized_symbol": "WBTC",
                                "price": 37017.8,
                                "protocol_id": "",
                                "symbol": "WBTC",
                                "time_at": 1623867469.0
                            },
                            {
                                "amount": 0.02813320830356541,
                                "chain": "arb",
                                "decimals": 18,
                                "display_symbol": None,
                                "id": "0x82af49447d8a07e3bd95bd0d56f35241523fbab1",
                                "is_core": True,
                                "is_verified": True,
                                "is_wallet": True,
                                "logo_url": "https://static.debank.com/image/arb_token/logo_url/0x82af49447d8a07e3bd95bd0d56f35241523fbab1/61844453e63cf81301f845d7864236f6.png",
                                "name": "Wrapped Ether",
                                "optimized_symbol": "WETH",
                                "price": 2061.09,
                                "protocol_id": "",
                                "symbol": "WETH",
                                "time_at": 1622346702.0
                            },
                            {
                                "amount": 48.769345882583224,
                                "chain": "arb",
                                "decimals": 6,
                                "display_symbol": "USDC(Bridged)",
                                "id": "0xff970a61a04b1ca14834a43f5de4533ebddb5cc8",
                                "is_core": True,
                                "is_verified": True,
                                "is_wallet": True,
                                "logo_url": "https://static.debank.com/image/coin/logo_url/usdc/e87790bfe0b3f2ea855dc29069b38818.png",
                                "name": "USD Coin (Arb1)",
                                "optimized_symbol": "USDC(Bridged)",
                                "price": 1.0,
                                "protocol_id": "arb_tracer",
                                "symbol": "USDC",
                                "time_at": 1623868379.0
                            },
                            {
                                "amount": 0.23220561474085502,
                                "chain": "arb",
                                "decimals": 18,
                                "display_symbol": None,
                                "id": "0xf97f4df75117a78c1a5a0dbb814af92458539fb4",
                                "is_core": True,
                                "is_verified": True,
                                "is_wallet": True,
                                "logo_url": "https://static.debank.com/image/arb_token/logo_url/0xf97f4df75117a78c1a5a0dbb814af92458539fb4/69425617db0ef93a7c21c4f9b81c7ca5.png",
                                "name": "ChainLink Token",
                                "optimized_symbol": "LINK",
                                "price": 15.038783670009687,
                                "protocol_id": "",
                                "symbol": "LINK",
                                "time_at": 1623867040.0
                            },
                            {
                                "amount": 0.31171129344884024,
                                "chain": "arb",
                                "decimals": 18,
                                "display_symbol": None,
                                "id": "0xfa7f8980b0f1e64a2062791cc3b0871572f1f7f0",
                                "is_core": True,
                                "is_verified": True,
                                "is_wallet": True,
                                "logo_url": "https://static.debank.com/image/arb_token/logo_url/0xfa7f8980b0f1e64a2062791cc3b0871572f1f7f0/fcee0c46fc9864f48ce6a40ed1cdd135.png",
                                "name": "Uniswap",
                                "optimized_symbol": "UNI",
                                "price": 5.390626390213456,
                                "protocol_id": "arb_uniswap3",
                                "symbol": "UNI",
                                "time_at": 1623867248.0
                            },
                            {
                                "amount": 3.309008139775368,
                                "chain": "arb",
                                "decimals": 6,
                                "display_symbol": None,
                                "id": "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9",
                                "is_core": True,
                                "is_verified": True,
                                "is_wallet": True,
                                "logo_url": "https://static.debank.com/image/coin/logo_url/usdt/23af7472292cb41dc39b3f1146ead0fe.png",
                                "name": "Tether USD",
                                "optimized_symbol": "USDT",
                                "price": 1.000495,
                                "protocol_id": "arb_rhino",
                                "symbol": "USDT",
                                "time_at": 1630432123.0
                            },
                            {
                                "amount": 6.490497253876655e-07,
                                "chain": "arb",
                                "decimals": 18,
                                "display_symbol": None,
                                "id": "0xfea7a6a0b346362bf88a9e4a88416b77a57d6c2a",
                                "is_core": True,
                                "is_verified": True,
                                "is_wallet": True,
                                "logo_url": "https://static.debank.com/image/arb_token/logo_url/0xfea7a6a0b346362bf88a9e4a88416b77a57d6c2a/7d0c0fb6eab1b7a8a9bfb7dcc04cb11e.png",
                                "name": "Magic Internet Money",
                                "optimized_symbol": "MIM",
                                "price": 0.9953961290010743,
                                "protocol_id": "arb_multichain",
                                "symbol": "MIM",
                                "time_at": 1631595191.0
                            },
                            {
                                "amount": 6.635970703942071,
                                "chain": "arb",
                                "decimals": 18,
                                "display_symbol": None,
                                "id": "0x17fc002b466eec40dae837fc4be5c67993ddbd6f",
                                "is_core": True,
                                "is_verified": True,
                                "is_wallet": True,
                                "logo_url": "https://static.debank.com/image/arb_token/logo_url/0x17fc002b466eec40dae837fc4be5c67993ddbd6f/4f323e33bfffa864c577e7bd2a3257c9.png",
                                "name": "Frax",
                                "optimized_symbol": "FRAX",
                                "price": 0.9989999971001299,
                                "protocol_id": "arb_frax",
                                "symbol": "FRAX",
                                "time_at": 1632766868.0
                            },
                            {
                                "amount": 6.3824766324520965,
                                "chain": "arb",
                                "decimals": 18,
                                "display_symbol": None,
                                "id": "0xda10009cbd5d07dd0cecc66161fc93d7c9000da1",
                                "is_core": True,
                                "is_verified": True,
                                "is_wallet": True,
                                "logo_url": "https://static.debank.com/image/arb_token/logo_url/0xda10009cbd5d07dd0cecc66161fc93d7c9000da1/549c4205dbb199f1b8b03af783f35e71.png",
                                "name": "Dai Stablecoin",
                                "optimized_symbol": "DAI",
                                "price": 0.99995,
                                "protocol_id": "",
                                "symbol": "DAI",
                                "time_at": 1632133487.0
                            },
                            {
                                "amount": 16.542601652398815,
                                "chain": "arb",
                                "decimals": 6,
                                "display_symbol": None,
                                "id": "0xaf88d065e77c8cc2239327c5edb3a432268e5831",
                                "is_core": True,
                                "is_verified": True,
                                "is_wallet": True,
                                "logo_url": "https://static.debank.com/image/arb_token/logo_url/0xaf88d065e77c8cc2239327c5edb3a432268e5831/fffcd27b9efff5a86ab942084c05924d.png",
                                "name": "USD Coin",
                                "optimized_symbol": "USDC",
                                "price": 1.0,
                                "protocol_id": "",
                                "symbol": "USDC",
                                "time_at": 1667248932.0
                            }
                        ],
                        "detail": {
                            "supply_token_list": [
                                {
                                    "amount": 0.0017050159551977174,
                                    "chain": "arb",
                                    "decimals": 8,
                                    "display_symbol": None,
                                    "id": "0x2f2a2543b76a4166549f7aab2e75bef0aefc5b0f",
                                    "is_core": True,
                                    "is_verified": True,
                                    "is_wallet": True,
                                    "logo_url": "https://static.debank.com/image/arb_token/logo_url/0x2f2a2543b76a4166549f7aab2e75bef0aefc5b0f/d3c52e7c7449afa8bd4fad1c93f50d93.png",
                                    "name": "Wrapped BTC",
                                    "optimized_symbol": "WBTC",
                                    "price": 37017.8,
                                    "protocol_id": "",
                                    "symbol": "WBTC",
                                    "time_at": 1623867469.0
                                },
                                {
                                    "amount": 0.02813320830356541,
                                    "chain": "arb",
                                    "decimals": 18,
                                    "display_symbol": None,
                                    "id": "0x82af49447d8a07e3bd95bd0d56f35241523fbab1",
                                    "is_core": True,
                                    "is_verified": True,
                                    "is_wallet": True,
                                    "logo_url": "https://static.debank.com/image/arb_token/logo_url/0x82af49447d8a07e3bd95bd0d56f35241523fbab1/61844453e63cf81301f845d7864236f6.png",
                                    "name": "Wrapped Ether",
                                    "optimized_symbol": "WETH",
                                    "price": 2061.09,
                                    "protocol_id": "",
                                    "symbol": "WETH",
                                    "time_at": 1622346702.0
                                },
                                {
                                    "amount": 48.769345882583224,
                                    "chain": "arb",
                                    "decimals": 6,
                                    "display_symbol": "USDC(Bridged)",
                                    "id": "0xff970a61a04b1ca14834a43f5de4533ebddb5cc8",
                                    "is_core": True,
                                    "is_verified": True,
                                    "is_wallet": True,
                                    "logo_url": "https://static.debank.com/image/coin/logo_url/usdc/e87790bfe0b3f2ea855dc29069b38818.png",
                                    "name": "USD Coin (Arb1)",
                                    "optimized_symbol": "USDC(Bridged)",
                                    "price": 1.0,
                                    "protocol_id": "arb_tracer",
                                    "symbol": "USDC",
                                    "time_at": 1623868379.0
                                },
                                {
                                    "amount": 0.23220561474085502,
                                    "chain": "arb",
                                    "decimals": 18,
                                    "display_symbol": None,
                                    "id": "0xf97f4df75117a78c1a5a0dbb814af92458539fb4",
                                    "is_core": True,
                                    "is_verified": True,
                                    "is_wallet": True,
                                    "logo_url": "https://static.debank.com/image/arb_token/logo_url/0xf97f4df75117a78c1a5a0dbb814af92458539fb4/69425617db0ef93a7c21c4f9b81c7ca5.png",
                                    "name": "ChainLink Token",
                                    "optimized_symbol": "LINK",
                                    "price": 15.038783670009687,
                                    "protocol_id": "",
                                    "symbol": "LINK",
                                    "time_at": 1623867040.0
                                },
                                {
                                    "amount": 0.31171129344884024,
                                    "chain": "arb",
                                    "decimals": 18,
                                    "display_symbol": None,
                                    "id": "0xfa7f8980b0f1e64a2062791cc3b0871572f1f7f0",
                                    "is_core": True,
                                    "is_verified": True,
                                    "is_wallet": True,
                                    "logo_url": "https://static.debank.com/image/arb_token/logo_url/0xfa7f8980b0f1e64a2062791cc3b0871572f1f7f0/fcee0c46fc9864f48ce6a40ed1cdd135.png",
                                    "name": "Uniswap",
                                    "optimized_symbol": "UNI",
                                    "price": 5.390626390213456,
                                    "protocol_id": "arb_uniswap3",
                                    "symbol": "UNI",
                                    "time_at": 1623867248.0
                                },
                                {
                                    "amount": 3.309008139775368,
                                    "chain": "arb",
                                    "decimals": 6,
                                    "display_symbol": None,
                                    "id": "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9",
                                    "is_core": True,
                                    "is_verified": True,
                                    "is_wallet": True,
                                    "logo_url": "https://static.debank.com/image/coin/logo_url/usdt/23af7472292cb41dc39b3f1146ead0fe.png",
                                    "name": "Tether USD",
                                    "optimized_symbol": "USDT",
                                    "price": 1.000495,
                                    "protocol_id": "arb_rhino",
                                    "symbol": "USDT",
                                    "time_at": 1630432123.0
                                },
                                {
                                    "amount": 6.490497253876655e-07,
                                    "chain": "arb",
                                    "decimals": 18,
                                    "display_symbol": None,
                                    "id": "0xfea7a6a0b346362bf88a9e4a88416b77a57d6c2a",
                                    "is_core": True,
                                    "is_verified": True,
                                    "is_wallet": True,
                                    "logo_url": "https://static.debank.com/image/arb_token/logo_url/0xfea7a6a0b346362bf88a9e4a88416b77a57d6c2a/7d0c0fb6eab1b7a8a9bfb7dcc04cb11e.png",
                                    "name": "Magic Internet Money",
                                    "optimized_symbol": "MIM",
                                    "price": 0.9953961290010743,
                                    "protocol_id": "arb_multichain",
                                    "symbol": "MIM",
                                    "time_at": 1631595191.0
                                },
                                {
                                    "amount": 6.635970703942071,
                                    "chain": "arb",
                                    "decimals": 18,
                                    "display_symbol": None,
                                    "id": "0x17fc002b466eec40dae837fc4be5c67993ddbd6f",
                                    "is_core": True,
                                    "is_verified": True,
                                    "is_wallet": True,
                                    "logo_url": "https://static.debank.com/image/arb_token/logo_url/0x17fc002b466eec40dae837fc4be5c67993ddbd6f/4f323e33bfffa864c577e7bd2a3257c9.png",
                                    "name": "Frax",
                                    "optimized_symbol": "FRAX",
                                    "price": 0.9989999971001299,
                                    "protocol_id": "arb_frax",
                                    "symbol": "FRAX",
                                    "time_at": 1632766868.0
                                },
                                {
                                    "amount": 6.3824766324520965,
                                    "chain": "arb",
                                    "decimals": 18,
                                    "display_symbol": None,
                                    "id": "0xda10009cbd5d07dd0cecc66161fc93d7c9000da1",
                                    "is_core": True,
                                    "is_verified": True,
                                    "is_wallet": True,
                                    "logo_url": "https://static.debank.com/image/arb_token/logo_url/0xda10009cbd5d07dd0cecc66161fc93d7c9000da1/549c4205dbb199f1b8b03af783f35e71.png",
                                    "name": "Dai Stablecoin",
                                    "optimized_symbol": "DAI",
                                    "price": 0.99995,
                                    "protocol_id": "",
                                    "symbol": "DAI",
                                    "time_at": 1632133487.0
                                },
                                {
                                    "amount": 16.542601652398815,
                                    "chain": "arb",
                                    "decimals": 6,
                                    "display_symbol": None,
                                    "id": "0xaf88d065e77c8cc2239327c5edb3a432268e5831",
                                    "is_core": True,
                                    "is_verified": True,
                                    "is_wallet": True,
                                    "logo_url": "https://static.debank.com/image/arb_token/logo_url/0xaf88d065e77c8cc2239327c5edb3a432268e5831/fffcd27b9efff5a86ab942084c05924d.png",
                                    "name": "USD Coin",
                                    "optimized_symbol": "USDC",
                                    "price": 1.0,
                                    "protocol_id": "",
                                    "symbol": "USDC",
                                    "time_at": 1667248932.0
                                }
                            ]
                        },
                        "detail_types": [
                            "common"
                        ],
                        "name": "Yield",
                        "pool": {
                            "adapter_id": "beefy_yield",
                            "chain": "arb",
                            "controller": "0x9dbbbaecacedf53d5caa295b8293c1def2055adc",
                            "id": "0x9dbbbaecacedf53d5caa295b8293c1def2055adc",
                            "index": None,
                            "project_id": "arb_beefy",
                            "time_at": 1666648497
                        },
                        "proxy_detail": {},
                        "stats": {
                            "asset_usd_value": 207.90750956281926,
                            "debt_usd_value": 0,
                            "net_usd_value": 207.90750956281926
                        },
                        "update_at": 1699697125.0
                    }
                ],
                "site_url": "https://app.beefy.com",
                "tag_ids": [
                    "yield_aggregator"
                ],
                "tvl": 27753037.136932474
            },
            {
                "chain": "arb",
                "dao_id": "equilibria",
                "has_supported_portfolio": True,
                "id": "arb_equilibria",
                "is_tvl": False,
                "is_visible_in_defi": None,
                "logo_url": "https://static.debank.com/image/project/logo_url/equilibria/7a7b04b1f607ec66798898c008b87046.png",
                "name": "Equilibria",
                "platform_token_id": "0xbfbcfe8873fe28dfa25f1099282b088d52bbad9c",
                "portfolio_item_list": [
                    {
                        "asset_dict": {
                            "0x0c880f6761f1af8d9aa9c466984b80dab9a8c9e8": 2.904012434853993,
                            "0x80c12d5b6cc494632bf11b03f09436c8b61cc5df": 0.3542243746456424,
                            "0x96c4a48abdf781e9c931cfa92ec0167ba219ad8e": 4.13821771966694,
                            "0xbb33e51bdc598d710ff59fdf523e80ab7c882c83": 0.29670184839555724,
                            "0xbfbcfe8873fe28dfa25f1099282b088d52bbad9c": 1.3794059065556468
                        },
                        "asset_token_list": [
                            {
                                "amount": 0.3542243746456424,
                                "chain": "arb",
                                "decimals": 18,
                                "display_symbol": None,
                                "id": "0x80c12d5b6cc494632bf11b03f09436c8b61cc5df",
                                "is_core": False,
                                "is_verified": False,
                                "is_wallet": False,
                                "logo_url": None,
                                "name": "SY wstETH",
                                "optimized_symbol": "SY-wstETH",
                                "price": 2362.469723067711,
                                "protocol_id": "arb_pendle2",
                                "symbol": "SY-wstETH",
                                "time_at": 1686040154.0
                            },
                            {
                                "amount": 0.29670184839555724,
                                "chain": "arb",
                                "decimals": 18,
                                "display_symbol": None,
                                "id": "0xbb33e51bdc598d710ff59fdf523e80ab7c882c83",
                                "is_core": False,
                                "is_verified": False,
                                "is_wallet": False,
                                "logo_url": None,
                                "name": "PT wstETH 28DEC2023",
                                "optimized_symbol": "PT-wstETH-28DEC2023",
                                "price": 2052.1177166139805,
                                "protocol_id": "arb_pendle2",
                                "symbol": "PT-wstETH-28DEC2023",
                                "time_at": 1689662350.0
                            },
                            {
                                "amount": 2.904012434853993,
                                "chain": "arb",
                                "decimals": 18,
                                "display_symbol": None,
                                "id": "0x0c880f6761f1af8d9aa9c466984b80dab9a8c9e8",
                                "is_core": True,
                                "is_verified": True,
                                "is_wallet": True,
                                "logo_url": "https://static.debank.com/image/arb_token/logo_url/0x0c880f6761f1af8d9aa9c466984b80dab9a8c9e8/b9351f830cd0a6457e489b8c685f29ad.png",
                                "name": "Pendle",
                                "optimized_symbol": "PENDLE",
                                "price": 1.1538035999989722,
                                "protocol_id": "arb_pendle2",
                                "symbol": "PENDLE",
                                "time_at": 1671422822.0
                            },
                            {
                                "amount": 1.3794059065556468,
                                "chain": "arb",
                                "decimals": 18,
                                "display_symbol": None,
                                "id": "0xbfbcfe8873fe28dfa25f1099282b088d52bbad9c",
                                "is_core": True,
                                "is_verified": False,
                                "is_wallet": True,
                                "logo_url": "https://static.debank.com/image/arb_token/logo_url/0xbfbcfe8873fe28dfa25f1099282b088d52bbad9c/97ef2bbb1b00b710238cd6ddffc2334f.png",
                                "name": "Equilibria Token",
                                "optimized_symbol": "EQB",
                                "price": 0.1890280119398194,
                                "protocol_id": "arb_equilibria",
                                "symbol": "EQB",
                                "time_at": 1685677153.0
                            },
                            {
                                "amount": 4.13821771966694,
                                "chain": "arb",
                                "decimals": 18,
                                "display_symbol": None,
                                "id": "0x96c4a48abdf781e9c931cfa92ec0167ba219ad8e",
                                "is_core": True,
                                "is_verified": True,
                                "is_wallet": True,
                                "logo_url": "https://static.debank.com/image/arb_token/logo_url/0x96c4a48abdf781e9c931cfa92ec0167ba219ad8e/879c85f8f0133d12fbb1ef89e0130d65.png",
                                "name": "max EQB",
                                "optimized_symbol": "xEQB",
                                "price": 0,
                                "protocol_id": "arb_equilibria",
                                "symbol": "xEQB",
                                "time_at": 1685689532.0
                            }
                        ],
                        "detail": {
                            "reward_token_list": [
                                {
                                    "amount": 2.904012434853993,
                                    "chain": "arb",
                                    "decimals": 18,
                                    "display_symbol": None,
                                    "id": "0x0c880f6761f1af8d9aa9c466984b80dab9a8c9e8",
                                    "is_core": True,
                                    "is_verified": True,
                                    "is_wallet": True,
                                    "logo_url": "https://static.debank.com/image/arb_token/logo_url/0x0c880f6761f1af8d9aa9c466984b80dab9a8c9e8/b9351f830cd0a6457e489b8c685f29ad.png",
                                    "name": "Pendle",
                                    "optimized_symbol": "PENDLE",
                                    "price": 1.1538035999989722,
                                    "protocol_id": "arb_pendle2",
                                    "symbol": "PENDLE",
                                    "time_at": 1671422822.0
                                },
                                {
                                    "amount": 1.3794059065556468,
                                    "chain": "arb",
                                    "decimals": 18,
                                    "display_symbol": None,
                                    "id": "0xbfbcfe8873fe28dfa25f1099282b088d52bbad9c",
                                    "is_core": True,
                                    "is_verified": False,
                                    "is_wallet": True,
                                    "logo_url": "https://static.debank.com/image/arb_token/logo_url/0xbfbcfe8873fe28dfa25f1099282b088d52bbad9c/97ef2bbb1b00b710238cd6ddffc2334f.png",
                                    "name": "Equilibria Token",
                                    "optimized_symbol": "EQB",
                                    "price": 0.1890280119398194,
                                    "protocol_id": "arb_equilibria",
                                    "symbol": "EQB",
                                    "time_at": 1685677153.0
                                },
                                {
                                    "amount": 4.13821771966694,
                                    "chain": "arb",
                                    "decimals": 18,
                                    "display_symbol": None,
                                    "id": "0x96c4a48abdf781e9c931cfa92ec0167ba219ad8e",
                                    "is_core": True,
                                    "is_verified": True,
                                    "is_wallet": True,
                                    "logo_url": "https://static.debank.com/image/arb_token/logo_url/0x96c4a48abdf781e9c931cfa92ec0167ba219ad8e/879c85f8f0133d12fbb1ef89e0130d65.png",
                                    "name": "max EQB",
                                    "optimized_symbol": "xEQB",
                                    "price": 0,
                                    "protocol_id": "arb_equilibria",
                                    "symbol": "xEQB",
                                    "time_at": 1685689532.0
                                }
                            ],
                            "supply_token_list": [
                                {
                                    "amount": 0.3542243746456424,
                                    "chain": "arb",
                                    "decimals": 18,
                                    "display_symbol": None,
                                    "id": "0x80c12d5b6cc494632bf11b03f09436c8b61cc5df",
                                    "is_core": False,
                                    "is_verified": False,
                                    "is_wallet": False,
                                    "logo_url": None,
                                    "name": "SY wstETH",
                                    "optimized_symbol": "SY-wstETH",
                                    "price": 2362.469723067711,
                                    "protocol_id": "arb_pendle2",
                                    "symbol": "SY-wstETH",
                                    "time_at": 1686040154.0
                                },
                                {
                                    "amount": 0.29670184839555724,
                                    "chain": "arb",
                                    "decimals": 18,
                                    "display_symbol": None,
                                    "id": "0xbb33e51bdc598d710ff59fdf523e80ab7c882c83",
                                    "is_core": False,
                                    "is_verified": False,
                                    "is_wallet": False,
                                    "logo_url": None,
                                    "name": "PT wstETH 28DEC2023",
                                    "optimized_symbol": "PT-wstETH-28DEC2023",
                                    "price": 2052.1177166139805,
                                    "protocol_id": "arb_pendle2",
                                    "symbol": "PT-wstETH-28DEC2023",
                                    "time_at": 1689662350.0
                                }
                            ]
                        },
                        "detail_types": [
                            "common"
                        ],
                        "name": "Staked",
                        "pool": {
                            "adapter_id": "equilibria_pool_staked",
                            "chain": "arb",
                            "controller": "0x4d32c8ff2facc771ec7efc70d6a8468bc30c26bf",
                            "id": "0x4d32c8ff2facc771ec7efc70d6a8468bc30c26bf:10",
                            "index": "10",
                            "project_id": "arb_equilibria",
                            "time_at": 1685689476
                        },
                        "proxy_detail": {},
                        "stats": {
                            "asset_usd_value": 1449.322886275513,
                            "debt_usd_value": 0,
                            "net_usd_value": 1449.322886275513
                        },
                        "update_at": 1699697125.0
                    }
                ],
                "site_url": "https://equilibria.fi",
                "tag_ids": [
                    "asset_management"
                ],
                "tvl": 14187255.141101146
            },
            {
                "chain": "arb",
                "dao_id": "gmx",
                "has_supported_portfolio": True,
                "id": "arb_gmx",
                "is_tvl": False,
                "is_visible_in_defi": None,
                "logo_url": "https://static.debank.com/image/project/logo_url/arb_gmx/1a57f390512f4fe108c2b7155dc1fb6d.png",
                "name": "GMX",
                "platform_token_id": "0xfc5a1a6eb076a2c7ad06ed22c90d7e710e35ad0a",
                "portfolio_item_list": [
                    {
                        "asset_dict": {
                            "0x17fc002b466eec40dae837fc4be5c67993ddbd6f": 0.0,
                            "0x2f2a2543b76a4166549f7aab2e75bef0aefc5b0f": 0.0,
                            "0x82af49447d8a07e3bd95bd0d56f35241523fbab1": 0.0,
                            "0xaf88d065e77c8cc2239327c5edb3a432268e5831": 0.0,
                            "0xda10009cbd5d07dd0cecc66161fc93d7c9000da1": 0.0,
                            "0xf42ae1d54fd613c9bb14810b0588faaa09a426ca": 0.0,
                            "0xf97f4df75117a78c1a5a0dbb814af92458539fb4": 0.0,
                            "0xfa7f8980b0f1e64a2062791cc3b0871572f1f7f0": 0.0,
                            "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9": 0.0,
                            "0xfea7a6a0b346362bf88a9e4a88416b77a57d6c2a": 0.0,
                            "0xff970a61a04b1ca14834a43f5de4533ebddb5cc8": 0.0,
                            "arb": 1.7968194998e-08
                        },
                        "asset_token_list": [
                            {
                                "amount": 0.0,
                                "chain": "arb",
                                "decimals": 8,
                                "display_symbol": None,
                                "id": "0x2f2a2543b76a4166549f7aab2e75bef0aefc5b0f",
                                "is_core": True,
                                "is_verified": True,
                                "is_wallet": True,
                                "logo_url": "https://static.debank.com/image/arb_token/logo_url/0x2f2a2543b76a4166549f7aab2e75bef0aefc5b0f/d3c52e7c7449afa8bd4fad1c93f50d93.png",
                                "name": "Wrapped BTC",
                                "optimized_symbol": "WBTC",
                                "price": 37017.8,
                                "protocol_id": "",
                                "symbol": "WBTC",
                                "time_at": 1623867469.0
                            },
                            {
                                "amount": 0.0,
                                "chain": "arb",
                                "decimals": 18,
                                "display_symbol": None,
                                "id": "0x82af49447d8a07e3bd95bd0d56f35241523fbab1",
                                "is_core": True,
                                "is_verified": True,
                                "is_wallet": True,
                                "logo_url": "https://static.debank.com/image/arb_token/logo_url/0x82af49447d8a07e3bd95bd0d56f35241523fbab1/61844453e63cf81301f845d7864236f6.png",
                                "name": "Wrapped Ether",
                                "optimized_symbol": "WETH",
                                "price": 2061.09,
                                "protocol_id": "",
                                "symbol": "WETH",
                                "time_at": 1622346702.0
                            },
                            {
                                "amount": 0.0,
                                "chain": "arb",
                                "decimals": 6,
                                "display_symbol": "USDC(Bridged)",
                                "id": "0xff970a61a04b1ca14834a43f5de4533ebddb5cc8",
                                "is_core": True,
                                "is_verified": True,
                                "is_wallet": True,
                                "logo_url": "https://static.debank.com/image/coin/logo_url/usdc/e87790bfe0b3f2ea855dc29069b38818.png",
                                "name": "USD Coin (Arb1)",
                                "optimized_symbol": "USDC(Bridged)",
                                "price": 1.0,
                                "protocol_id": "arb_tracer",
                                "symbol": "USDC",
                                "time_at": 1623868379.0
                            },
                            {
                                "amount": 0.0,
                                "chain": "arb",
                                "decimals": 18,
                                "display_symbol": None,
                                "id": "0xf97f4df75117a78c1a5a0dbb814af92458539fb4",
                                "is_core": True,
                                "is_verified": True,
                                "is_wallet": True,
                                "logo_url": "https://static.debank.com/image/arb_token/logo_url/0xf97f4df75117a78c1a5a0dbb814af92458539fb4/69425617db0ef93a7c21c4f9b81c7ca5.png",
                                "name": "ChainLink Token",
                                "optimized_symbol": "LINK",
                                "price": 15.038783670009687,
                                "protocol_id": "",
                                "symbol": "LINK",
                                "time_at": 1623867040.0
                            },
                            {
                                "amount": 0.0,
                                "chain": "arb",
                                "decimals": 18,
                                "display_symbol": None,
                                "id": "0xfa7f8980b0f1e64a2062791cc3b0871572f1f7f0",
                                "is_core": True,
                                "is_verified": True,
                                "is_wallet": True,
                                "logo_url": "https://static.debank.com/image/arb_token/logo_url/0xfa7f8980b0f1e64a2062791cc3b0871572f1f7f0/fcee0c46fc9864f48ce6a40ed1cdd135.png",
                                "name": "Uniswap",
                                "optimized_symbol": "UNI",
                                "price": 5.390626390213456,
                                "protocol_id": "arb_uniswap3",
                                "symbol": "UNI",
                                "time_at": 1623867248.0
                            },
                            {
                                "amount": 0.0,
                                "chain": "arb",
                                "decimals": 6,
                                "display_symbol": None,
                                "id": "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9",
                                "is_core": True,
                                "is_verified": True,
                                "is_wallet": True,
                                "logo_url": "https://static.debank.com/image/coin/logo_url/usdt/23af7472292cb41dc39b3f1146ead0fe.png",
                                "name": "Tether USD",
                                "optimized_symbol": "USDT",
                                "price": 1.000495,
                                "protocol_id": "arb_rhino",
                                "symbol": "USDT",
                                "time_at": 1630432123.0
                            },
                            {
                                "amount": 0.0,
                                "chain": "arb",
                                "decimals": 18,
                                "display_symbol": None,
                                "id": "0xfea7a6a0b346362bf88a9e4a88416b77a57d6c2a",
                                "is_core": True,
                                "is_verified": True,
                                "is_wallet": True,
                                "logo_url": "https://static.debank.com/image/arb_token/logo_url/0xfea7a6a0b346362bf88a9e4a88416b77a57d6c2a/7d0c0fb6eab1b7a8a9bfb7dcc04cb11e.png",
                                "name": "Magic Internet Money",
                                "optimized_symbol": "MIM",
                                "price": 0.9953961290010743,
                                "protocol_id": "arb_multichain",
                                "symbol": "MIM",
                                "time_at": 1631595191.0
                            },
                            {
                                "amount": 0.0,
                                "chain": "arb",
                                "decimals": 18,
                                "display_symbol": None,
                                "id": "0x17fc002b466eec40dae837fc4be5c67993ddbd6f",
                                "is_core": True,
                                "is_verified": True,
                                "is_wallet": True,
                                "logo_url": "https://static.debank.com/image/arb_token/logo_url/0x17fc002b466eec40dae837fc4be5c67993ddbd6f/4f323e33bfffa864c577e7bd2a3257c9.png",
                                "name": "Frax",
                                "optimized_symbol": "FRAX",
                                "price": 0.9989999971001299,
                                "protocol_id": "arb_frax",
                                "symbol": "FRAX",
                                "time_at": 1632766868.0
                            },
                            {
                                "amount": 0.0,
                                "chain": "arb",
                                "decimals": 18,
                                "display_symbol": None,
                                "id": "0xda10009cbd5d07dd0cecc66161fc93d7c9000da1",
                                "is_core": True,
                                "is_verified": True,
                                "is_wallet": True,
                                "logo_url": "https://static.debank.com/image/arb_token/logo_url/0xda10009cbd5d07dd0cecc66161fc93d7c9000da1/549c4205dbb199f1b8b03af783f35e71.png",
                                "name": "Dai Stablecoin",
                                "optimized_symbol": "DAI",
                                "price": 0.99995,
                                "protocol_id": "",
                                "symbol": "DAI",
                                "time_at": 1632133487.0
                            },
                            {
                                "amount": 0.0,
                                "chain": "arb",
                                "decimals": 6,
                                "display_symbol": None,
                                "id": "0xaf88d065e77c8cc2239327c5edb3a432268e5831",
                                "is_core": True,
                                "is_verified": True,
                                "is_wallet": True,
                                "logo_url": "https://static.debank.com/image/arb_token/logo_url/0xaf88d065e77c8cc2239327c5edb3a432268e5831/fffcd27b9efff5a86ab942084c05924d.png",
                                "name": "USD Coin",
                                "optimized_symbol": "USDC",
                                "price": 1.0,
                                "protocol_id": "",
                                "symbol": "USDC",
                                "time_at": 1667248932.0
                            },
                            {
                                "amount": 0.0,
                                "chain": "arb",
                                "decimals": 18,
                                "display_symbol": None,
                                "id": "0xf42ae1d54fd613c9bb14810b0588faaa09a426ca",
                                "is_core": True,
                                "is_verified": True,
                                "is_wallet": True,
                                "logo_url": "https://static.debank.com/image/arb_token/logo_url/0xf42ae1d54fd613c9bb14810b0588faaa09a426ca/28fd1e74e9f42ad073992bc8359a073a.png",
                                "name": "Escrowed GMX",
                                "optimized_symbol": "esGMX",
                                "price": 0,
                                "protocol_id": "arb_gmx",
                                "symbol": "esGMX",
                                "time_at": 1626958493.0
                            },
                            {
                                "amount": 1.7968194998e-08,
                                "chain": "arb",
                                "decimals": 18,
                                "display_symbol": None,
                                "id": "arb",
                                "is_core": True,
                                "is_verified": True,
                                "is_wallet": True,
                                "logo_url": "https://static.debank.com/image/arb_token/logo_url/arb/d61441782d4a08a7479d54aea211679e.png",
                                "name": "ETH",
                                "optimized_symbol": "ETH",
                                "price": 2061.09,
                                "protocol_id": "",
                                "symbol": "ETH",
                                "time_at": 1622131200.0
                            }
                        ],
                        "detail": {
                            "reward_token_list": [
                                {
                                    "amount": 0.0,
                                    "chain": "arb",
                                    "decimals": 18,
                                    "display_symbol": None,
                                    "id": "0xf42ae1d54fd613c9bb14810b0588faaa09a426ca",
                                    "is_core": True,
                                    "is_verified": True,
                                    "is_wallet": True,
                                    "logo_url": "https://static.debank.com/image/arb_token/logo_url/0xf42ae1d54fd613c9bb14810b0588faaa09a426ca/28fd1e74e9f42ad073992bc8359a073a.png",
                                    "name": "Escrowed GMX",
                                    "optimized_symbol": "esGMX",
                                    "price": 0,
                                    "protocol_id": "arb_gmx",
                                    "symbol": "esGMX",
                                    "time_at": 1626958493.0
                                },
                                {
                                    "amount": 1.7968194998e-08,
                                    "chain": "arb",
                                    "decimals": 18,
                                    "display_symbol": None,
                                    "id": "arb",
                                    "is_core": True,
                                    "is_verified": True,
                                    "is_wallet": True,
                                    "logo_url": "https://static.debank.com/image/arb_token/logo_url/arb/d61441782d4a08a7479d54aea211679e.png",
                                    "name": "ETH",
                                    "optimized_symbol": "ETH",
                                    "price": 2061.09,
                                    "protocol_id": "",
                                    "symbol": "ETH",
                                    "time_at": 1622131200.0
                                }
                            ],
                            "supply_token_list": [
                                {
                                    "amount": 0.0,
                                    "chain": "arb",
                                    "decimals": 8,
                                    "display_symbol": None,
                                    "id": "0x2f2a2543b76a4166549f7aab2e75bef0aefc5b0f",
                                    "is_core": True,
                                    "is_verified": True,
                                    "is_wallet": True,
                                    "logo_url": "https://static.debank.com/image/arb_token/logo_url/0x2f2a2543b76a4166549f7aab2e75bef0aefc5b0f/d3c52e7c7449afa8bd4fad1c93f50d93.png",
                                    "name": "Wrapped BTC",
                                    "optimized_symbol": "WBTC",
                                    "price": 37017.8,
                                    "protocol_id": "",
                                    "symbol": "WBTC",
                                    "time_at": 1623867469.0
                                },
                                {
                                    "amount": 0.0,
                                    "chain": "arb",
                                    "decimals": 18,
                                    "display_symbol": None,
                                    "id": "0x82af49447d8a07e3bd95bd0d56f35241523fbab1",
                                    "is_core": True,
                                    "is_verified": True,
                                    "is_wallet": True,
                                    "logo_url": "https://static.debank.com/image/arb_token/logo_url/0x82af49447d8a07e3bd95bd0d56f35241523fbab1/61844453e63cf81301f845d7864236f6.png",
                                    "name": "Wrapped Ether",
                                    "optimized_symbol": "WETH",
                                    "price": 2061.09,
                                    "protocol_id": "",
                                    "symbol": "WETH",
                                    "time_at": 1622346702.0
                                },
                                {
                                    "amount": 0.0,
                                    "chain": "arb",
                                    "decimals": 6,
                                    "display_symbol": "USDC(Bridged)",
                                    "id": "0xff970a61a04b1ca14834a43f5de4533ebddb5cc8",
                                    "is_core": True,
                                    "is_verified": True,
                                    "is_wallet": True,
                                    "logo_url": "https://static.debank.com/image/coin/logo_url/usdc/e87790bfe0b3f2ea855dc29069b38818.png",
                                    "name": "USD Coin (Arb1)",
                                    "optimized_symbol": "USDC(Bridged)",
                                    "price": 1.0,
                                    "protocol_id": "arb_tracer",
                                    "symbol": "USDC",
                                    "time_at": 1623868379.0
                                },
                                {
                                    "amount": 0.0,
                                    "chain": "arb",
                                    "decimals": 18,
                                    "display_symbol": None,
                                    "id": "0xf97f4df75117a78c1a5a0dbb814af92458539fb4",
                                    "is_core": True,
                                    "is_verified": True,
                                    "is_wallet": True,
                                    "logo_url": "https://static.debank.com/image/arb_token/logo_url/0xf97f4df75117a78c1a5a0dbb814af92458539fb4/69425617db0ef93a7c21c4f9b81c7ca5.png",
                                    "name": "ChainLink Token",
                                    "optimized_symbol": "LINK",
                                    "price": 15.038783670009687,
                                    "protocol_id": "",
                                    "symbol": "LINK",
                                    "time_at": 1623867040.0
                                },
                                {
                                    "amount": 0.0,
                                    "chain": "arb",
                                    "decimals": 18,
                                    "display_symbol": None,
                                    "id": "0xfa7f8980b0f1e64a2062791cc3b0871572f1f7f0",
                                    "is_core": True,
                                    "is_verified": True,
                                    "is_wallet": True,
                                    "logo_url": "https://static.debank.com/image/arb_token/logo_url/0xfa7f8980b0f1e64a2062791cc3b0871572f1f7f0/fcee0c46fc9864f48ce6a40ed1cdd135.png",
                                    "name": "Uniswap",
                                    "optimized_symbol": "UNI",
                                    "price": 5.390626390213456,
                                    "protocol_id": "arb_uniswap3",
                                    "symbol": "UNI",
                                    "time_at": 1623867248.0
                                },
                                {
                                    "amount": 0.0,
                                    "chain": "arb",
                                    "decimals": 6,
                                    "display_symbol": None,
                                    "id": "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9",
                                    "is_core": True,
                                    "is_verified": True,
                                    "is_wallet": True,
                                    "logo_url": "https://static.debank.com/image/coin/logo_url/usdt/23af7472292cb41dc39b3f1146ead0fe.png",
                                    "name": "Tether USD",
                                    "optimized_symbol": "USDT",
                                    "price": 1.000495,
                                    "protocol_id": "arb_rhino",
                                    "symbol": "USDT",
                                    "time_at": 1630432123.0
                                },
                                {
                                    "amount": 0.0,
                                    "chain": "arb",
                                    "decimals": 18,
                                    "display_symbol": None,
                                    "id": "0xfea7a6a0b346362bf88a9e4a88416b77a57d6c2a",
                                    "is_core": True,
                                    "is_verified": True,
                                    "is_wallet": True,
                                    "logo_url": "https://static.debank.com/image/arb_token/logo_url/0xfea7a6a0b346362bf88a9e4a88416b77a57d6c2a/7d0c0fb6eab1b7a8a9bfb7dcc04cb11e.png",
                                    "name": "Magic Internet Money",
                                    "optimized_symbol": "MIM",
                                    "price": 0.9953961290010743,
                                    "protocol_id": "arb_multichain",
                                    "symbol": "MIM",
                                    "time_at": 1631595191.0
                                },
                                {
                                    "amount": 0.0,
                                    "chain": "arb",
                                    "decimals": 18,
                                    "display_symbol": None,
                                    "id": "0x17fc002b466eec40dae837fc4be5c67993ddbd6f",
                                    "is_core": True,
                                    "is_verified": True,
                                    "is_wallet": True,
                                    "logo_url": "https://static.debank.com/image/arb_token/logo_url/0x17fc002b466eec40dae837fc4be5c67993ddbd6f/4f323e33bfffa864c577e7bd2a3257c9.png",
                                    "name": "Frax",
                                    "optimized_symbol": "FRAX",
                                    "price": 0.9989999971001299,
                                    "protocol_id": "arb_frax",
                                    "symbol": "FRAX",
                                    "time_at": 1632766868.0
                                },
                                {
                                    "amount": 0.0,
                                    "chain": "arb",
                                    "decimals": 18,
                                    "display_symbol": None,
                                    "id": "0xda10009cbd5d07dd0cecc66161fc93d7c9000da1",
                                    "is_core": True,
                                    "is_verified": True,
                                    "is_wallet": True,
                                    "logo_url": "https://static.debank.com/image/arb_token/logo_url/0xda10009cbd5d07dd0cecc66161fc93d7c9000da1/549c4205dbb199f1b8b03af783f35e71.png",
                                    "name": "Dai Stablecoin",
                                    "optimized_symbol": "DAI",
                                    "price": 0.99995,
                                    "protocol_id": "",
                                    "symbol": "DAI",
                                    "time_at": 1632133487.0
                                },
                                {
                                    "amount": 0.0,
                                    "chain": "arb",
                                    "decimals": 6,
                                    "display_symbol": None,
                                    "id": "0xaf88d065e77c8cc2239327c5edb3a432268e5831",
                                    "is_core": True,
                                    "is_verified": True,
                                    "is_wallet": True,
                                    "logo_url": "https://static.debank.com/image/arb_token/logo_url/0xaf88d065e77c8cc2239327c5edb3a432268e5831/fffcd27b9efff5a86ab942084c05924d.png",
                                    "name": "USD Coin",
                                    "optimized_symbol": "USDC",
                                    "price": 1.0,
                                    "protocol_id": "",
                                    "symbol": "USDC",
                                    "time_at": 1667248932.0
                                }
                            ]
                        },
                        "detail_types": [
                            "common"
                        ],
                        "name": "Staked",
                        "pool": {
                            "adapter_id": "gmx_staking",
                            "chain": "arb",
                            "controller": "0x1addd80e6039594ee970e5872d247bf0414c8903",
                            "id": "0x1addd80e6039594ee970e5872d247bf0414c8903:0x4e971a87900b931ff39d1aad67697f49835400b6",
                            "index": "0x4e971a87900b931ff39d1aad67697f49835400b6",
                            "project_id": "arb_gmx",
                            "time_at": 1628757069
                        },
                        "proxy_detail": {},
                        "stats": {
                            "asset_usd_value": 3.703406702842782e-05,
                            "debt_usd_value": 0,
                            "net_usd_value": 3.703406702842782e-05
                        },
                        "update_at": 1699697125.0
                    }
                ],
                "site_url": "https://gmx.io",
                "tag_ids": [
                    "perpetuals"
                ],
                "tvl": 678471573.0494703
            }
        ],
        "error_code": 0
    }
