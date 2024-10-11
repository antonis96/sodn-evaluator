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



# Function to get all possible combinations of replacing keys in a dictionary
def replace_dict_values(d, mode):
    keys = list(d.keys())
    dict_variants = []
    # Loop through each possible combination of key replacements (1 key, 2 keys, ..., n keys)
    for r in range(1, len(keys) + 1):
        for key_subset in itertools.combinations(keys, r):
            # Generate different versions of new_dict for each key
            new_dict_options = [d.copy()]
            for key in key_subset:
                if d[key] == '1':
                    # Create new variants for '0'
                    new_variants = []
                    for variant in new_dict_options:
                        variant_0 = variant.copy()
                        variant_0[key] = '0'
                        new_variants.extend([variant_0])
                    new_dict_options = new_variants
                elif d[key] == '0':
                    # Create new variants for '1'
                    new_variants = []
                    for variant in new_dict_options:
                        variant_1 = variant.copy()
                        variant_1[key] = '1'
                        new_variants.extend([variant_1])
                    new_dict_options = new_variants
            
            dict_variants.extend(new_dict_options)
    
    return dict_variants

# Function to get all possible string replacements
def replace_string_values(value, possible_values):
    return [v for v in possible_values if v != value]

# Function to determine how to generate variants based on the type of the value
def get_variants(value, herbrand_universe, mode):
    if isinstance(value, dict):
        return replace_dict_values(value, mode)
    elif isinstance(value, str):
        return replace_string_values(value, herbrand_universe)

def generate_variants_for_dataframe(df, predicate_type, args, vars, herbrand_universe, mode):
    # if df.empty:
    #     # Filter predicate_type based on whether its corresponding arg is in vars
    #     filtered_predicate_type = [
    #         element for element, arg in zip(predicate_type, args) if str(arg) in vars
    #     ]
        
    #     c = cartesian_product([
    #         herbrand_universe if not isinstance(element, list) else [
    #             {r: value} for r in list(itertools.combinations_with_replacement(herbrand_universe, len(element)))
    #             for value in ['0', '1/2', '1']
    #         ] for element in filtered_predicate_type
    #     ])

    #     return pd.DataFrame(c, columns=df.columns)
    
    all_variants = []
    initial_rows = df.to_dict(orient='records')  # Convert the original dataframe to a list of dicts (rows)
    
    for _, row in df.iterrows():
        column_variants = []
        
        # Generate variants for each column value
        for col in df.columns:
            variants = get_variants(row[col], herbrand_universe, mode)
            column_variants.append(variants)
        
        # Create all combinations of the variants across columns
        for variant_combination in itertools.product(*column_variants):
            variant_row = {col: variant_combination[i] for i, col in enumerate(df.columns)}
            if variant_row not in initial_rows:
            # Only add if the new row is not in the original dataframe
                all_variants.append(variant_row)
    return pd.DataFrame(all_variants)