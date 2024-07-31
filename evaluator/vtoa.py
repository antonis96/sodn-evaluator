from components import *
from typing import Union
import pandas as pd
from .helpers import *


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
            if new_tuple not in result:
                result.append(new_tuple)

    return pd.DataFrame(result)