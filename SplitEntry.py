class Split_Entry:
    def split(entry):
        def remove_dups(xlist):
            xlist = list(dict.fromkeys(xlist))
            if '' in split_l:
                xlist.remove('')
            if len(xlist) == 1:
                xlist = xlist[0]
            return xlist
        entry = entry
        if len(entry.split('\t')) > 1 and len(entry.split('\n')) > 1:
            t_split_l = entry.split('\t')
            split_l = []
            for t_split in t_split_l:
                n_split_l = t_split.split('\n')
                for n_split in n_split_l:
                    split_l.append(n_split.strip())
            split_l = remove_dups(split_l)
            return split_l
        elif len(entry.split('\t')) > 1:
            t_split_l = entry.split('\t')
            split_l = []
            for t_split in t_split_l:
                split_l.append(t_split.strip())
            split_l = remove_dups(split_l)
            return split_l
        elif len(entry.split('\n')) > 1:
            n_split_l = entry.split('\n')
            split_l = []
            for n_split in n_split_l:
                split_l.append(n_split.strip())
            split_l = remove_dups(split_l)
            return split_l
        else:
            return entry.strip()
