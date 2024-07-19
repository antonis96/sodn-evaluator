from components import *
from typing import Union, List
import pandas as pd
import itertools
import copy 
from functools import reduce
from itertools import product


H_u = {'a','b','c'}

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

def get_false_combinations(df_true):
    # Extract columns and unique values for each column
    columns = df_true.columns

    data_columns = [col for col in columns if df_true[col].apply(lambda x: isinstance(x, str)).all()]
    relation_columns = [col for col in columns if col not in data_columns]

    def get_relation_keys(df, relation_columns):
        keys_dict = {}
        for col in relation_columns:
            keys = set()
            for val in df[col]:
                if isinstance(val, dict):
                    keys.update(val.keys())
            keys_dict[col] = list(keys)
        return keys_dict

    relation_keys = get_relation_keys(df_true, relation_columns)

    data_combinations = list(product(H_u, repeat=len(data_columns)))

    def generate_relation_combinations(relation_columns, relation_keys):
        all_combinations = []
        for col in relation_columns:
            key_combinations = list(product(['0', '1/2', '1'], repeat=len(relation_keys[col])))
            all_combinations.append((col, key_combinations))
        return all_combinations

    relation_combinations = generate_relation_combinations(relation_columns, relation_keys)

    def is_true(row):
        for _, true_row in df_true.iterrows():
            match = True
            for col in data_columns:
                if row.get(col) != true_row.get(col):
                    match = False
                    break
            for rel_col in relation_columns:
                if rel_col in row and rel_col in true_row:
                    for key in row[rel_col]:
                        if row[rel_col][key] != true_row[rel_col].get(key):
                            match = False
                            break
            if match:
                return True
        return False

    def generate_rows(data_comb, rel_comb_idx=0, current_row=None):
        if current_row is None:
            current_row = dict(zip(data_columns, data_comb))

        if rel_comb_idx >= len(relation_combinations):
            if not is_true(current_row):
                false_combinations.append(current_row.copy())
            return

        col, key_combinations = relation_combinations[rel_comb_idx]
        for key_comb in key_combinations:
            current_row[col] = dict(zip(relation_keys[col], key_comb))
            generate_rows(data_comb, rel_comb_idx + 1, current_row)

    false_combinations = []

    for data_comb in data_combinations:
        generate_rows(data_comb)

    df_false = pd.DataFrame(false_combinations)

    return df_false



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
        false_df = get_false_combinations(matched_df)
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
                expanded_data = df.apply(lambda row: expand_row(row, ['1', '1/2']), axis=1).tolist()
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




def combine_literal_evaluations(literal_evaluations: List[Union[pd.DataFrame, bool]]) -> Union[pd.DataFrame, bool]:
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

    # If there are no dataframes, return an empty dataframe
    if not dfs:
        boolean_evaluations = [eval for eval in literal_evaluations if isinstance(eval, bool)]
        return reduce(lambda x, y: x and y, boolean_evaluations, True)

    # Function to handle the union and intersection for pair values
    def merge_dicts(dict1, dict2):
        for k in dict2.keys():
            if k in dict1 and dict1[k] != dict2[k]:
                return None  # Conflict found, return None to indicate no merge
        merged_dict = dict1.copy()
        merged_dict.update(dict2)
        return merged_dict

    def merge_relations(df1, df2):
        common_columns = df1.columns.intersection(df2.columns)

        common_first_order_columns = [col for col in common_columns if not isinstance(df1[col].iloc[0], dict)]

        if common_first_order_columns:
            # Perform the natural join on these common_first_order_columns columns
            result = pd.merge(df1, df2, on=common_first_order_columns)
        else:
            result = pd.merge(df1, df2, how='cross')

        # Identify dictionary columns
        dict_columns_df1 = [col for col in df1.columns if isinstance(df1[col].iloc[0], dict)]
        dict_columns_df2 = [col for col in df2.columns if isinstance(df2[col].iloc[0], dict)]

        # Find common dictionary columns
        common_second_order_columns = list(set(dict_columns_df1) & set(dict_columns_df2))

        # Merge dictionaries in common dictionary columns
        for col in common_second_order_columns:
            result[col] = result.apply(
                lambda row: merge_dicts(row[f'{col}_x'], row[f'{col}_y']) if pd.notna(row[f'{col}_x']) and pd.notna(row[f'{col}_y']) else row[f'{col}_x'] if pd.notna(row[f'{col}_x']) else row[f'{col}_y'],
                axis=1
            )
            # Drop rows where merge_dicts returned None
            result = result[result[col].notna()]
            result.drop(columns=[f'{col}_x', f'{col}_y'], inplace=True)
        return result

    return reduce(lambda left, right: merge_relations(left, right), dfs)





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


def update_approximation(approximation: dict, head: PredicateHead, values: Union[pd.DataFrame, bool], approximation_to_update: str) -> bool:
    changes_made = False
    predicate = head.predicate
    
    if isinstance(values, pd.DataFrame):
        if predicate in approximation:
            if isinstance(approximation[predicate], pd.DataFrame):
                original_length = len(approximation[predicate])
                approximation[predicate] = pd.DataFrame(values)
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

def process_rules(program: Program, types: list, current_under_approximation: dict, current_over_approximation: dict, mode: str) -> dict:
    while True:
        new_tuples_produced = False
        new_under_approximation = copy.deepcopy(current_under_approximation)
        new_over_approximation = copy.deepcopy(current_over_approximation)
        
        for rule in program.rules:
            body = rule.body
            literal_evaluations = []
            for l in body:
                literal_evaluations.append(
                    atov(l, types, new_under_approximation, new_over_approximation)
                )
            body_evaluation = combine_literal_evaluations(literal_evaluations)
            
            head_tuples = vtoa(rule.head, body_evaluation)
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