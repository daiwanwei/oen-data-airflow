from datetime import datetime
from typing import Callable

import pandas as pd
from airflow.operators.python import get_current_context


def get_execution_date() -> datetime:
    context = get_current_context()
    execution_date = context['execution_date']
    return execution_date


def gen_ts_filename(filepath: str) -> str:
    execution_date = get_execution_date()
    ts = datetime.timestamp(execution_date)
    filename = filepath.replace('.csv', f'_{ts}.csv')
    return filename


def collect_item_from_dict_list(dict_list: list[dict], key: str) -> list[any]:
    item_set = set()
    for item in dict_list:
        item_set.add(item[key])
    return list(item_set)


def filter_dict_list(dict_list: list[dict], key: list[str], check: list[Callable[[any], bool]]) -> list[dict]:
    filtered_list = []
    for item in dict_list:
        for i, k in enumerate(key):
            if not check[i](item[k]):
                break
            if i == len(key) - 1:
                filtered_list.append(item)
    return filtered_list


def save_to_csv(data: dict, csv_file: str):
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)