from tkinter import simpledialog, messagebox
import shelve
import numpy as np
import pandas as pd
from func_file import GenFuncs
from SplitEntry import Split_Entry
from retrieve_info import Retrieve_R
class DropDupes:
    def __init__(self):
        self.of = []
        self.fnl = []
        self.cl = []
        self.ap = 0
    def run(self, opened_files, file_name_list, checked_list, auto_open):
        self.of = opened_files
        self.fnl = file_name_list
        self.cl = checked_list
        self.ap = auto_open
        initiateQ = messagebox.askyesno("Drop Duplicates", "Would you like to drop duplicates from the checked files?")
        new_output = []
        first_last_Q = messagebox.askyesno("Drop Duplicates",
                                           "Would you like to keep the first occurrence?\n (Last occurrence kept if \"No\")")
        counter_count = 0
        delete_list = []
        counter_dict = {}
        if first_last_Q:
            first_last = "first"
        else:
            first_last = "last"
        if initiateQ:
            var_file = shelve.open('var_file')
            try:
                zeros_dict = var_file['lead_zeroes']
            except KeyError:
                zeros_dict = {}
            var_file.close()
            for key in self.fnl:
                if self.cl[self.fnl.index(key)][2].get() == 1:
                    if self.of[self.fnl.index(key)].fill_val != {}:
                        temp_df = self.of[self.fnl.index(key)].df.copy()
                        for col, val in self.of[self.fnl.index(key)].fill_val.items():
                            temp_df[col].replace(val, np.NaN, inplace=True)
                        temp_df['Counter'] = range(counter_count, len(temp_df) + counter_count)
                        counter_dict[key] = [counter_count, len(temp_df) + counter_count]
                        counter_count += len(temp_df)
                    else:
                        ph = self.of[self.fnl.index(key)].df.copy()
                        ph['Counter'] = range(counter_count, len(ph) + counter_count)
                        counter_dict[key] = [counter_count, len(ph) + counter_count]
                        counter_count += len(ph)
                        temp_df = self.of[self.fnl.index(key)].df
                    GenFuncs.add_lead_0s(temp_df, zeros_dict)
                    new_output.append(temp_df)
            try:
                new_new_output = pd.concat(new_output, axis=0, sort=False, ignore_index=True)
            except ValueError:
                new_new_output = new_output
            ask_headers = simpledialog.askstring("Drop Duplicates",
                                                 "What Columns would you like to check for duplicates?")
            headers_list = Split_Entry.split(ask_headers)
            new_new_output.drop_duplicates(headers_list, first_last, inplace=True)
            keep_all_Q = messagebox.askyesno("Drop Duplicates", "Keep all results?")
            if not keep_all_Q:
                for key, value in counter_dict.items():
                    output_file_Q = messagebox.askyesno("Drop Duplicates", "Keep rows from " + key + "?")
                    if not output_file_Q:
                        delete_list.append(counter_dict[key])
                        counter_dict[key] = []
            for list in delete_list:
                new_new_output.drop(new_new_output.index[(new_new_output['Counter'] >= list[0]) &
                                                         (new_new_output['Counter'] <= list[1])], inplace=True)
            del new_new_output['Counter']
            Retrieve_R.ow_frames("", new_new_output, "", self.ap, 'xlsx', "", func=1, file_name="DropDupes")
