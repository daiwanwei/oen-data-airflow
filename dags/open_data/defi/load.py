import os

import psycopg2

from ..utils.db_utils import insert_to_db

INSERT_ASSET_QUERY = """
INSERT INTO defi_historical_assets (
    owner_address, chain, symbol, usd_value,amount,
     price, asset_type, is_debt, project, recorded_at
)
VALUES (
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s
    );
"""


def load_assets_to_db(conn: psycopg2.extensions.connection, csv_file: str):
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f'{csv_file} not found')
    params = (
        'owner_address', 'chain', 'symbol', 'usd_value', 'amount',
        'price', 'asset_type', 'is_debt', 'project', 'recorded_at'
    )
    insert_to_db(conn, csv_file, INSERT_ASSET_QUERY, params)
