from components import *
from typing import Union, List
import pandas as pd
import itertools
import copy 
from functools import reduce


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


def atov(literal: Literal, types:dict, under_approximation: dict, over_approximation: dict) -> pd.DataFrame:
    return (
        constant_predicate_atov(literal, types[literal.atom.predicate], under_approximation, over_approximation)
        if literal.atom.predicate.islower()
        else variable_predicate_atov(literal, ['i' for i in range(0,len(literal.atom.args))], under_approximation, over_approximation)
    )    


def constant_predicate_atov(literal: Literal, atom_type:Union[str,list], under_approximation: dict, over_approximation: dict) -> Union[pd.DataFrame,bool]:
    atom = literal.atom
    predicate = atom.predicate
    args = tuple([arg.value for arg in atom.args ])
    vars = [str(v) for v in tuple(atom.args) if v.value.isupper()]
    is_negated = literal.negated


    if predicate.startswith('dt_'):
        stored_df = under_approximation[predicate]
    else:
        stored_df = over_approximation[predicate]


    if not vars:
        if args:
            stored_df_tuples = [tuple(row) for row in stored_df.itertuples(index=False, name=None)]
            if is_negated:
                return True if args not in stored_df_tuples else False
            return True if args in stored_df_tuples else False
        else:
            return not stored_df if is_negated else stored_df
    if not is_negated:
        matches = []
        for row in stored_df.itertuples(index=False, name=None):
            sub = match(atom.args, row, atom_type)
            if sub:
                matches.append(sub)
        return pd.DataFrame(matches,columns=vars)
    else:
        matches = []
        all_combinations = [dict(zip(vars, comb)) for comb in itertools.product(H_u, repeat=len(vars))] # fix it alter in order to include constants as well
        if stored_df.empty:
            return pd.DataFrame(all_combinations, columns=vars)
        for row in stored_df.itertuples(index=False, name=None):
            sub = match(atom.args, row, atom_type)
            if sub:
                matches.append(sub)
        diff = [item for item in all_combinations if item not in matches]
        return pd.DataFrame(diff, columns=vars)

             

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
    atom = literal.atom
    predicate = atom.predicate
    args = tuple([arg.value for arg in atom.args ])
    arg_vars = [str(v) for v in tuple(atom.args) if v.value.isupper()]
    arg_constants = [const for const in args if const not in arg_vars]
    is_negated = literal.negated


    var_subs = list(itertools.product(H_u, repeat=len(arg_vars))) # possible substitutions of argument variables
    possible_subs = list(itertools.product(H_u, repeat=len(args)))
    
    if not is_negated:
        df = pd.DataFrame(var_subs, columns=arg_vars)
        for const in arg_constants: # add constants into df
            df[const] = const

        def create_tuple_set(row):
            return {tuple(row)}

        # Add new column with the required pairs of sets
        df[predicate] = df.apply(lambda row: (create_tuple_set(row), set(possible_subs)), axis=1)
        df = df.drop(columns=arg_constants)
    else:
        df = pd.DataFrame(var_subs, columns=arg_vars)
        for const in arg_constants: # add constants into df
            df[const] = const

        def remove_tuple(row):
            difference = set(possible_subs)
            difference.discard(tuple(row))
            return difference
            # return {tuple(row)}

        # Add new column with the required pairs of sets
        df[predicate] = df.apply(lambda row: (set(), set(remove_tuple(row))), axis=1)
        df = df.drop(columns=arg_constants)

    return df




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
        return pd.DataFrame(result, columns=vars).drop_duplicates()



def update_approximation(approximation: dict, head: PredicateHead, values: Union[pd.DataFrame, bool], approximation_to_update: str) -> bool:
    changes_made = False
    predicate = head.predicate
    
    if isinstance(values, pd.DataFrame):
        if predicate in approximation:
            if isinstance(approximation[predicate], pd.DataFrame):
                original_length = len(approximation[predicate])
                if approximation_to_update == 'dt':
                    approximation[predicate] = pd.concat([approximation[predicate], values]).drop_duplicates().reset_index(drop=True)
                else:  # For ndf_approximation or others, just add values
                    approximation[predicate] = pd.DataFrame(values).drop_duplicates().reset_index(drop=True)
                if len(approximation[predicate]) != original_length:
                    changes_made = True
            else:
                approximation[predicate] = values.drop_duplicates().reset_index(drop=True)
                changes_made = True
        else:
            approximation[predicate] = values.drop_duplicates().reset_index(drop=True)
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
            df1 = value1.sort_index(axis=1).sort_values(by=list(value1.columns)).reset_index(drop=True)
            df2 = value2.sort_index(axis=1).sort_values(by=list(value2.columns)).reset_index(drop=True)
            
            if not df1.equals(df2):
                return False
        else:
            return False
            
    return True
