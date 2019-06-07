import pandas as pd
import time
class OpenFile:
    def __init__(self):
        pass
    def open_file(self, entry, inp_options):
        gen_rules = inp_options[0]
        delimiter = gen_rules['Delimiter']
        terminator = gen_rules['Terminator']
        header_line = gen_rules['Header Line']
        index_col = gen_rules['Index Column']
        chunk = gen_rules['Chunk']
        verbose = gen_rules['Verbose']

        only_cols = inp_options[1]
        dtypes = inp_options[2]
        temp_field = entry.split('/')
        new_field = temp_field[(len(temp_field) - 1)]
        print('Opening ' + new_field)
        start = time.time()

        if entry[-4:] == '.csv':
            if delimiter != None:
                df = pd.read_csv(entry, sep=delimiter, nrows=50, low_memory=False)
                orig_headers = df.columns.values.tolist()
                stripped_headers = []
                for item in orig_headers[0]:
                    try:
                        stripped_headers.append(item.strip())
                    except AttributeError:
                        stripped_headers.append(item)
                new_dtypes = self.df_to_dtypes_dict(df)
                if dtypes != None:
                    for key, value in dtypes.items():
                        # print(orig_headers[0])
                        if key in orig_headers[0]:
                            new_dtypes[key] = value
                        elif key.strip() in orig_headers[0]:
                            new_dtypes[key.strip()] = value
                        elif key in stripped_headers:
                            ind = stripped_headers.index(key)
                            new_dtypes[orig_headers[0][ind]] = value
                        elif key.strip() in stripped_headers:
                            ind = stripped_headers.index(key.strip())
                            new_dtypes[orig_headers[0][ind]] = value
                        else:
                            print(key + ':not found in ' + new_field)
                if only_cols != None:
                    new_only_cols = []
                    for item in only_cols:
                        if item in orig_headers[0]:
                            new_only_cols.append(item)
                        elif item.strip() in orig_headers[0]:
                            new_only_cols.append(item.strip())
                        elif item in stripped_headers:
                            ind = stripped_headers.index(item)
                            new_only_cols.append(orig_headers[0][ind])
                        elif item.strip() in stripped_headers:
                            ind = stripped_headers.index(item.strip())
                            new_only_cols.append(orig_headers[0][ind])
                        else:
                            print(item + ':not found in ' + new_field)

                    try:
                        data = pd.read_csv(entry, sep=delimiter, header=header_line, index_col=index_col,
                                           usecols=new_only_cols, dtype=new_dtypes, verbose=verbose,
                                           lineterminator=terminator, low_memory=False)
                        data.columns = [col.strip() for col in data.columns]
                        return ((data), (entry))
                    except ValueError as e:
                        print(e)
                else:
                    try:
                        data = pd.read_csv(entry, sep=delimiter, header=header_line, index_col=index_col,
                                           dtype=new_dtypes, verbose=verbose, lineterminator=terminator,
                                           low_memory=False)
                        data.columns = [col.strip() for col in data.columns]
                        end = time.time()
                        print('-------'+ str(end-start) +'-------')
                        return ((data), (entry))
                    except ValueError as e:
                        print(e)

            else:
                df = pd.read_csv(entry, nrows=50, low_memory=False)
                # print(df.values.tolist())
                orig_headers = df.columns.values.tolist()
                stripped_headers = []
                for item in orig_headers[0]:
                    try:
                        stripped_headers.append(item.strip())
                    except AttributeError:
                        stripped_headers.append(item)
                new_dtypes = self.df_to_dtypes_dict(df)
                if dtypes != None:
                    for key, value in dtypes.items():
                        # print(orig_headers[0])
                        if key in orig_headers[0]:
                            new_dtypes[key] = value
                        elif key.strip() in orig_headers[0]:
                            new_dtypes[key.strip()] = value
                        elif key in stripped_headers:
                            ind = stripped_headers.index(key)
                            new_dtypes[orig_headers[0][ind]] = value
                        elif key.strip() in stripped_headers:
                            ind = stripped_headers.index(key.strip())
                            new_dtypes[orig_headers[0][ind]] = value
                        else:
                            print(key + ':not found in ' + new_field)
                if only_cols != None:
                    new_only_cols = []
                    for item in only_cols:
                        if item in orig_headers[0]:
                            new_only_cols.append(item)
                        elif item.strip() in orig_headers[0]:
                            new_only_cols.append(item.strip())
                        elif item in stripped_headers:
                            ind = stripped_headers.index(item)
                            new_only_cols.append(orig_headers[0][ind])
                        elif item.strip() in stripped_headers:
                            ind = stripped_headers.index(item.strip())
                            new_only_cols.append(orig_headers[0][ind])
                        else:
                            print(item + ':not found in ' + new_field)

                    try:
                        data = pd.read_csv(entry, header=header_line, chunksize=chunk, index_col=index_col,
                                           usecols=new_only_cols, dtype=new_dtypes, verbose=verbose,
                                           lineterminator=terminator, low_memory=False)
                        data.columns = [col.strip() for col in data.columns]
                        return ((data), (entry))
                    except ValueError as e:
                        print(e)
                else:
                    try:
                        data = pd.read_csv(entry, header=header_line, chunksize=chunk, index_col=index_col,
                                           dtype=new_dtypes, verbose=verbose, lineterminator=terminator,
                                           low_memory=False)
                        data.columns = [col.strip() for col in data.columns]
                        return ((data), (entry))
                    except ValueError as e:
                        print(e)
        elif (entry[-4:] == 'xlsx') or (entry[-4:] == '.xls') or ((entry[-4:])[:3] == 'xls'):
            df = pd.read_excel(entry, sheet_name=0, nrows=50)
            orig_headers = list(df.columns.values)#.tolist()
            stripped_headers = []
            for item in orig_headers[0]:
                try:
                    stripped_headers.append(item.strip())
                except AttributeError:
                    stripped_headers.append(item)
            new_only_cols = []
            try:
                for item in only_cols:
                    if item in orig_headers[0]:
                        new_only_cols.append(item)
                    elif item.strip() in orig_headers[0]:
                        new_only_cols.append(item.strip())
                    elif item in stripped_headers:
                        ind = stripped_headers.index(item)
                        new_only_cols.append(orig_headers[0][ind])
                    elif item.strip() in stripped_headers:
                        ind = stripped_headers.index(item.strip())
                        new_only_cols.append(orig_headers[0][ind])
            except TypeError:
                new_only_cols = None
            new_dtypes = self.df_to_dtypes_dict(df)
            if dtypes != None:
                for key, value in dtypes.items():
                        # print(orig_headers[0])
                        if key in orig_headers[0]:
                            new_dtypes[key] = value
                        elif key.strip() in orig_headers[0]:
                            new_dtypes[key.strip()] = value
                        elif key in stripped_headers:
                            ind = stripped_headers.index(key)
                            new_dtypes[orig_headers[0][ind]] = value
                        elif key.strip() in stripped_headers:
                            ind = stripped_headers.index(key.strip())
                            new_dtypes[orig_headers[0][ind]] = value
                        else:
                            print(key + ':not found in ' + new_field)

            data = pd.read_excel(entry, sheet_name=0, header=header_line, index_col=index_col,
                                 usecols=new_only_cols, dtype=new_dtypes, verbose=verbose)
            data.columns = [col.strip() for col in data.columns]
            end = time.time()
            print('-------'+ str(end-start) +'-------')
            return ((data), (entry))
        elif entry[-3:] == '.h5':
            data = pd.read_hdf(entry,'df')
            end = time.time()
            print('-------'+ str(end-start) +'-------')
            return ((data), (entry))
        else:
            df_empty = pd.DataFrame({'A':[]})
            end = time.time()
            print('-------'+ str(end-start) +'-------')
            return df_empty
    def map_func(self, data_frame, indexes):
        new_list = {}
        new_list.update(indexes)
        for column in data_frame.columns.values:
            for value in data_frame[column].values:
                if value not in indexes:
                    new_list[value] = ((len(indexes)+1) + len(new_list))
        for item in new_list:
            for column in data_frame.columns.values:
                data_frame[column].map({item:new_list[item]})
        return new_list

    def df_to_dtypes_dict(self, df):
        for col in df.columns.values:
            if df[col].empty == True:
                df.drop(col, axis=1)
        df_int = df.select_dtypes(include=['int64'])
        converted_int2 = df_int.apply(pd.to_numeric,downcast='unsigned')
        converted_int = converted_int2.apply(pd.to_numeric,downcast='signed')
        df_float = df.select_dtypes(include=['float'])
        converted_float = df_float.apply(pd.to_numeric,downcast='float')
        df_obj = df.select_dtypes(include=['object'])
        converted_obj = pd.DataFrame()
        for col in df_obj.columns:
            num_unique = len(df_obj[col].unique())
            num_total = len(df_obj[col])
            if num_unique / num_total < 0.5:
                converted_obj.loc[:,col] = df_obj[col].astype('category')
            else:
                converted_obj.loc[:, col] = df_obj[col]
        optimized_df = df.copy()
        optimized_df[converted_int.columns] = converted_int
        optimized_df[converted_float.columns] = converted_float
        optimized_df[converted_obj.columns] = converted_obj

        dtypes = optimized_df.dtypes
        dtypes_col = dtypes.index
        dtypes_type = [i.name for i in dtypes.values]
        column_types = dict(zip(dtypes_col, dtypes_type))
        return column_types
