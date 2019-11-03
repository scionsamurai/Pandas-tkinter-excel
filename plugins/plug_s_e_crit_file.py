from tkinter import filedialog
from os import getcwd
from SplitEntry import Split_Entry
from SearchDF import SearchDataFrame
from retrieve_info import Retrieve_R
import pandas as pd
from func_file import GenFuncs


class SECritFile:
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
        my_filetypes = [('all files', '.*'), ('CSV files', '.csv')]

        file_key = filedialog.askopenfilename(initialdir=getcwd(),
                                                   title="Select file with search criteria:",
                                                   filetypes=my_filetypes)


        criteria_df = pd.read_csv(file_key, low_memory=False)

        row_list = []
        for index, rows in criteria_df.iterrows():
            my_list = []
            for header in criteria_df.columns:
                val = "rows." + header
                my_list.append(eval(val))
                row_list.append(my_list)
        s_values = ""
        h_values = ""
        for row in row_list:
            for value in row:
                if (row.index(value)+1) < len(row):
                    new_v = str(value) + "\t"
                else:
                    new_v = str(value) + "\n"
                s_values += new_v
        cols_list = []
        for col in criteria_df.columns:
            cols_list.append(col)
            if (cols_list.index(col) + 1) < len(criteria_df.columns):
                h_values += col + "\t"
            else:
                h_values += col

        f_name = (GenFuncs.strip_dir(file_key)).split('.')[0]
        ents = [h_values, s_values]
        Retrieve_R.ow_frames(ents, self.cl, self.of, self.ap, 'xlsx', self.fnl, func=3, file_name=f_name)
