class SearchDataFrame:
    def criteria_by_column(i, search_column, search_item, new_field, int_str, data_frames):
        data = data_frames[i]
        if int_str == 1:
            try:
                try:
                    rows_w_matching_crit = data[data[search_column] == search_item]
                    if len(rows_w_matching_crit.values) >= 1:
                        return rows_w_matching_crit
                    else:
                        print(search_item + ' isn\'t in ' + new_field[:-4])
                except KeyError:
                    print(search_column + ' Header isn\'t in ' + new_field[:-4])
            except FutureWarning:
                try:
                    rows_w_matching_crit = data[data[search_column] == float(search_item)]
                    return rows_w_matching_crit
                except (KeyError, ValueError) as e:
                    print(str(e)[34:] + ' isn\'t in ' + new_field[:-4])
        else:
            try:
                try:
                    rows_w_matching_crit = data[data[search_column] == str(search_item)]
                    if len(rows_w_matching_crit.values) >= 1:
                        return rows_w_matching_crit
                    else:
                        print(search_item + ' isn\'t in ' + new_field[:-4])
                except KeyError:
                    print(search_column + ' isn\'t in ' + new_field[:-4])
            except FutureWarning:
                try:
                    rows_w_matching_crit = data[data[search_column] == float(search_item)]
                    return rows_w_matching_crit
                except (KeyError, ValueError) as e:
                    print(str(e)[34:] + ' isn\'t in ' + new_field[:-4])
