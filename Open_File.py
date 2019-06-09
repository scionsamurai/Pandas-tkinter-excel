import pandas as pd
import numpy as np
import time
from RetrieveInput import Retrieve_Input
class OpenFile:
    def __init__(self):
        self.var = ''
    def open_file(self, entry, inp_options, ):
        gen_rules = inp_options[0]
        delimiter = gen_rules['Delimiter']
        terminator = gen_rules['Terminator']
        header_line = gen_rules['Header Line']
        index_col = gen_rules['Index Column']
        chunk = gen_rules['Chunk']
        verbose = gen_rules['Verbose']
        header_func = gen_rules['Header Func']
        skip_rows = None
        skip_cols = 0
        name = None
        self.var = verbose

        only_cols = inp_options[1]
        dtypes = inp_options[2]
        head_func_dtypes = inp_options[3]
        if len(inp_options) > 5:
            search_col = inp_options[4]
            real_l = inp_options[5]
            filter_results = True
            inp = Retrieve_Input()
        else:
            filter_results = False
        temp_field = entry.split('/')
        new_field = temp_field[(len(temp_field) - 1)]
        print('Opening ' + new_field)
        start = time.time()

        if entry[-4:] == '.csv':
            if delimiter != None:
                df = pd.read_csv(entry, sep=delimiter, nrows=50, low_memory=False)
                if header_func:
                    skip_rows, skip_cols, name = self.col_check(df,head_func_dtypes)
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
                        if name != None:
                            header_line = 0
                        data = pd.read_csv(entry, sep=delimiter, header=header_line, index_col=index_col,
                                           usecols=new_only_cols, dtype=new_dtypes, verbose=verbose,
                                           lineterminator=terminator, low_memory=False)
                        data.columns = [col.strip() for col in data.columns]
                        if filter_results:
                            data = inp.result_frames(data,search_col, real_l,entry)
                        if not data.empty:
                            data = self.reduce_mem_usage(data)[0]
                        else:
                            print('no results in x')
                        return ((data), (entry))
                    except ValueError as e:
                        print(e)
                else:
                    try:
                        if name != None:
                            header_line = 0
                        data = pd.read_csv(entry, sep=delimiter, header=header_line, names=name, index_col=index_col,
                                           dtype=new_dtypes, skiprows=skip_rows, verbose=verbose,
                                           lineterminator=terminator, low_memory=False)
                        if skip_cols > 0:
                            for i in range(skip_cols):
                                data.drop(data.columns[1],axis=1)
                        data.columns = [col.strip() for col in data.columns]
                        if filter_results:
                            data = inp.result_frames(data,search_col, real_l,entry)
                        #print(data)
                        if not data.empty:
                            data = self.reduce_mem_usage(data)[0]
                        else:
                            print('no results in x')

                        end = time.time()
                        print('-------' + str(end - start) + '-------')
                        return ((data), (entry))

                    except ValueError as e:
                        print(e)

            else:
                df = pd.read_csv(entry, nrows=50, low_memory=False)
                if header_func:
                    skip_rows, skip_cols, name = self.col_check(df,head_func_dtypes)
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
                        if name != None:
                            header_line = 0
                        data = pd.read_csv(entry, header=header_line, chunksize=chunk, index_col=index_col,
                                           usecols=new_only_cols, dtype=new_dtypes, verbose=verbose,
                                           lineterminator=terminator, low_memory=False)
                        if skip_cols > 0:
                            for i in range(skip_cols):
                                data.drop(data.columns[1],axis=1)
                        data.columns = [col.strip() for col in data.columns]
                        if filter_results:
                            data = inp.result_frames(data,search_col, real_l,entry)
                        if not data.empty:
                            data = self.reduce_mem_usage(data)[0]
                        else:
                            print('no results in x')
                        return ((data), (entry))
                    except ValueError as e:
                        print(e)
                else:
                    try:
                        if name != None:
                            header_line = 0
                        data = pd.read_csv(entry, header=header_line, names=name, chunksize=chunk, index_col=index_col,
                                           dtype=new_dtypes, skiprows=skip_rows, verbose=verbose,
                                           lineterminator=terminator, low_memory=False)
                        if skip_cols > 0:
                            for i in range(skip_cols):
                                data.drop(data.columns[1],axis=1)
                        data.columns = [col.strip() for col in data.columns]
                        if filter_results:
                            data = inp.result_frames(data,search_col, real_l,entry)
                        if not data.empty:
                            data = self.reduce_mem_usage(data)[0]
                        else:
                            print('no results in x')
                        return ((data), (entry))
                    except ValueError as e:
                        print(e)
        elif (entry[-4:] == 'xlsx') or (entry[-4:] == '.xls') or ((entry[-4:])[:3] == 'xls'):
            df = pd.read_excel(entry, sheet_name=0, nrows=50)
            if header_func:
                skip_rows, skip_cols, name = self.col_check(df, head_func_dtypes)
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

            if name != None:
                header_line = 0
            data = pd.read_excel(entry, sheet_name=0, header=header_line, names=name, index_col=index_col,
                                 usecols=new_only_cols, dtype=new_dtypes, skiprows=skip_rows, verbose=verbose)
            if skip_cols > 0:
                for i in range(skip_cols):
                    data = data.drop(data.columns[0], axis=1)
            try:
                data.columns = [col.strip() for col in data.columns]
            except AttributeError: #'int'object has no attribute 'strip'  < - files with int headers
                pass
            if filter_results:
                data = inp.result_frames(data, search_col, real_l, entry)
            if not data.empty:
                data = self.reduce_mem_usage(data)[0]
            else:
                print('no results in x')
            end = time.time()
            print('-------'+ str(end-start) +'-------')
            return ((data), (entry))
        elif entry[-3:] == '.h5':
            data = pd.read_hdf(entry,'df')
            if filter_results:
                data = inp.result_frames(data, search_col, real_l, entry)
            if not data.empty:
                data = self.reduce_mem_usage(data)[0]
            else:
                print('no results in x')
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
        self.verb_print(("Memory usage of properties dataframe is :", start_mem_usg, " MB"))
        NAlist = []  # Keeps track of columns that have missing values filled in.
        for col in props.columns:
            if props[col].dtype != object and props[col].dtype != 'datetime64[ns]':  # Exclude strings and dates

                # Print current column type
                self.verb_print("******************************")
                self.verb_print(("Column: ", col))
                self.verb_print(("dtype before: ", props[col].dtype))

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
                self.verb_print(("dtype after: ", props[col].dtype))
                self.verb_print("******************************")
            # Categorize Object/string Columns if unique values is less than 50%
            else:
                # Print current column type
                self.verb_print("******************************")
                self.verb_print(("Column: ", col))
                self.verb_print(("dtype before: ", props[col].dtype))
                num_unique = len(props[col].unique())
                num_total = len(props[col])
                if num_unique / num_total < 0.5:
                    props[col] = props[col].astype('category')
                # Print new column type
                self.verb_print(("dtype after: ", props[col].dtype))
                self.verb_print("******************************")
        # Print final result
        self.verb_print("___MEMORY USAGE AFTER SHRINK:___")
        mem_usg = props.memory_usage().sum() / 1024 ** 2
        self.verb_print(("Memory usage is: ", mem_usg, " MB"))
        self.verb_print(("This is ", 100 * mem_usg / start_mem_usg, "% of the initial size"))
        return props, NAlist

    def verb_print(self,text):
        if self.var:
            print(text)

    def col_check(self, frame_slice, func_dict):
        slice_dict = {}
        slice_key_list = []
        dict_key_list = []
        for col in frame_slice.columns.values:
            try:
                slice_dict[col.strip()] = frame_slice[col].dtype
            except AttributeError:
                slice_dict[col] = frame_slice[col].dtype
            slice_key_list.append(col)
        for key in func_dict:
            dict_key_list.append(key)
        first_header = dict_key_list[0]
        if first_header == slice_key_list[0]:            #first col header matches
            pass
            #print('first col header matches')
            #for col in slice_dict:
            #    if col in func_dict:
            #        print(col + ' is in func dict')
        else:                                           #first col header doesn't match
            print('first col header doesn\'t match')
            #for col in frame_slice.columns.values:
            #    in_col = frame_slice[col].str.contains(first_header)
            #    print(col + ' : ' + in_col)
            current_col = (-1)
            found_col = []
            list1 = frame_slice[frame_slice.isin([first_header])].dropna(how='all').count()
            for i in list1: #finding what column has the first func_dict header
                current_col += 1
                if i > 0:
                    found_col.append(current_col)
            if len(found_col) > 0: #if one of the columns has the first func_dict header
                found_col_series = frame_slice.iloc[:, found_col[0]] #list of values from row that has first f_d header
                series_count = 0
                found_row = 0
                for i in found_col_series: #finding what row has the func_dict header
                    series_count += 1
                    if i == first_header:
                        found_row = series_count
                        break
                return found_row, found_col[0], None
            else:
                name = []
                if len(slice_dict) == len(func_dict):
                    for key,val in func_dict.items():
                        name.append(key)

                return None, 0, name
