from components import *
from typing import Union, List
import pandas as pd
import itertools
import copy 
from functools import reduce
from itertools import product


H_u = {'a','b', 'c'}

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

def initialize_over_approximation(program: Program, predicate: str) -> pd.DataFrame:
    predicate_type = program.types[predicate]
    if predicate_type == 'o':
        return True
    else:  # if it is a list
        c = cartesian_product([
                H_u if not isinstance(element, list) else [
                {r: value} for r in list(itertools.combinations_with_replacement(H_u, len(element)))
                for value in ['0', '1/2', '1']
            ] for element in predicate_type
        ]) 
        df = pd.DataFrame(c)
        return df
    

def gather_all_keys(dicts):
    """Collect all unique keys from a list of dictionaries."""
    all_keys = set()
    for d in dicts:
        all_keys.update(d.keys())
    return list(all_keys)

# def generate_dict_combinations(d, possible_values):
#     """Generate all possible dictionary combinations by changing at least one value."""
#     if not d:
#         return [{}]
#     keys, current_values = zip(*d.items())
#     all_combinations = itertools.product(*[possible_values if val == current_value else [current_value] for val, current_value in zip(current_values, current_values)])
#     return [dict(zip(keys, combo)) for combo in all_combinations if combo != current_values]

def generate_dict_combinations(all_keys, possible_values):
    value_combinations = list(itertools.product(possible_values, repeat=len(all_keys)))
    dict_combinations = [dict(zip(all_keys, values)) for values in value_combinations]
    return dict_combinations

def remove_rows_with_k(data, k):
  return [row for row in data if k != {key: value for key, value in row.items() if key in k}]


def remove_nan_keys(d):
    """Remove keys with NaN values from a dictionary."""
    return {k: v for k, v in d.items() if pd.notna(v)}

def get_false_combinations(df, predicate_type):
    if df.empty:
        c = cartesian_product([
                H_u if not isinstance(element, list) else [
                {r: value} for r in list(itertools.combinations_with_replacement(H_u, len(element)))
                for value in ['0', '1/2', '1']
            ] for element in predicate_type
        ]) 
        return pd.DataFrame(c,columns=df.columns)
    

    dict_columns = [col for col in df.columns if isinstance(df[col].dropna().iloc[0], dict)]
    plain_columns = [col for col in df.columns if col not in dict_columns]

    # Handling dictionary columns
    dict_combinations = []
    for col in dict_columns:
        all_combos = []
        all_keys = gather_all_keys(df[col].dropna().tolist())
        all_combos.extend(generate_dict_combinations(all_keys, ['0', '1', '1/2']))
        for entry in df[col].dropna():

            all_combos = remove_rows_with_k(all_combos, entry)

        unique_combos = pd.DataFrame(all_combos).drop_duplicates().to_dict('records')
        dict_combinations.append(unique_combos)


    # Create Cartesian product of all column combinations
    all_combinations = list(itertools.product(*([ H_u for col in plain_columns] + dict_combinations)))

    # Convert combinations to DataFrame
    new_rows = pd.DataFrame(all_combinations, columns=plain_columns + dict_columns)

    # Convert rows to hashable form to facilitate comparison
    df_hashable = df.apply(hashable, axis=1)
    new_rows_hashable = new_rows.apply(hashable, axis=1)

    # Filter new rows to include only those not present in original df
    unique_new_rows = new_rows[~new_rows_hashable.isin(df_hashable)]

    # Use loc to remove NaN keys from dictionaries in the DataFrame safely
    for col in dict_columns:
        unique_new_rows.loc[:, col] = unique_new_rows[col].apply(remove_nan_keys)

    return unique_new_rows.reset_index(drop=True)


def initialize_under_approximation(program: Program, predicate: str) -> pd.DataFrame:
    predicate_type = program.types[predicate]
    if predicate_type == 'o':
        return False
    else:  # if it is a list
        c = cartesian_product([set() if not isinstance(element, list) else 
                [ dict() ] # maybe needs to change
        for element in predicate_type])        
        df = pd.DataFrame(c)
        return df


