class Split_Entry:
    def split(entry):
        entry = entry
        if len(entry.split('\t')) > 1 and len(entry.split('\n')) > 1:
            t_split_l = entry.split('\t')
            split_l = []
            for t_split in t_split_l:
                n_split_l = t_split.split('\n')
                for n_split in n_split_l:
                    split_l.append(n_split.strip())
            return split_l
        else:
            return entry.strip()
