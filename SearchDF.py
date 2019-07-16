from SplitEntry import Split_Entry
from pandas import concat, DataFrame
class SearchDataFrame:
    def criteria_by_column(search_column, search_items, new_field, data_frames):
        data = data_frames

        def strip_col_vals(column):
            try:
                data[column] = data[column].str.strip()
            except (AttributeError, KeyError):
                pass

        def split_s_vals(search_item):
            real_list = Split_Entry.split(search_item)  # If able splits main window Search Item(s) into list
            if not isinstance(real_list, str):
                func_var = 2
            else:
                func_var = 1
            return real_list, func_var

        def not_in_list(list,var):
            if var in list:
                return False
            else:
                return True

        def is_float(string):
            try:
                float(string)
                return True
            except ValueError:
                return False

        def search_command(input_l,columns):
            exec_str = 'new_df_list['
            search_vars = input_l.split('\t')
            digit_vars = []
            for e in search_vars:
                print(e)
                print(is_float(e))
                if is_float(e):
                    digit_vars.append(e)
            for v in columns:
                if columns.index(v) != (len(columns) - 1):
                    if not_in_list(digit_vars, search_vars[columns.index(v)]):
                        exec_str += '(new_df_list[cols[' + str(columns.index(v)) + ']] == search_vars[' + str(
                            columns.index(v)) + ']) & '
                    else:
                        exec_str += '(new_df_list[cols[' + str(
                            columns.index(v)) + ']] == float(search_vars[' + str(
                            columns.index(v)) + '])) & '
                else:
                    if not_in_list(digit_vars, search_vars[columns.index(v)]):
                        exec_str += '(new_df_list[cols[' + str(columns.index(v)) + ']] == search_vars[' + str(
                            columns.index(v)) + '])]'
                    else:
                        exec_str += '(new_df_list[cols[' + str(
                            columns.index(v)) + ']] == float(search_vars[' + str(
                            columns.index(v)) + ']))]'
            return exec_str, search_vars
        col_list_check = Split_Entry.split(search_column)

        if not isinstance(col_list_check, str):
            input_list = Split_Entry.split(search_items.split('\n'),1) # Split input by newline chars
            col_list_dict = {}
            cols = []
            for c in col_list_check: # Create list and dict for list of search variables per column
                col_list_dict[c] = []
                cols.append(c)
            if not isinstance(input_list, str):
                for i in input_list: # For var set in input list
                    search_vars = i.split('\t')
                    for x in cols:
                        if search_vars[cols.index(x)] not in col_list_dict[x]:
                            col_list_dict[x].append(search_vars[cols.index(x)])

            else:
                search_vars = input_list.split('\t')
                print(search_vars)
                for x in cols:
                    if search_vars[cols.index(x)] not in col_list_dict[x]:
                        col_list_dict[x].append(search_vars[cols.index(x)])
            df_list = []
            for m in range(len(cols)): # For each search column
                df_list.append(data.loc[data[cols[m]].isin(col_list_dict[cols[m]])])
                #^ creates list of locations that have matches in each column
            new_df_list = DataFrame.drop_duplicates(concat(df_list, axis=0, sort=False, ignore_index=True))
            new_df = []
            if not isinstance(input_list, str):
                for i in input_list:
                    exec_str, search_vars = search_command(i, cols)
                    new_df.append(eval(exec_str))
                new_new_df = concat(new_df, axis=0, sort=False, ignore_index=True)
                new_new_df = DataFrame.drop_duplicates(new_new_df)
                return new_new_df
            else:
                exec_str, search_vars = search_command(input_list, cols)
                new_new_df = eval(exec_str)
                return new_new_df

        search_item, int_str = split_s_vals(search_items)
        if int_str == 1:
            strip_col_vals(search_column)
            try:
                try:
                    rows_w_matching_crit = data[data[search_column] == str(search_item)]
                    if len(rows_w_matching_crit.values) >= 1:
                        return rows_w_matching_crit
                    else:
                        # print('1')
                        print(search_item + ' isn\'t in ' + new_field)
                except KeyError:
                    print(search_column + ' Header isn\'t in ' + new_field)
            except FutureWarning:
                #"""
                try:
                    rows_w_matching_crit = data[data[search_column] == float(search_item)]
                    if len(rows_w_matching_crit.values) >= 1:
                        return rows_w_matching_crit
                    else:
                        # print('2')
                        print(search_item + ' isn\'t in ' + new_field)
                except (KeyError, ValueError) as e:
                    # print('3')
                    print(str(e)[34:] + ' isn\'t in ' + new_field)
                    #"""
        else:
            strip_col_vals(search_column)
            try:
                ## failing when a value error is thrown
                try:
                    rows_w_matching_crit = data.loc[data[search_column].isin(search_item)]
                    if len(rows_w_matching_crit.values) >= 1:
                        return rows_w_matching_crit
                    else:
                        print('4')
                        print('No results in ' + new_field)
                except KeyError:
                    print(search_column + ' Header isn\'t in ' + new_field)
            except (FutureWarning, TypeError):
                try:
                    num_list = []
                    str_list = []
                    for item in search_item:
                        try:
                            val = float(item)
                            num_list.append(item)
                        except ValueError:
                            str_list.append(item)
                    print(str_list)
                    print('^^not in numeric column^^')
                    rows_w_matching_crit = data.loc[data[search_column].isin(num_list)]
                    if len(rows_w_matching_crit.values) >= 1:
                        return rows_w_matching_crit
                    else:
                        print('5')
                        print('No results in ' + new_field)
                except (KeyError, ValueError) as e:
                    # print('6')
                    print(str(e)[34:] + ' isn\'t in ' + new_field)

