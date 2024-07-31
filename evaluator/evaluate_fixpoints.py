from components import *
from typing import Union, List
import pandas as pd
import copy 
from .helpers import *
from .evaluate_rule import evaluate_rule_union


def evaluate_tp(
        program: Program, 
        types: list, 
        current_under_approximation: dict, 
        current_over_approximation: dict, 
        herbrand_universe: set, 
        mode: str
) -> dict[str, pd.DataFrame]:

    grouped_rules = group_rules_by_head(program.rules)
    new_approximation = current_under_approximation if mode == 'dt' else current_over_approximation
    iteration = 0
    stable = False

    while not stable:
        stable = True
        iteration += 1
        previous_approximation = copy.deepcopy(new_approximation)

        for p in grouped_rules.keys():
            rules = grouped_rules[p]
            rule_tuples = evaluate_rule_union(rules, types, current_under_approximation, current_over_approximation, herbrand_universe)

            if isinstance(rule_tuples,pd.DataFrame):
                if iteration == 1:
                    fact_tuples = []
                    for fact in program.facts:
                        if fact.head.predicate == p:
                            fact_tuples.append(tuple([str(arg) for arg in fact.head.args]))
                    new_approximation[p] = pd.concat([rule_tuples,pd.DataFrame(fact_tuples)]).drop_duplicates() ##### + FACTS HERE
                else:
                    new_approximation[p] = pd.concat([new_approximation[p], rule_tuples])
                    new_approximation[p]['__hashable__'] = new_approximation[p].apply(hashable, axis=1)
                    new_approximation[p] = new_approximation[p].drop_duplicates(subset=['__hashable__']).drop(columns=['__hashable__']).reset_index(drop=True)
            else:
                new_approximation[p] = rule_tuples
        if mode == 'dt':
            current_under_approximation = copy.deepcopy(new_approximation)
        else:
            current_over_approximation = copy.deepcopy(new_approximation)

        # Check if the new approximation is stable
        for p in grouped_rules.keys():
            if isinstance(new_approximation[p], pd.DataFrame):
                if not new_approximation[p].equals(previous_approximation[p]):
                    stable = False
                    break
            else:
                if new_approximation[p] != previous_approximation[p]:
                    stable = False
                    break
    return new_approximation

def evaluate_alternating_fp(
        dt_program: Program, 
        ndf_program: Program, 
        types: list, 
        current_under_approximation: dict, 
        current_over_approximation: dict, 
        herbrand_universe: set
) -> dict[str, pd.DataFrame]:

    stable = False

    while not stable:
        stable = True
        previous_under_approximation = copy.deepcopy(current_under_approximation)
        previous_over_approximation = copy.deepcopy(current_over_approximation)

        new_under_approximation = evaluate_tp(dt_program, types, current_under_approximation, current_over_approximation, herbrand_universe, mode='dt')
        new_over_approximation = evaluate_tp(ndf_program, types, current_under_approximation, current_over_approximation, herbrand_universe, mode='ndf')

        current_under_approximation = copy.deepcopy(new_under_approximation)
        current_over_approximation = copy.deepcopy(new_over_approximation)

        for key in current_under_approximation.keys():
            if isinstance(new_under_approximation[key], pd.DataFrame):
                if not new_under_approximation[key].equals(previous_under_approximation[key]):
                    stable = False
                    break
            else:
                if new_under_approximation[key] != previous_under_approximation[key]:
                    stable = False
                    break

        if stable:
            for key in current_over_approximation.keys():
                if isinstance(new_over_approximation[key], pd.DataFrame):
                    if not new_over_approximation[key].equals(previous_over_approximation[key]):
                        stable = False
                        break
                else:
                    if new_over_approximation[key] != previous_over_approximation[key]:
                        stable = False
                        break


    return current_under_approximation, current_over_approximation