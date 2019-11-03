from tkinter import filedialog
from os import getcwd
import numpy as np
import pandas as pd
class SaveSelected:
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
        """
        Save Dataframes that are checked in main window to a single file.
        """
        new_output = []
        output_filetypes = [('HD5', '.h5'), ('CSV files', '.csv')]
        save_answer = filedialog.asksaveasfilename(initialdir=getcwd(),
                                                   title="Please select save location and name:",
                                                   filetypes=output_filetypes,
                                                   defaultextension='.h5')
        for key in self.fnl:
            if self.cl[self.fnl.index(key)][2].get() == 1:
                if self.of[self.fnl.index(key)].fill_val != {}:
                    temp_df = self.of[self.fnl.index(key)].df.copy()
                    for col, val in self.of[self.fnl.index(key)].fill_val.items():
                        temp_df[col].replace(val, np.NaN, inplace=True)
                    new_output.append(temp_df)
        try:
            new_new_output = pd.concat(new_output, axis=0, sort=False, ignore_index=True)
        except ValueError:
            new_new_output = new_output
        if save_answer[-3:] == '.h5':
            new_new_output.to_hdf(save_answer, key='df', mode='w', format='table')
        elif save_answer[-4:] == '.csv':
            new_new_output.to_csv(save_answer, index=False)
        print('saved')
        del new_output