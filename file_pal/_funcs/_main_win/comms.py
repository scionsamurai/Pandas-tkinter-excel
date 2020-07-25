class Comm:
    def clear_values(thread_busyx,entsx, ENDx):
        if not thread_busyx:
            entsx[0][1].delete(0, ENDx)
            entsx[1][1].delete(0, ENDx)

    def fetch(pandas_obj, pdx):
        """
        Print first Files Memory Usage and file list.
        :param pandas_obj: Input DataFrame.
        """
        if isinstance(pandas_obj, pdx.DataFrame):
            usage_b = pandas_obj.memory_usage(deep=True).sum()
        else:
            usage_b = pandas_obj.memory_usage(deep=True)
        usage_mb = usage_b / 1024 ** 2 # convert bytes to megabytes
        print("{:03.2f} MB".format(usage_mb))
        print(pandas_obj.info(verbose=True))
        print('----header_W/filler_value : filler_value----')
        print(answer)

    def open_brows(web_b, func=1):
        if func == 1:
            web_b.open_new(r"https://github.com/scionsamurai/Pandas-tkinter-excel/blob/Test/README.md")
        else:
            web_b.open_new(r"https://github.com/scionsamurai/Pandas-tkinter-excel/blob/Test/LICENSE")
