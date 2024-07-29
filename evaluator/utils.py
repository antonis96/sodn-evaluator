from components import *
from typing import Union, List
import pandas as pd
import itertools
import copy 
from functools import reduce
from itertools import product
from .helpers import *


def extract_herbrand_univse(program: Program) -> set:
    herbrand_universe = set()
    for f in program.facts:
        herbrand_universe.update(set(f.head.args))
    
    for r in program.rules:
        for arg in r.head.args:
            if arg.value.islower():
                herbrand_universe.add(arg.value)
        # args that are not predicate constants in the rule's body
        non_predicate_body_args = set()
        for l in r.body:
            for arg in l.atom.args:
                if arg.value.islower() and arg.value not in program.predicates:
                 non_predicate_body_args.add(arg.value)
        herbrand_universe.update(non_predicate_body_args)
    return {str(element) for element in herbrand_universe}

def initialize_over_approximation(program: Program, predicate: str, herbrand_universe: set) -> pd.DataFrame:
    predicate_type = program.types[predicate]
    if predicate_type == 'o':
        return True
    else:  # if it is a list
        c = cartesian_product([
                herbrand_universe if not isinstance(element, list) else [
                {r: value} for r in list(itertools.combinations_with_replacement(herbrand_universe, len(element)))
                for value in ['0', '1/2', '1']
            ] for element in predicate_type
        ]) 
        df = pd.DataFrame(c)
        return df
    
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

def process_rules(program: Program, types: list, current_under_approximation: dict, current_over_approximation: dict, mode: str, herbrand_universe) -> dict:
    
    grouped_rules = group_rules_by_head(program.rules)

    predicate_tuples = {
        predicate: pd.DataFrame()
        for predicate in program.predicates
    }
   
    for i in range(0,10):
        new_tuples_produced = False
        new_under_approximation = copy.deepcopy(current_under_approximation)
        new_over_approximation = copy.deepcopy(current_over_approximation)

        for p in grouped_rules.keys():
            head_tuples = predicate_tuples[p]

            for rule in grouped_rules[p]:
                body = rule.body
                literal_evaluations = []
                for l in body:
                    literal_evaluations.append(
                        atov(l, types, new_under_approximation, new_over_approximation, herbrand_universe)
                    )
                
                body_evaluation = combine_literal_evaluations(literal_evaluations)
                
                rule_tuples = vtoa(rule.head, body_evaluation)

                if isinstance(rule_tuples, bool):
                    head_tuples = rule_tuples
                else:
                    head_tuples = pd.concat([head_tuples, rule_tuples])
                    head_tuples['__hashable__'] = head_tuples.apply(hashable, axis=1)
                    head_tuples = head_tuples.drop_duplicates(subset=['__hashable__']).drop(columns=['__hashable__']).reset_index(drop=True)
        
        predicate_tuples[p] = pd.concat([predicate_tuples[p], head_tuples])
            
            # if mode == 'dt':
            #     if update_approximation(new_under_approximation, rule.hepredicate_tuplesad, [p], mode):
            #         new_tuples_produced = True
            # elif mode == 'ndf':
            #     if update_approximation(new_over_approximation, rule.head, predicate_tuples[p], mode):
            #         new_tuples_produced = True

        # if not new_tuples_produced:
        #     break
        

        current_under_approximation = copy.deepcopy(new_under_approximation)
        current_over_approximation = copy.deepcopy(new_over_approximation)
    print_approximation(predicate_tuples)
    if mode == 'dt':
        return new_under_approximation
    else:
        return new_over_approximation


def atov(literal: Literal, types:dict, under_approximation: dict, over_approximation: dict, herbrand_universe) -> pd.DataFrame:
    return (
        constant_predicate_atov(literal, types[literal.atom.predicate], under_approximation, over_approximation, herbrand_universe)
        if literal.atom.predicate.islower()
        else variable_predicate_atov(literal, herbrand_universe)
    )    

def constant_predicate_atov(literal: Literal, atom_type:Union[str,list], under_approximation: dict, over_approximation: dict, herbrand_universe) -> Union[pd.DataFrame,bool]:
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
        false_df = get_false_combinations(matched_df,atom_type, herbrand_universe)
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

# TODO add types
def get_false_combinations(df, predicate_type, herbrand_universe):
    if df.empty:
        c = cartesian_product([
                herbrand_universe if not isinstance(element, list) else [
                {r: value} for r in list(itertools.combinations_with_replacement(herbrand_universe, len(element)))
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
    all_combinations = list(itertools.product(*([ herbrand_universe for col in plain_columns] + dict_combinations)))

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


def variable_predicate_atov(literal: Literal, herbrand_universe) -> pd.DataFrame:
    atom = literal.atom
    predicate = atom.predicate
    args = tuple([str(arg.value) for arg in atom.args ])
    arg_vars = [str(v) for v in tuple(atom.args) if v.value.isupper()]
    is_negated = literal.negated

    var_subs = list(itertools.product(herbrand_universe, repeat=len(arg_vars))) # possible substitutions of argument variables
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


def handle_query(query):
    pass