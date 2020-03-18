import pandas as pd
from typing import Dict


class MissingValue(object):
    def __init__(self, pd_df: pd.DataFrame) -> None:
        self.na_count_dict = {}
        self.na_index_dict = {}
        self.data = pd_df

    def __str__(self) -> Dict:
        return self.na_count_dict
    
    def __getitem__(self, item) -> int:
        return self.na_count_dict[item]

    def missing_value_summary(self, verbose=False):
        na_list = self.data.isna().sum(axis=0)
        for obj in na_list.index:
            if na_list[obj] != 0:
                self.na_count_dict[obj] = na_list[obj]
                if verbose:
                    print("In column\033[91m {}\033[00m , "
                          "we have\033[91m {}\033[00m missing values.".format(obj, na_list[obj]))
        if not self.na_count_dict:
            if verbose:
                print("No missing value found!")
        return self.na_count_dict

    def missing_value_enumerator(self):
        self.na_index_dict = {}
        if not self.na_count_dict:
            raise Exception("Please use function missing_value_summary() first.")
        for item in self.na_count_dict:
            self.na_index_dict[item] = set()
            for i in range(len(self.data)):
                if self.data.isna().loc[i, item]:
                    self.na_index_dict[item].add(i)
