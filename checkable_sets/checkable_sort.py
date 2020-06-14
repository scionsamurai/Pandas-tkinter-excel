import pandas as pd
from tkinter import simpledialog
from SplitEntry import Split_Entry
from sort_popup import SortPopup
import shelve, os
class Sort:
    def run(self,df):
        """
        Plugin for output contents. Adds sort option when outputting file.
        :param df: Input dataframe
        :return: updated dataframe
        """
        var_file = shelve.open(os.path.join(os.environ['HOME'],'var_file'))
        plug_l = var_file['plug_lists']
        dupes_plug = plug_l['Sort']
        var = dupes_plug[0]
        code = dupes_plug[1]
        save_set = dupes_plug[2]
        if save_set == False:
            popup_win =SortPopup()
            usr_inp = (popup_win.output1, popup_win.save)
            #column = simpledialog.askstring("Sort","Column name to sort")
            sorted_df = df.sort_values(by=Split_Entry.split(usr_inp[0]))
            if usr_inp[1]:
                save_set = usr_inp[0]
                plug_l['Sort'] = [var, code, save_set]
                var_file['plug_lists'] = plug_l
            else:
                plug_l['Sort'] = [var, code, False]
                var_file['plug_lists'] = plug_l
        else:
            sorted_df = df.sort_values(by=Split_Entry.split(save_set))
        return sorted_df
