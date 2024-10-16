from components import *
from typing import Union, List
import pandas as pd
import itertools


def cartesian_product(elements):
    products = list(itertools.product(*elements))
    return products


def get_approximation_string(approximation: dict) -> str:
    result = []
    for key, value in approximation.items():
        result.append(f"Predicate: {key}\n")
        if isinstance(value, pd.DataFrame):
            result.append(value.to_string(index=False, header=False))
        elif isinstance(value, bool):
            result.append(str(value))
        result.append("\n" + "="*40 + "\n")
    return "\n".join(result)


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



def replace_dict_values(d):
    dict_variants = []
    for r in range(1, len(d) + 1):
        for key_subset in itertools.combinations(d, r):
            variant_queue = [d.copy()]
            for key in key_subset:
                variant_queue = [
                    {**variant, key: '0' if variant[key] == '1' else '1'}
                    for variant in variant_queue
                ]
            dict_variants.extend(variant_queue)
    return dict_variants


def create_variations(row, binary_strings, herbrand_universe):
    original_dict = row.to_dict()
    keys = list(original_dict.keys())
    variations_set = set()

    for binary_string in binary_strings:
        current_variations = []
        for bit, key in zip(binary_string, keys):
            value = original_dict[key]
            if bit == 1:
                if isinstance(value, dict):
                    # Get all possible variations for the dictionary
                    possible_values = replace_dict_values(value)
                    # Convert each dictionary to a tuple for hashability
                    possible_values = [tuple(sorted(v.items())) for v in possible_values]
                else:
                    possible_values = [val for val in herbrand_universe if val != value]
                current_variations.append(possible_values)
            else:
                if isinstance(value, dict):
                    current_variations.append([tuple(sorted(value.items()))])
                else:
                    current_variations.append([value])

        # Add all combinations as tuples to the set for uniqueness
        variations_set.update(itertools.product(*current_variations))

    # Convert the set of variations back to a DataFrame
    variations_list = []
    for variation in variations_set:
        variation_dict = {}
        for key, val in zip(keys, variation):
            if isinstance(val, tuple):
                # Convert tuples back to dictionaries
                variation_dict[key] = dict(val)
            else:
                variation_dict[key] = val
        variations_list.append(variation_dict)

    return pd.DataFrame(variations_list)