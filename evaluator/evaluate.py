from components import *
from typing import Union, List
import pandas as pd
import itertools

H_u = {'a', 'b', 'c'}

def cartesian_product(elements):
    products = list(itertools.product(*elements))
    return products


def initialize_over_approximation(program: Program, predicate: str) -> pd.DataFrame:
    predicate_type = program.types[predicate]
    if predicate_type == 'o':
        return True
    else:  # if it is a list
        arity = len(predicate_type)
        c = cartesian_product([H_u if not isinstance(element, list) else [ (set(), set(itertools.combinations_with_replacement(H_u, len(element)))) ] for element in predicate_type])   
        df = pd.DataFrame(c)
        return df


def initialize_under_approximation(program: Program, predicate: str) -> pd.DataFrame:
    predicate_type = program.types[predicate]
    if predicate_type == 'o':
        return False
    else:  # if it is a list
        arity = len(predicate_type)
        c = cartesian_product([() if not isinstance(element, list) else [ ((), () ) ] for element in predicate_type])        
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


def atov(literal: Literal, types:list, under_approximation: dict, over_approximation: dict) -> pd.DataFrame:
    return (
        constant_predicate_atov(literal, types[literal.atom.predicate], under_approximation, over_approximation)
        if literal.atom.predicate.islower()
        else variable_predicate_atov(literal, types[literal.atom.predicate], under_approximation, over_approximation)
    )    


def constant_predicate_atov(literal: Literal, atom_type:Union[str,list], under_approximation: dict, over_approximation: dict) -> Union[pd.DataFrame,bool]:
    atom = literal.atom
    predicate = atom.predicate
    args = tuple([arg.value for arg in atom.args ])
    vars = [str(v) for v in tuple(atom.args) if v.value.isupper()]
    is_negated = literal.negated

    stored_df = pd.DataFrame()
    if predicate.startswith('dt_'):
        stored_df = under_approximation[predicate]
    else:
        stored_df = over_approximation[predicate]


    if not vars:
        stored_df_tuples = [tuple(row) for row in stored_df.itertuples(index=False, name=None)]
        return args in stored_df_tuples

    if not is_negated:
        matches = []
        for row in stored_df.itertuples(index=False, name=None):

            sub = match(atom.args, row, atom_type)
            if sub:
                matches.append(sub)
        return pd.DataFrame(matches)
    else:
        matches = []
        all_combinations = [dict(zip(vars, comb)) for comb in itertools.product(H_u, repeat=len(vars))]
        for row in stored_df.itertuples(index=False, name=None):
            sub = match(atom.args, row, atom_type)
            if sub:
                matches.append(sub)
        diff = [item for item in all_combinations if item not in matches]
        return pd.DataFrame(diff)

             

def match(a: tuple, b:tuple, atom_type:Union[str,list]) -> dict:
    if len(a) != len(b):
        return {}
    sub = {}
    for ai, bi, ti in zip(a, b,atom_type):
        if ai.arg_type == 'data_const' and ai.value != bi:
            return {}
        elif ai.arg_type == 'variable':
            if ai not in sub:
                sub[ai.value] = bi
            elif isinstance(ai, str) and sub[ai.value] != bi:
                return {}
            elif isinstance(ai, list):
                pass
                # sub[ai.value] = 5

    return sub


def variable_predicate_atov(literal: Literal, atom_type:Union[str,list], under_approximation: dict, over_approximation: dict) -> pd.DataFrame:
    pass

from functools import reduce


def combine_literal_evaluations(literal_evaluations: List[Union[pd.DataFrame, bool]]) -> Union[pd.DataFrame, bool]:
    if not literal_evaluations:
        return pd.DataFrame()  # Return an empty dataframe if the list is empty

    # Filter out boolean values and check for False, and check for empty dataframes
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

    # Perform a natural join on the list of dataframes using pd.merge
    def join_with_cartesian(left, right):
        common_columns = list(set(left.columns) & set(right.columns))
        if not common_columns:
            # Perform Cartesian product if no common columns
            left['key'] = 1
            right['key'] = 1
            result = pd.merge(left, right, on='key').drop('key', axis=1)
        else:
            result = pd.merge(left, right, on=common_columns)
        return result

    return reduce(lambda left, right: join_with_cartesian(left, right), dfs)



def vtoa(head: PredicateHead, body_evaluation: Union[pd.DataFrame, bool]) -> Union[pd.DataFrame, bool]:
    predicate = head.predicate
    args = tuple([arg.value for arg in head.args ])
    vars = [str(v) for v in args if v.isupper()]

    if not args:  # If args is empty, return body_evaluation
        return body_evaluation
    
    if body_evaluation is False:
        return pd.DataFrame()  # Return an empty dataframe for False

    if body_evaluation is True:
        # Return a dataframe with a single row containing the head arguments
        return pd.DataFrame([head.args])
    if isinstance(body_evaluation, pd.DataFrame):
        result = []
        for _, row in body_evaluation.iterrows():
            new_tuple = tuple(row.iloc[i] if str(args[i]) in vars else str(args[i]) for i in range(len(args)))
            result.append(new_tuple)
        return pd.DataFrame(result).drop_duplicates()
