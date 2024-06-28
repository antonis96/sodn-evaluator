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


# Function to generate all subsets of a given set, allowing repetitions
def generate_subsets_with_replacement(s, size):
    subsets = []
    for r in range(size + 1):
        subsets.extend(map(lambda x: set((elem,) for elem in x), itertools.combinations_with_replacement(s, r)))
    subsets.append(set((elem,) for elem in s))  # Ensure the full set is included as required
    return subsets

# Function to process the input list and associate values
def associate_values(input_list, H_u):
    associated_values = []
    for element in input_list:
        if element == 'i':
            associated_values.append(list(H_u))
        elif isinstance(element, list):
            subset_size = len(element)
            subsets = generate_subsets_with_replacement(H_u, subset_size)
            associated_values.append(subsets)
    return associated_values

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
    args = tuple([str(arg.value) for arg in atom.args ])
    vars = [str(v) for v in tuple(atom.args) if v.value.isupper()]
    is_negated = literal.negated


    if predicate.startswith('dt_'):
        stored_df = under_approximation[predicate]
    else:
        stored_df = over_approximation[predicate]

    if not is_negated:
        matches = []
        for row in stored_df.itertuples(index=False, name=None):
            sub, valid_sub = match(atom.args, row, under_approximation, over_approximation)
            if not valid_sub:
                continue
            if sub == {}: # no variables
                return valid_sub
            else:
                matches.append(sub)
        return pd.DataFrame(matches,columns=vars)
    else:
        print(atom_type)
        associated_values = associate_values(atom_type, H_u)
        full_df = pd.DataFrame(cartesian_product(associated_values))
        print(full_df)
        matches = [] 
        for f_row in full_df.itertuples(index=False, name=None):
            valid_match = False
            for s_row in stored_df.itertuples(index=False, name=None):
                pass
            
            if valid_match is False:
                matches.append(f_row)

def match(a: tuple, b:tuple, under_approximation: dict, over_approximation: dict):
    if len(a) != len(b):
        return {}, False
    sub = {}
    for ai, bi in zip(a, b):
        if ai.arg_type == 'data_const' and ai.value != bi:
            return {}, False
        elif ai.arg_type == 'predicate_const':
            dt_tuples = set(under_approximation['dt_q'].apply(tuple, axis=1)) # SOS fix that so it won't be just q but anything
            ndf_tuples = set(over_approximation['ndf_q'].apply(tuple, axis=1))
            if not dt_tuples.issuperset(bi[0]) or not ndf_tuples.issubset(bi[1]):
                return {}, False
                    
        if ai.arg_type == 'variable':
            if ai not in sub:
                sub[ai.value] = bi
            elif isinstance(ai, str) and sub[ai.value] != bi:
                return {}, False
    return sub, True


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
        if not arg_vars: # if no variables
            df = pd.DataFrame(
                {
                    predicate: [
                        (
                            set([args]), 
                            set(possible_subs)
                        )
                    ]
                }
            )
            return df
        
        df = pd.DataFrame(var_subs, columns=arg_vars)
        for const in arg_constants: # add constants into df
            df[const] = const
        def create_tuple_set(row):
            return {tuple(row)}

        # Add new column with the required pairs of sets
        df[predicate] = df.apply(lambda row: (create_tuple_set(row), set(possible_subs)), axis=1)
        df = df.drop(columns=arg_constants)
        return  df
    else:
        if not arg_vars: # if no variables
            difference = set(possible_subs)
            difference.discard(args)
            df = pd.DataFrame(
                {
                    predicate: [
                        (
                            set(()), 
                            difference
                        )
                    ]
                }
            )
            return df
        
        df = pd.DataFrame(var_subs, columns=arg_vars)
        for const in arg_constants: # add constants into df
            df[const] = const

        def remove_tuple(row):
            difference = set(possible_subs)
            difference.discard(tuple(row))
            return difference
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

    # Function to handle the union and intersection for pair values
    def merge_pairs(pair1, pair2):
        first_union = pair1[0].union(pair2[0])
        second_intersection = pair1[1].intersection(pair2[1])
        return (first_union, second_intersection)

    # Function to perform a natural join or Cartesian product with special handling for pairs
    def join_with_cartesian(left, right):
        common_columns = list(set(left.columns) & set(right.columns))
        
        if not common_columns:
            # Perform Cartesian product if no common columns
            left['key'] = 1
            right['key'] = 1
            result = pd.merge(left, right, on='key').drop('key', axis=1)
            return result
        else:
            # Separate columns into regular and pair columns
            pair_columns = [col for col in common_columns if isinstance(left[col].iloc[0], tuple)]
            regular_columns = [col for col in common_columns if col not in pair_columns]
            
            if regular_columns:
                result = pd.merge(left, right, on=regular_columns)
            else:
                left['key'] = 1
                right['key'] = 1
                result = pd.merge(left, right, on='key').drop('key', axis=1)

            if pair_columns:
                for col in pair_columns:
                    if col in common_columns:
                        # Handle common pair columns
                        left_pairs = left[[col]].rename(columns={col: col + '_left'})
                        right_pairs = right[[col]].rename(columns={col: col + '_right'})
                        temp_df = pd.merge(left_pairs.assign(key=1), right_pairs.assign(key=1), on='key').drop('key', axis=1)
                        temp_df[col] = temp_df.apply(lambda row: merge_pairs(row[col + '_left'], row[col + '_right']), axis=1)
                        temp_df = temp_df[[col]]
                        result = result.merge(temp_df, left_index=True, right_index=True)
                        result = result.drop(columns=[col + '_left', col + '_right'], errors='ignore')
                    else:
                        # Handle non-common pair columns by taking the Cartesian product
                        left['key'] = 1
                        right['key'] = 1
                        result = pd.merge(left, right, on='key').drop('key', axis=1)

            return result.drop(columns=[col for col in result.columns if col.endswith('_x') or col.endswith('_y')], errors='ignore')
        
    return reduce(lambda left, right: join_with_cartesian(left, right), dfs)




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
        return pd.DataFrame([head.args])
    if isinstance(body_evaluation, pd.DataFrame):        
        result = []
        for _, row in body_evaluation.iterrows():
            new_tuple = tuple(row.loc[i] if i in vars else i for i in args)
            result.append(new_tuple)

    return pd.DataFrame(result)



def update_approximation(approximation: dict, head: PredicateHead, values: Union[pd.DataFrame, bool], approximation_to_update: str) -> bool:
    changes_made = False
    predicate = head.predicate
    
    if isinstance(values, pd.DataFrame):
        if predicate in approximation:
            if isinstance(approximation[predicate], pd.DataFrame):
                original_length = len(approximation[predicate])
                approximation[predicate] = pd.DataFrame(values)
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
            if not value1.equals(value2):
                return False
            
    return True