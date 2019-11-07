import pandas as pd
from tkinter import simpledialog
from SplitEntry import Split_Entry
class Sort:
    def run(self,df):
        """
        Plugin for output contents. Adds sort option when outputting file.
        :param df: Input dataframe
        :return: updated dataframe
        """
        column = simpledialog.askstring("Sort","Column name to sort")
        sorted_df = df.sort_values(by=Split_Entry.split(column))

        return sorted_df
