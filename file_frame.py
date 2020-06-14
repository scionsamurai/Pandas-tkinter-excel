"""
Class for storing File data and fill values (generated when optimizing data size).
"""
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

    def search_col(self, column, values, zeros_dict, func=0):
        """
        Retrieve info from file by searching info under header.
        :param column: Column to Search - copied from main window.
        :param values: Search Item(s) - copied from main window.
        :param zeros_dict: Dictionary from Output settings for columns that user wants x leading zeros.
        :return: Returns a DataFrame with resulting columns from Search or None if no results.
         """
        try:
            if func == 0:
                temp_output = SearchDataFrame.criteria_by_column(column, values, self.name, self.df).copy()
            else:
                temp_output = self.df.copy()
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
        except (TypeError, AttributeError): # Catch AttributeError from SearchDataFrame.copy when result is noneType
            pass