def evaluate_facts(program: Program, under_approximation: dict) -> dict:
    new_tuples = {key: [] for key in under_approximation.keys()}

    for fact in program.facts:
        if fact.head.predicate in under_approximation:
            new_tuples[fact.head.predicate].append(tuple([str(arg) for arg in fact.head.args]))
    
    for key in new_tuples.keys():
        if new_tuples[key]:
            under_approximation[key] = pd.DataFrame(new_tuples[key])

    return under_approximation


def atov(literal: Literal, types:dict, under_approximation: dict, over_approximation: dict) -> pd.DataFrame:
    return (
        constant_predicate_atov(literal, types[literal.atom.predicate], under_approximation, over_approximation)
        if literal.atom.predicate.islower()
        else variable_predicate_atov(literal)
    )    


def constant_predicate_atov(literal: Literal, atom_type:Union[str,list], under_approximation: dict, over_approximation: dict) -> Union[pd.DataFrame,bool]:
    atom = literal.atom
    predicate = atom.predicate
    args = tuple([str(arg.value) for arg in atom.args ])
    vars = [str(v) for v in tuple(atom.args) if v.value.isupper()]
    is_negated = literal.negated

    if predicate.startswith('dt_'):
        stored_df = under_approximation[predicate]
    else:
        stored_df = over_approximation[predicate]
    if atom_type == 'o':
        return stored_df if not is_negated else not stored_df
    
    if not vars:
        if is_negated:
            for row in stored_df.itertuples(index=False, name=None):
                sub, valid_sub = match(atom.args, row, under_approximation, over_approximation)
                if valid_sub:
                    return False
            return True
        else:
            for row in stored_df.itertuples(index=False, name=None):
                sub, valid_sub = match(atom.args, row, under_approximation, over_approximation)
                if valid_sub:
                    return True
            return False

    matches = []
    for row in stored_df.itertuples(index=False, name=None):
        sub, valid_sub = match(atom.args, row, under_approximation, over_approximation)
        if not valid_sub:
            continue
        matches.append(sub)
   
    matched_df = pd.DataFrame(matches,columns=vars)
    if not is_negated:
        return matched_df
    else:
        false_df = get_false_combinations(matched_df,atom_type)
        return false_df
    

def match(a: tuple, b:tuple, under_approximation: dict, over_approximation: dict):
    if len(a) != len(b):
        return {}, False
    sub = {}
    for ai, bi in zip(a, b):
        if ai.arg_type == 'data_const' and ai.value != bi:
            return {}, False
        elif ai.arg_type == 'predicate_const': #TODO
            dt_tuples = set(under_approximation[f"dt_{ai.value}"].apply(tuple, axis=1))
            ndf_tuples = set(over_approximation[f"ndf_{ai.value}"].apply(tuple, axis=1))
            def check_keys(dt_tuples, ndf_tuples, bi):
                for key, val in bi.items():
                    if val == '1' and key not in dt_tuples:
                        return False
                    if val == '1/2':
                        if not (key in ndf_tuples and key not in dt_tuples):
                            return False
                    if val == '0' :
                        if key in ndf_tuples:
                            return False      
                return True

            check = check_keys(dt_tuples, ndf_tuples, bi)
            if not check:
                return {}, False
                    
        if ai.arg_type == 'variable':
            if ai not in sub:
                sub[ai.value] = bi
            elif isinstance(ai, str) and sub[ai.value] != bi:
                return {}, False
    return sub, True


