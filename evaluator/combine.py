from components import *
from typing import Union, List
import pandas as pd
from functools import reduce
from .helpers import *

def combine_literal_evaluations(
        literal_evaluations: List[Union[pd.DataFrame,bool]]
) -> Union[pd.DataFrame,bool]:

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

    if not dfs:
        boolean_evaluations = [eval for eval in literal_evaluations if isinstance(eval, bool)]
        return reduce(lambda x, y: x and y, boolean_evaluations, True)


    # Iterate over the DataFrames and their indices
    for idx, df in enumerate(dfs):
        new_columns = {col: f"{col}_{idx}" for col in df.columns if all(isinstance(item, dict) for item in df[col])}
        df.rename(columns=new_columns, inplace=True)
    # Perform a natural join between all DataFrames
    combined_df = dfs[0]
    for df in dfs[1:]:
        common_columns = combined_df.columns.intersection(df.columns)
        if common_columns.any():
            combined_df = pd.merge(combined_df, df, how='inner')
        else:
            combined_df = pd.merge(combined_df, df, how='cross')
    
    # Identify columns with common prefixes and merge dictionaries
    column_groups = {}
    for col in combined_df.columns:
        prefix = col.rsplit('_', 1)[0]
        if prefix not in column_groups:
            column_groups[prefix] = []
        column_groups[prefix].append(col)
    
    def merge_dicts_series(series):
        merged = {}
        for d in series:
            for k, v in d.items():
                if k in merged:
                    if (merged[k] == '1' and v == '0') or (merged[k] == '0' and v == '1'):
                        return None  # Conflict, drop this row
                    if (merged[k] == '1' and v == '1/2') or (merged[k] == '1/2' and v == '1'):
                        merged[k] = '1/2'
                    elif (merged[k] == '0' and v == '1/2') or (merged[k] == '1/2' and v == '0'):
                        merged[k] = '1/2'
                    else:
                        merged[k] = v
                else:
                    merged[k] = v
        return merged

    for prefix, columns in column_groups.items():
        if len(columns) > 1:
            combined_df[prefix] = combined_df[columns].apply(merge_dicts_series, axis=1)
            combined_df.drop(columns=columns, inplace=True)
            combined_df.dropna(subset=[prefix], inplace=True)
        elif len(columns) == 1 and any(all(isinstance(item, dict) for item in combined_df[col]) for col in columns):
            original_col_name = prefix
            combined_df.rename(columns={columns[0]: original_col_name}, inplace=True)
    
    return combined_df
 
