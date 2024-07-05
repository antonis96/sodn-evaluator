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
def generate_relations(elements):
    relations = []
    n = len(elements)
    for r in range(n + 1):
        for subset in itertools.combinations(elements, r):
            relations.append(set(subset))
    return relations

# Function to process the input list and associate values
def associate_values(atom_type, H_u):
    associated_values = []
    for i, element in enumerate(atom_type):
        if element == 'i':
            associated_values.append(list(H_u))
        elif isinstance(element, list):
            pairs = list(itertools.product(H_u, repeat=len(element))) 
            subsets = generate_relations(pairs)
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
        c = cartesian_product([H_u if not isinstance(element, list) else [ 
            {r:1} for r in list(itertools.combinations_with_replacement(H_u, len(element)))
        ] for element in predicate_type])   
        df = pd.DataFrame(c)
        return df


def initialize_under_approximation(program: Program, predicate: str) -> pd.DataFrame:
    predicate_type = program.types[predicate]
    if predicate_type == 'o':
        return False
    else:  # if it is a list
        c = cartesian_product([set() if not isinstance(element, list) else 
                [ (set(), set() ) ] 
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
        indexes_to_include = [args.index(var) for var in vars]
        associated_values = associate_values(atom_type, H_u)
        full_df = pd.DataFrame(cartesian_product(associated_values))
        constants = [str(v) for v in atom.args if str(v) not in vars]
        for c in constants:
            if f"dt_{c}" not in under_approximation.keys():
                matched_df[c] = [c]
            else:
                dt_tuples = set(under_approximation[f"dt_{c}"].apply(tuple, axis=1)) 
                ndf_tuples = set(over_approximation[f"ndf_{c}"].apply(tuple, axis=1))
                matched_df[c] = [(dt_tuples, ndf_tuples)]

        unmatched = []
        for f_row in full_df.itertuples(index=False, name=None):
            valid_match = False
            for m_row in matched_df.itertuples(index=False, name=None):
                if rows_match(f_row, m_row, atom_type):
                    valid_match = True
                    break
            if not valid_match:
                unmatched.append(f_row)
     
        unmatched  = [tuple((el, el) if isinstance(el, set) else el for el in tup) for tup in unmatched]
        data_selected = [[r[i] for i in indexes_to_include] for r in unmatched]
        return pd.DataFrame(data_selected,columns=vars)

 
def rows_match(f_row, s_row, atom_type):
    for i in range(len(f_row)):
        if isinstance(atom_type[i], str):
            if f_row[i] != s_row[i]:
                return False
        elif isinstance(atom_type[i], list):
            if  not f_row[i].issuperset(s_row[i][0]) or not f_row[i].issubset(s_row[i][1]):
                return False
       
    return True

def match(a: tuple, b:tuple, under_approximation: dict, over_approximation: dict):
    if len(a) != len(b):
        return {}, False
    sub = {}
    for ai, bi in zip(a, b):
        if ai.arg_type == 'data_const' and ai.value != bi:
            return {}, False
        elif ai.arg_type == 'predicate_const':
            dt_tuples = set(under_approximation[f"dt_{ai.value}"].apply(tuple, axis=1))
            ndf_tuples = set(over_approximation[f"ndf_{ai.value}"].apply(tuple, axis=1))
            if not dt_tuples.issuperset(bi[0]) or not ndf_tuples.issubset(bi[1]):
                return {}, False
                    
        if ai.arg_type == 'variable':
            if ai not in sub:
                sub[ai.value] = bi
            elif isinstance(ai, str) and sub[ai.value] != bi:
                return {}, False
    return sub, True


def variable_predicate_atov(literal: Literal) -> pd.DataFrame:
    atom = literal.atom
    predicate = atom.predicate
    args = tuple([str(arg.value) for arg in atom.args ])
    arg_vars = [str(v) for v in tuple(atom.args) if v.value.isupper()]
    arg_constants = [const for const in args if const not in arg_vars]
    is_negated = literal.negated

    var_subs = list(itertools.product(H_u, repeat=len(arg_vars))) # possible substitutions of argument variables
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
                expanded_data = df.apply(lambda row: expand_row(row, ['1', '1/2']), axis=1).tolist()
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




def combine_literal_evaluations(literal_evaluations: List[Union[pd.DataFrame, bool]]) -> Union[pd.DataFrame, bool]:
    if not literal_evaluations:
        return pd.DataFrame()  # Return an empty dataframe if the list is empty

    # Filter out boolean values, check for False, and check for empty dataframes
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
    def merge_dicts(dict1, dict2):
        for k in dict2.keys():
            if k in dict1 and dict1[k] != dict2[k]:
                return None  # Conflict found, return None to indicate no merge
        merged_dict = dict1.copy()
        merged_dict.update(dict2)
        return merged_dict

    def merge_relations(df1,df2):
        result_df = pd.DataFrame()

        # Cartesian product of rows for columns containing dictionaries
        common_columns = set(df1.columns).intersection(set(df2.columns))

        for column in common_columns:
            if isinstance(df1[column].iloc[0], dict):
                merged_rows = []
                for idx1, row1 in df1.iterrows():
                    for idx2, row2 in df2.iterrows():
                        merged_dict = merge_dicts(row1[column], row2[column])
                        if merged_dict:
                            merged_rows.append({column: merged_dict})
                result_df = pd.concat([result_df, pd.DataFrame(merged_rows)], ignore_index=True)

        # Add non-common columns from both dataframes
        for column in set(df1.columns).difference(common_columns):
            df1_non_common = df1[[column]].loc[result_df.index // len(df2)].reset_index(drop=True)
            result_df = pd.concat([result_df, df1_non_common], axis=1)

        for column in set(df2.columns).difference(common_columns):
            df2_non_common = df2[[column]].loc[result_df.index % len(df2)].reset_index(drop=True)
            result_df = pd.concat([result_df, df2_non_common], axis=1)

        return result_df
    
    return reduce(lambda left, right: merge_relations(left, right), dfs)




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
        return pd.DataFrame([head.args], dtype=str)
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
