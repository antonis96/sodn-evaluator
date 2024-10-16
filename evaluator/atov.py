from typing import Union
import itertools
import pandas as pd
from components import Literal
from .helpers import *
from .combine import combine_literal_evaluations

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
        mode = 'dt'
        stored_df = under_approximation[predicate]
    else:
        mode = 'ndf'
        stored_df = over_approximation[predicate]
    if atom_type == 'o':
        return stored_df if not is_negated else not stored_df
    
    if not vars:
        if is_negated:
            for row in stored_df.itertuples(index=False, name=None):
                sub, valid_sub = match(atom.args, row, under_approximation, over_approximation, mode)
                if valid_sub:
                    return False
            return True
        else:
            for row in stored_df.itertuples(index=False, name=None):
                sub, valid_sub = match(atom.args, row, under_approximation, over_approximation, mode)
                if valid_sub:
                    return True
            return False

    matches = []
    for row in stored_df.itertuples(index=False, name=None):
        sub, valid_sub = match(atom.args, row, under_approximation, over_approximation, mode)
        if not valid_sub:
            continue
        matches.append(sub)

    matched_df = pd.DataFrame(matches,columns=vars)
    if not is_negated:
        return matched_df
    else:
        false_df = get_false_combinations(matched_df,herbrand_universe)
        return false_df

def match(
        a: tuple, 
        b:tuple, 
        under_approximation: dict, 
        over_approximation: dict,
        mode: str
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
            
            def check_keys(dt_tuples, ndf_tuples, bi, mode):
                if mode == 'dt':
                    for key, val in bi.items():
                        if val ==  '1' and key not in dt_tuples:
                            return False
                        if val == '0' and key in ndf_tuples:
                            return False      
                    return True
                elif mode == 'ndf':
                    for key, val in bi.items():
                        if val == '1' and key not in ndf_tuples :
                            return False
                        if val == '0':
                            if not ((key not in ndf_tuples) or (key in ndf_tuples and key not in dt_tuples)):
                                return False      
                    return True

            check = check_keys(dt_tuples, ndf_tuples, bi, mode)
            if not check:
                return {}, False
                    
        if ai.arg_type == 'variable':
            if ai not in sub:
                sub[ai.value] = bi
            elif isinstance(ai, str) and sub[ai.value] != bi:
                return {}, False
    return sub, True

def get_false_combinations(df,herbrand_universe):
    n = len(df.columns)
    binary_strings = list(itertools.product([0, 1], repeat=n))
    binary_strings = [bs for bs in binary_strings if any(bs)]

    row_dataframes = [create_variations(row, binary_strings, herbrand_universe) for _, row in df.iterrows()]

    result_df = combine_literal_evaluations(row_dataframes)
    return result_df


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
                ]
                df = pd.DataFrame( {predicate:data})

            else:
                expanded_data = df.apply(lambda row: expand_row(row, ['0']), axis=1).tolist()
                expanded_data_flat = [item for sublist in expanded_data for item in sublist]

                df = pd.DataFrame(expanded_data_flat, columns=list(df.columns) + [predicate])

    else:
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
                ]
                df = pd.DataFrame( {predicate:data})
            else:
                expanded_data = df.apply(lambda row: expand_row(row, ['0']), axis=1).tolist()
                expanded_data_flat = [item for sublist in expanded_data for item in sublist]

                df = pd.DataFrame(expanded_data_flat, columns=list(df.columns) + [predicate])

    return df
