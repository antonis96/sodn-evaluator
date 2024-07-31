from components import *
from typing import Union, List
import pandas as pd
from .helpers import *
from .atov import atov
from .combine import combine_literal_evaluations
from .vtoa import vtoa

def evaluate_rule(rule: Rule, types:list, current_under_approximation: dict, current_over_approximation: dict, herbrand_universe):
    literal_evaluations = []
    for l in rule.body:
        literal_evaluations.append(
            atov(l, types, current_under_approximation, current_over_approximation, herbrand_universe)
        )
    body_evaluation = combine_literal_evaluations(literal_evaluations)
    new_tuples = vtoa(rule.head, body_evaluation)
    return new_tuples


def evaluate_rule_union(
        rules: List[Rule], 
        types: list, 
        current_under_approximation: dict, 
        current_over_approximation: dict, herbrand_universe
) -> Union[pd.DataFrame,bool]:

    combined = None

    for rule in rules:
        new_tuples = evaluate_rule(rule, types, current_under_approximation, current_over_approximation, herbrand_universe)
        if isinstance(new_tuples, pd.DataFrame):
            if combined is None:
                combined = pd.DataFrame()
            combined = pd.concat([combined, new_tuples])
            combined['__hashable__'] = combined.apply(hashable, axis=1)
            combined = combined.drop_duplicates(subset=['__hashable__']).drop(columns=['__hashable__']).reset_index(drop=True)
        elif isinstance(new_tuples, bool):
            combined = combined or new_tuples
    return combined
