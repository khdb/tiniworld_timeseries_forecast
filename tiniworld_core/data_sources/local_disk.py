
import pandas as pd
import os
from colorama import Fore, Style
from tiniworld_core.logic.params import LOCAL_DATA_PATH


def get_data(path: str,
                     columns: list = None,
                     verbose=True) -> pd.DataFrame:
    """
    return the raw dataset from local disk
    """
    path = os.path.join(
        os.path.expanduser(LOCAL_DATA_PATH),
        f"{path}.csv")

    if verbose:
        print("The path is: ", path)
        print(Fore.MAGENTA + f"Source data from {path}: {'all'} rows " + Style.RESET_ALL)

    try:

        dtypes = {'docDate': object, 'item_code': object, 'item_name': object, 'qty': int, 'store_code': object, 'store_name': object}
        df = pd.read_csv(
                path,
                dtype=dtypes)  # read all rows


        # read_csv(dtypes=...) will silently fail to convert data types, if column names do no match dictionnary key provided.
        #if isinstance(dtypes, dict):
        #    assert dict(df.dtypes) == dtypes

        if columns is not None:
            df.columns = columns

    except pd.errors.EmptyDataError:

        return None  # end of data

    return df
