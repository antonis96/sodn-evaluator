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

def filter_rules_without_idb_predicates(program, mode):
    idb_predicates = {rule.head.predicate for rule in program.rules}
    
    filtered_rules = []
    for rule in program.rules:
        has_idb_predicate = any(literal.atom.predicate in idb_predicates for literal in rule.body)
        if not has_idb_predicate:
            filtered_rules.append(rule)
    
    filtered_program = Program(
        types={f"{mode}_{k}": t for k, t in program.types.items()},
        predicates=[f"{mode}_{p}" for p in program.predicates]
    )
    for r in filtered_rules:
        filtered_program.add_rule(r)
    
    return filtered_program
    
def group_rules_by_head(rules: List[str]) -> dict[str, List[str]]:
    rule_dict = {}

    for rule in rules:
        if rule.head.predicate not in rule_dict:
            rule_dict[rule.head.predicate] = []
        rule_dict[rule.head.predicate].append(rule)

    return rule_dict


def compare_dicts_of_dataframes(dict1: dict, dict2: dict) -> bool:
    if dict1.keys() != dict2.keys():
        return False

    for key in dict1:
        value1 = dict1[key]
        value2 = dict2[key]

        if isinstance(value1, bool) and isinstance(value2, bool):
            if value1 != value2:
                return False
        elif isinstance(value1, pd.DataFrame) and isinstance(value2, pd.DataFrame):
            if not value1.equals(value2):
                return False
            
    return True

