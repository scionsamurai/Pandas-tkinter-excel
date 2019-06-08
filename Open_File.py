import pandas as pd
import numpy as np
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
                new_dtypes = {}
                if dtypes != None:
                    for key, value in dtypes.items():
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
                if new_dtypes == {}:
                    new_dtypes = None
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
                        data = self.reduce_mem_usage(data)[0]
                        return ((data), (entry))
                    except ValueError as e:
                        print(e)
                else:
                    try:
                        data = pd.read_csv(entry, sep=delimiter, header=header_line, index_col=index_col,
                                           dtype=new_dtypes, verbose=verbose, lineterminator=terminator,
                                           low_memory=False)
                        data.columns = [col.strip() for col in data.columns]
                        data = self.reduce_mem_usage(data)[0]
                        end = time.time()
                        print('-------'+ str(end-start) +'-------')
                        return ((data), (entry))
                    except ValueError as e:
                        print(e)

            else:
                df = pd.read_csv(entry, nrows=50, low_memory=False)
                orig_headers = df.columns.values.tolist()
                stripped_headers = []
                for item in orig_headers[0]:
                    try:
                        stripped_headers.append(item.strip())
                    except AttributeError:
                        stripped_headers.append(item)
                new_dtypes = {}
                if dtypes != None:
                    for key, value in dtypes.items():
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
                if new_dtypes == {}:
                    new_dtypes = None
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
                        data = self.reduce_mem_usage(data)[0]
                        return ((data), (entry))
                    except ValueError as e:
                        print(e)
                else:
                    try:
                        data = pd.read_csv(entry, header=header_line, chunksize=chunk, index_col=index_col,
                                           dtype=new_dtypes, verbose=verbose, lineterminator=terminator,
                                           low_memory=False)
                        data.columns = [col.strip() for col in data.columns]
                        data = self.reduce_mem_usage(data)[0]
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
            new_dtypes = {}
            if dtypes != None:
                for key, value in dtypes.items():
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
            if new_dtypes == {}:
                new_dtypes = None

            data = pd.read_excel(entry, sheet_name=0, header=header_line, index_col=index_col,
                                 usecols=new_only_cols, dtype=new_dtypes, verbose=verbose)
            data.columns = [col.strip() for col in data.columns]
            data = self.reduce_mem_usage(data)[0]
            end = time.time()
            print('-------'+ str(end-start) +'-------')
            return ((data), (entry))
        elif entry[-3:] == '.h5':
            data = pd.read_hdf(entry,'df')
            data = self.reduce_mem_usage(data)[0]
            end = time.time()
            print('-------'+ str(end-start) +'-------')
            return ((data), (entry))
        else:
            df_empty = pd.DataFrame({'A':[]})
            end = time.time()
            print('-------'+ str(end-start) +'-------')
            return df_empty

    def reduce_mem_usage(self,props):
        start_mem_usg = props.memory_usage().sum() / 1024 ** 2
        print("Memory usage of properties dataframe is :", start_mem_usg, " MB")
        NAlist = []  # Keeps track of columns that have missing values filled in.
        for col in props.columns:
            if props[col].dtype != object and props[col].dtype != 'datetime64[ns]':  # Exclude strings and dates

                # Print current column type
                print("******************************")
                print("Column: ", col)
                print("dtype before: ", props[col].dtype)

                # make variables for Int, max and min
                IsInt = False
                mx = props[col].max()
                mn = props[col].min()

                # Integer does not support NA, therefore, NA needs to be filled
                if not np.isfinite(props[col]).all():
                    NAlist.append(col)
                    props[col].fillna(0, inplace=True)

                # test if column can be converted to an integer
                asint = props[col].fillna(0).astype(np.int64)
                result = (props[col] - asint)
                result = result.sum()
                if result > -0.01 and result < 0.01:
                    IsInt = True

                # Make Integer/unsigned Integer datatypes
                if IsInt:
                    if mn >= 0:
                        if mx < 255:
                            props[col] = props[col].astype(np.uint8)
                        elif mx < 65535:
                            props[col] = props[col].astype(np.uint16)
                        elif mx < 4294967295:
                            props[col] = props[col].astype(np.uint32)
                        else:
                            props[col] = props[col].astype(np.uint64)
                    else:
                        if mn > np.iinfo(np.int8).min and mx < np.iinfo(np.int8).max:
                            props[col] = props[col].astype(np.int8)
                        elif mn > np.iinfo(np.int16).min and mx < np.iinfo(np.int16).max:
                            props[col] = props[col].astype(np.int16)
                        elif mn > np.iinfo(np.int32).min and mx < np.iinfo(np.int32).max:
                            props[col] = props[col].astype(np.int32)
                        elif mn > np.iinfo(np.int64).min and mx < np.iinfo(np.int64).max:
                            props[col] = props[col].astype(np.int64)

                            # Make float datatypes 32 bit
                else:
                    props[col] = props[col].astype(np.float32)

                # Print new column type
                print("dtype after: ", props[col].dtype)
                print("******************************")
            # Categorize Object/string Columns if unique values is less than 50%
            else:
                num_unique = len(props[col].unique())
                num_total = len(props[col])
                if num_unique / num_total < 0.5:
                    props[col] = props[col].astype('category')
        # Print final result
        print("___MEMORY USAGE AFTER COMPLETION:___")
        mem_usg = props.memory_usage().sum() / 1024 ** 2
        print("Memory usage is: ", mem_usg, " MB")
        print("This is ", 100 * mem_usg / start_mem_usg, "% of the initial size")
        return props, NAlist
