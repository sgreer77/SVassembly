#"alignment_test.txt"
def interesting_contigs_mappy(infile, outfile):
    import pandas as pd
    import ast 

    df = pd.read_table(infile, sep="\t", index_col = 0)
    df = df.reset_index() #otherwise 'read' column is index
    grouped = df.groupby('read').filter(lambda x: len(x)>=2) #only reads that appear 2+ times
    grouped = grouped.groupby('read')

    df = pd.read_table(infile, sep="\t", index_col = 0)
    df['interesting'] = False 
    
    for name, group in grouped:
        r_st_list = []
        r_en_list = []
        i = 0
        
        for row in group.iterrows(): 
            if abs(row[1]['r_en'] - row[1]['r_st']) > 500: 
                r_st_list.append(row[1]['r_st'])
                r_en_list.append(row[1]['r_st'])
                i += 1
        
        if i == 2: #should generally have 2 rows
            if r_st_list[1] > r_en_list[0] or r_st_list[0] > r_en_list[1]: #interesting
                df.loc[name, 'interesting'] = True

    dfInteresting = df.query('interesting == True')
    dfInteresting.to_csv(outfile)
        
