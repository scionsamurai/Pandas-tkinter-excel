import pandas as pd
from tkinter import simpledialog
from SplitEntry import Split_Entry
class VerifyFollowing:
    def run(self,df):
        """
        Plugin for output contents. Adds sort option when outputting file.
        :param df: Input dataframe
        :return: updated dataframe
        """

        et_list = Split_Entry.split(simpledialog.askstring("Title","ET numbers"))
        et_col = simpledialog.askstring("Title", "ET column name")
        hx_col_name = simpledialog.askstring("Title","HX Column")
        col_w_fol_val = simpledialog.askstring("Title","Column that will be searched for following values")

        df_et_list = df[et_col].tolist()
        final_et_list = []

        current_row = 0

        for et_num in df_et_list:
            current_row +=1
            if et_num in et_list:
                hx_id = df.at(current_row,hx_col_name)
                temp_df = df[df[hx_col_name]==hx_id]
                et_num_line = 0
                temp_df_et_list = temp_df[et_col].tolist()
                for temp_df_et_num in temp_df_et_list:
                    et_num_line += 1
                    if temp_df_et_num == et_num:
                        break
                temp_df = temp_df.iloc[et_num_line:]
                df_or_not = temp_df[temp_df[col_w_fol_val] == 25]
                if df_or_not.empty:
                    final_et_list.append(et_num)
        final_df = df.loc[df[et_col].isin(final_et_list)]
        return final_df
