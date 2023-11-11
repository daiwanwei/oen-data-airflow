from enum import Enum
import re


def transform_token_data(owner: str, token_data: dict, project: str) -> dict:
    asset_type = classify_asset_type(token_data['symbol'])
    usd_value = token_data['amount'] * token_data['price']
    is_debt = token_data['amount'] < 0
    return {
        'owner_address': owner,
        'chain': token_data['chain'],
        'symbol': token_data['symbol'],
        'usd_value': usd_value,
        'amount': token_data['amount'],
        'price': token_data['price'],
        'asset_type': asset_type.value,
        'is_debt': is_debt,
        'project': project
    }


def transform_project_data(owner: str, project_data: dict) -> list:
    asset_list = []
    for portfolio in project_data['portfolio_item_list']:
        for token in portfolio['asset_token_list']:
            asset_list.append(transform_token_data(owner,token, project_data['dao_id']))
    return asset_list


def transform_balance_data(owner: str, balance_data: list) -> list:
    asset_list = []
    for token in balance_data:
        asset_list.append(transform_token_data(owner,token, 'owner'))
    return asset_list


class AssetType(Enum):
    StableCoin = 'StableCoin'
    Coin = 'Coin'


def classify_asset_type(symbol: str) -> AssetType:
    symbol_l = symbol.lower()
    reg = re.compile(r'(usd)')
    if reg.search(symbol_l):
        return AssetType.StableCoin
    else:
        return AssetType.Coin