from _funcs.SplitEntry import Split_Entry
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

        def search_command(input_l,columns):
            search_vars = input_l.split('\t')
            query = ' and '.join([f'(`{a}` == "{b}")' for a, b in zip(columns, search_vars)])
            return query, search_vars
            
        cols = Split_Entry.split(search_column)

        if not isinstance(cols, str):
            input_list = Split_Entry.split(search_items.split('\n'), 1)  # Split input by newline chars
            for c in cols:  # Strip leading/trailing whitespace from search Cols
                strip_col_vals(c)
            new_df = []
            if not isinstance(input_list, str):
                for i in input_list:
                    exec_str, search_vars = search_command(i, cols)
                    new_df.append(data.query(exec_str))
                new_new_df = concat(new_df, axis=0, sort=False, ignore_index=True)
                new_new_df = DataFrame.drop_duplicates(new_new_df)
                return new_new_df
            else:
                exec_str, search_vars = search_command(input_list, cols)
                try:
                    new_new_df = data.query(exec_str)
                    return new_new_df
                except:
                    print("Error in SearchDF")

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
        else:
            strip_col_vals(search_column)
            try:
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