def variable_predicate_atov(literal: Literal) -> pd.DataFrame:
    atom = literal.atom
    predicate = atom.predicate
    args = tuple([str(arg.value) for arg in atom.args ])
    arg_vars = [str(v) for v in tuple(atom.args) if v.value.isupper()]
    arg_constants = [const for const in args if const not in arg_vars]
    is_negated = literal.negated

    var_subs = list(itertools.product(H_u, repeat=len(arg_vars))) # possible substitutions of argument variables
    df = pd.DataFrame(var_subs, columns=arg_vars)

    # Function to expand a row
    def expand_row(row, vals):
        return [row.tolist() + [{tuple(row.loc[i] if i in arg_vars else i for i in args): v}] for v in vals]
    
    if predicate.startswith('dt_'):
        predicate = predicate.split("_")[-1]
        if not is_negated:
            if df.empty:
                data = [
                    { tuple(args): '1'},
                ]
                df = pd.DataFrame( {predicate:data})
            else:
                expanded_data = df.apply(lambda row: expand_row(row, ['1']), axis=1).tolist()
                expanded_data_flat = [item for sublist in expanded_data for item in sublist]

                df = pd.DataFrame(expanded_data_flat, columns=list(df.columns) + [predicate])
        else:
            if df.empty:
                data = [
                    { tuple(args): '0'},
                    { tuple(args): '1/2'},
                ]
                df = pd.DataFrame( {predicate:data})

            else:
                expanded_data = df.apply(lambda row: expand_row(row, ['0', '1/2']), axis=1).tolist()
                expanded_data_flat = [item for sublist in expanded_data for item in sublist]

                df = pd.DataFrame(expanded_data_flat, columns=list(df.columns) + [predicate])

    else:
        predicate = predicate.split("_")[-1]
        if not is_negated:
            if df.empty:
                data = [
                    { tuple(args): '1'},
                    { tuple(args): '1/2'}
                ]
                df = pd.DataFrame( {predicate:data})
            else:
                expanded_data = df.apply(lambda row: expand_row(row, ['1','1/2']), axis=1).tolist()
                expanded_data_flat = [item for sublist in expanded_data for item in sublist]

                df = pd.DataFrame(expanded_data_flat, columns=list(df.columns) + [predicate])
        else:
            if df.empty:
                data = [
                    { tuple(args): '0'},
                ]
                df = pd.DataFrame( {predicate:data})
            else:
                expanded_data = df.apply(lambda row: expand_row(row, ['0']), axis=1).tolist()
                expanded_data_flat = [item for sublist in expanded_data for item in sublist]

                df = pd.DataFrame(expanded_data_flat, columns=list(df.columns) + [predicate])

    return df



def combine_literal_evaluations(literal_evaluations: List[Union[pd.DataFrame,bool]]) -> Union[pd.DataFrame,bool]:
    if not literal_evaluations:
        return pd.DataFrame()  # Return an empty dataframe if the list is empty

    # Filter out boolean values, check for False, and check for empty dataframes
    for eval in literal_evaluations:
        if isinstance(eval, bool):
            if eval is False:
                return False
        elif isinstance(eval, pd.DataFrame):
            if eval.empty:
                return False
    
    # Collect non-empty dataframes
    dfs = [df for df in literal_evaluations if isinstance(df, pd.DataFrame) and not df.empty]

    if not dfs:
        boolean_evaluations = [eval for eval in literal_evaluations if isinstance(eval, bool)]
        return reduce(lambda x, y: x and y, boolean_evaluations, True)


    # Iterate over the DataFrames and their indices
    for idx, df in enumerate(dfs):
        new_columns = {col: f"{col}_{idx}" for col in df.columns if all(isinstance(item, dict) for item in df[col])}
        df.rename(columns=new_columns, inplace=True)
    # Perform a natural join between all DataFrames
    combined_df = dfs[0]
    for df in dfs[1:]:
        common_columns = combined_df.columns.intersection(df.columns)
        if common_columns.any():
            combined_df = pd.merge(combined_df, df, how='inner')
        else:
            combined_df = pd.merge(combined_df, df, how='cross')
    
    # Identify columns with common prefixes and merge dictionaries
    column_groups = {}
    for col in combined_df.columns:
        prefix = col.rsplit('_', 1)[0]
        if prefix not in column_groups:
            column_groups[prefix] = []
        column_groups[prefix].append(col)
    
    def merge_dicts_series(series):
        merged = {}
        for d in series:
            for k, v in d.items():
                if k in merged:
                    if (merged[k] == '1' and v == '0') or (merged[k] == '0' and v == '1'):
                        return None  # Conflict, drop this row
                    if (merged[k] == '1' and v == '1/2') or (merged[k] == '1/2' and v == '1'):
                        merged[k] = '1/2'
                    elif (merged[k] == '0' and v == '1/2') or (merged[k] == '1/2' and v == '0'):
                        merged[k] = '1/2'
                    else:
                        merged[k] = v
                else:
                    merged[k] = v
        return merged

    for prefix, columns in column_groups.items():
        if len(columns) > 1:
            combined_df[prefix] = combined_df[columns].apply(merge_dicts_series, axis=1)
            combined_df.drop(columns=columns, inplace=True)
            combined_df.dropna(subset=[prefix], inplace=True)
        elif len(columns) == 1 and any(all(isinstance(item, dict) for item in combined_df[col]) for col in columns):
            original_col_name = prefix
            combined_df.rename(columns={columns[0]: original_col_name}, inplace=True)
    
    return combined_df
 

