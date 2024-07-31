from components import *
from typing import Union, List
import pandas as pd
import itertools


def cartesian_product(elements):
    products = list(itertools.product(*elements))
    return products

def print_approximation(approximation: dict):
    for key, value in approximation.items():
        print(f"Predicate: {key}\n")
        if isinstance(value, pd.DataFrame):
            print(value.to_string(index=False, header=False))
        elif isinstance(value, bool):
            print(value)
        print("\n" + "="*40 + "\n")

def gather_all_keys(dicts):
    """Collect all unique keys from a list of dictionaries."""
    all_keys = set()
    for d in dicts:
        if d.keys():
            all_keys.update(d.keys())
    return list(all_keys)


def generate_dict_combinations(all_keys, possible_values):
    value_combinations = list(itertools.product(possible_values, repeat=len(all_keys)))
    dict_combinations = [dict(zip(all_keys, values)) for values in value_combinations]
    return dict_combinations

def remove_rows_with_k(data, k):
  return [row for row in data if k != {key: value for key, value in row.items() if key in k}]


def remove_nan_keys(d):
    return {k: v for k, v in d.items() if pd.notna(v)}

def make_hashable(value):
    if isinstance(value, dict):
        return frozenset((make_hashable(k), make_hashable(v)) for k, v in value.items())
    elif isinstance(value, (list, set, tuple)):
        return tuple(make_hashable(x) for x in value)
    return value

def hashable(row):
    return tuple((k, make_hashable(v)) for k, v in row.items())

    
def group_rules_by_head(rules: List[str]) -> dict[str, List[str]]:
    rule_dict = {}

    for rule in rules:
        if rule.head.predicate not in rule_dict:
            rule_dict[rule.head.predicate] = []
        rule_dict[rule.head.predicate].append(rule)

    return rule_dict

