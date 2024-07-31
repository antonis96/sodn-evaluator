from typing import Union
import itertools
import pandas as pd

from components import Literal
from .helpers import *


def atov(
        literal: Literal, 
        types:dict, 
        under_approximation: dict, 
        over_approximation: dict, 
        herbrand_universe
) -> pd.DataFrame:
    return (
        constant_predicate_atov(literal, types[literal.atom.predicate], under_approximation, over_approximation, herbrand_universe)
        if literal.atom.predicate.islower()
        else variable_predicate_atov(literal, herbrand_universe)
    )    

def constant_predicate_atov(
    literal: Literal, 
    atom_type:Union[str,list], 
    under_approximation: dict, 
    over_approximation: dict, 
    herbrand_universe
) -> Union[pd.DataFrame,bool]:

    atom = literal.atom
    predicate = atom.predicate
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

def match(
        a: tuple, 
        b:tuple, 
        under_approximation: dict, 
        over_approximation: dict
):
    if len(a) != len(b):
        return {}, False
    sub = {}
    for ai, bi in zip(a, b):
        if ai.arg_type == 'data_const' and ai.value != bi:
            return {}, False
        elif ai.arg_type == 'predicate_const':
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


    all_combinations = list(itertools.product(*([ herbrand_universe for col in plain_columns] + dict_combinations)))

    new_rows = pd.DataFrame(all_combinations, columns=plain_columns + dict_columns)
    df_hashable = df.apply(hashable, axis=1)
    new_rows_hashable = new_rows.apply(hashable, axis=1)

    # Filter new rows to include only those not present in original df
    unique_new_rows = new_rows[~new_rows_hashable.isin(df_hashable)]

    for col in dict_columns:
        unique_new_rows.loc[:, col] = unique_new_rows[col].apply(remove_nan_keys)

    return unique_new_rows.reset_index(drop=True)


def variable_predicate_atov(
    literal: Literal, 
    herbrand_universe
) -> pd.DataFrame:

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
