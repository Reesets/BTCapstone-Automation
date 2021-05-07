#!/usr/bin/env python3

import os
from dotenv import load_dotenv

import pandas as pd

if __name__ == '__main__':

    load_dotenv()

    df = pd.read_excel('{}main/prophages.xlsx'.format(os.getenv('MAIN_PATH')), sheet_name = 'Sheet1')
    datadf = pd.read_csv('{}prokaryotes.csv'.format(os.getenv('MAIN_PATH')), delimiter = ',')
    datadf = datadf[['#Organism Name', 'Organism Groups', 'Strain', 'BioSample', 'Size(Mb)', 'Replicons']]

    replicons = datadf['Replicons'].tolist()

    for i in range(len(df)):
        for ind, j in enumerate(replicons):
            try:
                if df.at[i, 'accessionNumbers'] in j:
                    df.at[i, 'size'] = datadf.at[ind, 'Size(Mb)']
                    df.at[i, 'strain'] = datadf.at[ind, 'Strain']
                    df.at[i, 'organismName'] = datadf.at[ind, 'Organism Name']
                    df.at[i, 'organismGroup'] = datadf.at[ind, 'Organism Groups']
                    df.at[i, 'biosample'] = datadf.at[ind, 'BioSample']
            except:
                pass

    for i in range(len(df)):
        for ind, j in enumerate(replicons):
            try:
                j = j.split(' ')
                for slot, k in enumerate(j):
                    if df.at[i, 'accessionNumbers'] in k:
                        print(k)
                        if 'plasmid' in j[slot - 1].lower():
                            df.at[i, 'type'] = 'plasmid'
                        elif k.split(':')[0].lower() == 'chromosome':
                            df.at[i, 'type'] = 'chromosome'
                        elif 'chromosome' in j[slot - 1].lower():
                            df.at[i, 'type'] = 'chromosome'
                        elif 'plasmid' in j[slot - 2].lower():
                            df.at[i, 'type'] = 'plasmid'
            except:
                pass
            finally:
                continue

    print(df)
    print(len(df[df['type'] == 'plasmid']), len(df[df['type'] == 'chromosome']))
    print(len(df), len(df.dropna()))

    writer = pd.ExcelWriter('{}main/prophages.xlsx'.format(os.getenv('MAIN_PATH')), engine = 'xlsxwriter') # pylint: disable=abstract-class-instantiated
    df.to_excel(writer, sheet_name = 'Sheet1', index = False)
    writer.save()
