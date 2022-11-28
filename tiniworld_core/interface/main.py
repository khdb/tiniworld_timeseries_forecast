import numpy as np
import pandas as pd

from colorama import Fore, Style

from tiniworld_core.data_sources.local_disk import get_data


def preprocess():
    """
    Preprocess the dataset by chunks fitting in memory.
    parameters:
    - source_type: 'train' or 'val'
    """

    print("\n⭐️ Use case: preprocess")

    data_ = get_data("ticket-sales")

    # print message if data is none
    if data_ is None:
        print(Fore.BLUE + "\nNo data in latest chunk..." + Style.RESET_ALL)

    print("Shape of the data frame: ", data_.shape)

    return None


if __name__ == '__main__':
    preprocess() #test get data
