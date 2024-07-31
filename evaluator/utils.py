from components import *
import pandas as pd
import itertools
from functools import reduce
from .helpers import *


def extract_herbrand_universe(program: Program) -> set:
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
    if herbrand_universe == set():
        return {'c'}
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