def vtoa(head: PredicateHead, body_evaluation: Union[pd.DataFrame, bool]) -> Union[pd.DataFrame, bool]:
    args = tuple([str(arg.value) for arg in head.args ])
    vars = [str(v) for v in args if v.isupper()]
    if not args:  # If args is empty, return body_evaluation
        if isinstance(body_evaluation, bool):
            return body_evaluation
        else:
            return True if not body_evaluation.empty else False
    
    if body_evaluation is False:
        return pd.DataFrame()  # Return an empty dataframe for False

    if body_evaluation is True:
        # Return a dataframe with a single row containing the head arguments
        return pd.DataFrame([head.args], dtype=str)
    if isinstance(body_evaluation, pd.DataFrame):        
        result = []
        for _, row in body_evaluation.iterrows():
            new_tuple = tuple(row.loc[i] if i in vars else i for i in args)
            if new_tuple not in result:
                result.append(new_tuple)

    return pd.DataFrame(result)




def make_hashable(value):
    if isinstance(value, dict):
        return frozenset((make_hashable(k), make_hashable(v)) for k, v in value.items())
    elif isinstance(value, (list, set, tuple)):
        return tuple(make_hashable(x) for x in value)
    return value

def hashable(row):
    return tuple((k, make_hashable(v)) for k, v in row.items())

def update_approximation(approximation: dict[str, Union[pd.DataFrame, bool]], head: PredicateHead, values: Union[pd.DataFrame, bool], approximation_to_update: str) -> bool:
    changes_made = False
    predicate = head.predicate
    
    if isinstance(values, pd.DataFrame):
        if predicate in approximation:
            if isinstance(approximation[predicate], pd.DataFrame):
                original_length = len(approximation[predicate])
                approximation[predicate] = values                
                if len(approximation[predicate]) != original_length:
                    changes_made = True
            else:
                approximation[predicate] = values
                changes_made = True
        else:
            approximation[predicate] = values
            changes_made = True

    elif isinstance(values, bool):
        if predicate in approximation and isinstance(approximation[predicate], bool):
            if approximation[predicate] != values:
                approximation[predicate] = values
                changes_made = True

    return changes_made

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

def process_rules(program: Program, types: list, current_under_approximation: dict, current_over_approximation: dict, mode: str) -> dict:
    while True:
        new_tuples_produced = False
        new_under_approximation = copy.deepcopy(current_under_approximation)
        new_over_approximation = copy.deepcopy(current_over_approximation)
        grouped_rules = group_rules_by_head(program.rules)
        new_tuples_produced = False
        for p in grouped_rules.keys():
            head_tuples = pd.DataFrame()
            for rule in grouped_rules[p]:
                body = rule.body
                literal_evaluations = []
                for l in body:
                    literal_evaluations.append(
                        atov(l, types, new_under_approximation, new_over_approximation)
                    )
                body_evaluation = combine_literal_evaluations(literal_evaluations)
                
                rule_tuples = vtoa(rule.head, body_evaluation)
                if isinstance(rule_tuples, bool):
                    head_tuples = rule_tuples
                else:
                    head_tuples = pd.concat([head_tuples, rule_tuples])
                    head_tuples['__hashable__'] = head_tuples.apply(hashable, axis=1)
                    head_tuples = head_tuples.drop_duplicates(subset=['__hashable__']).drop(columns=['__hashable__']).reset_index(drop=True)
    
            if mode == 'dt':
                if update_approximation(new_under_approximation, rule.head, head_tuples, mode):
                    new_tuples_produced = True
            elif mode == 'ndf':
                if update_approximation(new_over_approximation, rule.head, head_tuples, mode):
                    new_tuples_produced = True

        if not new_tuples_produced:
            break
        current_under_approximation = new_under_approximation
        current_over_approximation = new_over_approximation
    
    if mode == 'dt':
        return new_under_approximation
    else:
        return new_over_approximation

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


def handle_query(query):
    pass