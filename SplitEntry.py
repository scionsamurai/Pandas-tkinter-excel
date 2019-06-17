class Split_Entry:
    def split(entry):
        def remove_dups(xlist):
            xlist = list(dict.fromkeys(xlist))
            if '' in split_l:
                xlist.remove('')
            if len(xlist) == 1:
                xlist = xlist[0]
            return xlist
        def strip_list(nlist):
            n_list = []
            for n in nlist:
                n_list.append(n.strip())
            return n_list
        entry = entry
        if len(entry.split('\t')) > 1 and len(entry.split('\n')) > 1:
            t_split_l = entry.split('\t')
            split_l = []
            for t_split in t_split_l:
                n_split_l = t_split.split('\n')
                split_l.extend(strip_list(n_split_l))
            split_l = remove_dups(split_l)
            return split_l
        elif len(entry.split('\t')) > 1:
            t_split_l = entry.split('\t')
            split_l = strip_list(t_split_l)
            split_l = remove_dups(split_l)
            return split_l
        elif len(entry.split('\n')) > 1:
            n_split_l = entry.split('\n')
            split_l = strip_list(n_split_l)
            split_l = remove_dups(split_l)
            return split_l
        else:
            return entry.strip()

