from SearchDF import SearchDataFrame
from SplitEntry import Split_Entry
class FileFrame:
    def __init__(self, data_frame=[], file_location=None, fill_col_val={}):
        self.df = data_frame
        self.key = file_location
        temp_var = file_location.split('/')
        self.name = temp_var[(len(temp_var)-1)]
        self.fill_val = fill_col_val
        self.int_cols = []

    def search_col(self, col, values, zeros_dict):
        real_list = Split_Entry.split(values)  # Splits main window Search Item(s) into list
        if not isinstance(real_list, str):
            func_var = 2
        else:
            func_var = 1
        try:
            temp_output = SearchDataFrame.criteria_by_column(col, real_list, self.name, func_var, self.df).copy()
            if not temp_output.empty:
                for col in self.fill_val:  # Strip space saving Filler Values from output
                    dtype_var = temp_output[col].dtype
                    if str(dtype_var)[:3] == 'int' or str(dtype_var)[:3] == 'uin':
                        self.int_cols.append(col)
                    temp_output[col].replace(self.fill_val[col], "", inplace=True)
                for key, val in zeros_dict.items(): # Apply Leading Zeros rules to output
                    try:
                        temp_str = '{0:0>' + str(val) + '}'
                        if str(temp_output[key].dtype)[:3] == 'int' or str(temp_output[key].dtype)[:3] == 'uin' or \
                                str(temp_output[key].dtype)[:5] == 'float' or key in self.int_cols: # For Numbers
                            temp_output[key] = temp_output[key].apply(lambda x: temp_str.format(x))
                        elif str(temp_output[key].dtype)[:3] == 'cat':
                            temp_output[key] = temp_output[key].astype('object')
                            temp_output[key] = temp_output[key].str.zfill(int(val))
                        else: # For Strings
                            try:
                                temp_output[key] = temp_output[key].str.zfill(int(val))
                            except AttributeError:
                                pass
                    except KeyError: # Catch if Rule Header wasn't in output results
                        pass
            return temp_output
        except (TypeError, AttributeError):
            print('flag1122334455')


