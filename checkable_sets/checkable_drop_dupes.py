import pandas as pd
from tkinter import simpledialog, messagebox
from SplitEntry import Split_Entry
from dupes_popup import DupesPopup
from tkinter import Toplevel
import shelve
class DropDupes:
    def run(self,df):
        """
        Plugin for output contents. Adds sort option when outputting file.
        :param df: Input dataframe
        :return: updated dataframe
        """

        var_file = shelve.open('var_file')
        plug_l = var_file['plug_lists']
        dupes_plug = plug_l['DropDupes']
        var = dupes_plug[0]
        code = dupes_plug[1]
        save_set = dupes_plug[2]
        if save_set == False:
            popup_win = DupesPopup()
            usr_inp = (popup_win.output1,popup_win.output2, popup_win.save)
            headers_list = Split_Entry.split(usr_inp[0])
            df.drop_duplicates(headers_list, usr_inp[1], inplace=True)
            print(usr_inp[2])
            if usr_inp[2]:
                save_set = [usr_inp[1], headers_list]
                plug_l['DropDupes'] = [var, code, save_set]
                var_file['plug_lists'] = plug_l
            else:
                plug_l['DropDupes'] = [var, code, False]
                var_file['plug_lists'] = plug_l
        else:
            df.drop_duplicates(save_set[1], save_set[0], inplace=True)

        var_file.close()
        return df
