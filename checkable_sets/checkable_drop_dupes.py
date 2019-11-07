import pandas as pd
from tkinter import simpledialog, messagebox
from SplitEntry import Split_Entry
class DropDupes:
    def run(self,df):
        """
        Plugin for output contents. Adds sort option when outputting file.
        :param df: Input dataframe
        :return: updated dataframe
        """
        first_last_Q = messagebox.askyesno("Drop Duplicates",
                                           "Would you like to keep the first occurrence?\n (Last occurrence kept if \"No\")")
        if first_last_Q:
            first_last = "first"
        else:
            first_last = "last"
        ask_headers = simpledialog.askstring("Drop Duplicates", "What Columns would you like to check for duplicates?")
        headers_list = Split_Entry.split(ask_headers)
        df.drop_duplicates(headers_list, first_last, inplace=True)
        return df