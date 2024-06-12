from components import *
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
        column_names = [f'{predicate}_{i+1}' for i in range(arity)]
        c = cartesian_product([H_u if not isinstance(element, list) else [ (set(), set(itertools.combinations_with_replacement(H_u, len(element)))) ] for element in predicate_type])        
        df = pd.DataFrame(c, columns=column_names)
        return df


def initialize_under_approximation(program: Program, predicate: str) -> pd.DataFrame:
    predicate_type = program.types[predicate]
    if predicate_type == 'o':
        return False
    else:  # if it is a list
        arity = len(predicate_type)
        column_names = [f'{predicate}_{i+1}' for i in range(arity)]
        c = cartesian_product([H_u if not isinstance(element, list) else [ ((), () ) ] for element in predicate_type])        
        df = pd.DataFrame(c, columns=column_names)
        return df


def atov(literal: Literal, under_approximation: dict, over_approximation: dict) -> pd.DataFrame:
    
    return (
        constant_predicate_atov(literal, under_approximation, over_approximation)
        if literal.atom.predicate.islower()
        else variable_predicate_atov(literal, under_approximation, over_approximation)
    )    


def constant_predicate_atov(literal: Literal, under_approximation: dict, over_approximation: dict) -> pd.DataFrame:
    atom = literal.atom
    predicate = atom.predicate
    args = atom.args
    vars = [v for v in args if v.value.isupper()]
    is_negated = literal.negated

    stored_tuples_dt = pd.DataFrame()
    if predicate.startswith('dt_'):
        stored_tuples_df = under_approximation[predicate]
        print(stored_tuples_df)
    else:
        stored_tuples_df = over_approximation[predicate]
        print(stored_tuples_df)


def variable_predicate_atov(literal: Literal, under_approximation: dict, over_approximation: dict) -> pd.DataFrame:
    pass