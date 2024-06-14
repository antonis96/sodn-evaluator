from components import *
from typing import Union
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
            new_tuples[fact.head.predicate].append(tuple(fact.head.args))
    
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


def constant_predicate_atov(literal: Literal, atom_type:Union[str,list], under_approximation: dict, over_approximation: dict) -> pd.DataFrame:
    atom = literal.atom
    predicate = atom.predicate
    args = tuple(atom.args)
    vars = [v for v in args if v.value.isupper()]
    is_negated = literal.negated

    stored_tuples_dt = pd.DataFrame()
    if predicate.startswith('dt_'):
        stored_tuples_df = under_approximation[predicate]
    else:
        stored_tuples_df = over_approximation[predicate]

    for row in stored_tuples_df.itertuples(index=False, name=None):
        sub = match(args, row, atom_type)
        print(sub)
        if not is_negated: # if we have a positive literal
            pass
        else: # if we have a negative literal
            pass
             

def match(a: tuple, b:tuple, atom_type:Union[str,list]) -> dict:
    if len(a) != len(b):
        return {}

    sub = {}
    for ai, bi, ti in zip(a, b,atom_type):
        if ai.arg_type == 'data_const' and ai.value != bi.value:
            return {}
        elif ai.arg_type == 'variable':
            if ai.value not in sub:
                sub[ai.value] = bi
            elif isinstance(ai, str) and sub[ai.value] != bi:
                return {}
            elif isinstance(ai, list):
                sub[ai.value] = 5

    return sub


def variable_predicate_atov(literal: Literal, atom_type:Union[str,list], under_approximation: dict, over_approximation: dict) -> pd.DataFrame:
    pass