#!/usr/bin/env python3

import os
from dotenv import load_dotenv

import pandas as pd

if __name__ == '__main__':

    load_dotenv()

    df = pd.read_csv('{}prokaryotes.csv'.format(os.getenv('MAIN_PATH')), delimiter = ',')
    df = df[['Strain', 'Size(Mb)', 'Replicons']]
    replicons = df['Replicons'].tolist()

    accdf = pd.read_excel('{}accessionnumbers.xlsx'.format(os.getenv('MAIN_PATH')), sheet_name = 'Sheet1')
    accDF = accdf['accession numbers'].tolist()
    
    strain = []
    accnum = []
    sizemb = []
    for i in accDF:
        for ind, j in enumerate(replicons):
            try:
                if i in j:
                    accnum.append(i)
                    sizemb.append(df.at[ind, 'Size(Mb)'])
                    strain.append(df.at[ind, 'Strain'])
                    print(i)
                    print(df.at[ind, 'Replicons'])
            except:
                pass

    df = pd.DataFrame({'accession numbers': accnum, 'strain': strain, 'size': sizemb})
    df = pd.merge(accdf, df, how = 'left', left_on = 'accession numbers', right_on = 'accession numbers')
    print(df)
    print(df.columns.tolist())

    writer = pd.ExcelWriter('{}accessiondata.xlsx'.format(os.getenv('MAIN_PATH')), engine = 'xlsxwriter') # pylint: disable=abstract-class-instantiated
    df.to_excel(writer, sheet_name = 'Sheet1', index = False)
    writer.save()
    