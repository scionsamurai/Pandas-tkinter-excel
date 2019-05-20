class SearchDataFrame:
    def criteria_by_column(i, search_column, search_item, new_field, int_str, data_frames):
        data = data_frames[i]
        try:
            data[search_column] = data[search_column].str.strip()
        except AttributeError:
            pass
        if int_str == 1:
            try:
                try:
                    rows_w_matching_crit = data[data[search_column] == str(search_item)]
                    if len(rows_w_matching_crit.values) >= 1:
                        return rows_w_matching_crit
                    else:
                        # print('1')
                        print(search_item + ' isn\'t in ' + new_field[:-4])
                except KeyError:
                    print(search_column + ' Header isn\'t in ' + new_field[:-4])
            except FutureWarning:
                try:
                    rows_w_matching_crit = data[data[search_column] == float(search_item)]
                    if len(rows_w_matching_crit.values) >= 1:
                        return rows_w_matching_crit
                    else:
                        # print('2')
                        print(search_item + ' isn\'t in ' + new_field[:-4])
                except (KeyError, ValueError) as e:
                    # print('3')
                    print(str(e)[34:] + ' isn\'t in ' + new_field[:-4])
        else:
            try:
                try:
                    rows_w_matching_crit = data[data[search_column] == str(search_item)]
                    if len(rows_w_matching_crit.values) >= 1:
                        return rows_w_matching_crit
                    else:
                        # print('4')
                        print(search_item + ' isn\'t in ' + new_field[:-4])
                except KeyError:
                    print(search_column + ' Header isn\'t in ' + new_field[:-4])
            except FutureWarning:
                try:
                    rows_w_matching_crit = data[data[search_column] == float(search_item)]
                    if len(rows_w_matching_crit.values) >= 1:
                        return rows_w_matching_crit
                    else:
                        # print('5')
                        print(search_item + ' isn\'t in ' + new_field[:-4])
                except (KeyError, ValueError) as e:
                    # print('6')
                    print(str(e)[34:] + ' isn\'t in ' + new_field[:-4])

