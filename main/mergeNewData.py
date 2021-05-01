#!/usr/bin/env python3

import os
from dotenv import load_dotenv

import time

import pickle
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

if __name__ == '__main__':

    load_dotenv()

    df = pd.read_excel('{}fastasequences.xlsx'.format(os.getenv('MAIN_PATH')), sheet_name = 'Sheet1')

    df['accession numbers'] = df['accession numbers'].map(lambda x:x.replace('NZ_', ''))
    l = pickle.load(open('{}linklist.txt'.format(os.getenv('MAIN_PATH')), 'rb'))
    l = [i for i in l if 'NC_' not in i]
    linkDF = pd.DataFrame({'links': l, 'accession numbers': list(map(lambda x:x.split('/')[4], l))})
    df = pd.merge(linkDF, df, how = 'left', left_on = 'accession numbers', right_on = 'accession numbers')
    df = df.fillna('0')

    for ind in range(len(df)):
        
        if df.at[ind, 'links_y'] == '0':
            df.at[ind, 'links'] = df.at[ind, 'links_x'].strip().replace(' ', '')
        else:
            df.at[ind, 'links'] = df.at[ind, 'links_y'].strip().replace(' ', '')

    df = df.drop(['links_x', 'links_y'], axis = 1)
    
    tempDF = pd.read_csv('{}prokaryotes.csv'.format(os.getenv('MAIN_PATH')), delimiter = ',')
    tempDF = tempDF[['Strain', 'Size(Mb)', 'Replicons']]
    replicons = tempDF['Replicons'].tolist()

    for i in range(len(df)):
        if df.at[i, 'strain'] == '0':
            for ind, j in enumerate(replicons):
                try:
                    if df.at[i, 'accession numbers'] in j:
                        df.at[i, 'size'] = tempDF.at[ind, 'Size(Mb)']
                        df.at[i, 'strain'] = tempDF.at[ind, 'Strain']
                except:
                    pass

    for i in range(len(df)):
        print(df.at[i, 'accession numbers'])
        for ind, j in enumerate(replicons):
            try:
                j = j.split(' ')
                for slot, k in enumerate(j):
                    if df.at[i, 'accession numbers'] in k:
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
    df = df.sort_values('status').reset_index(drop = True)
    print(df)
    print(len(df[df['status'] == '0']))
    print(len(df[df['type'] == 'plasmid']), len(df[df['type'] == 'chromosome']))
    print(len(df), len(df.dropna()))

    writer = pd.ExcelWriter('{}fastasequences.xlsx'.format(os.getenv('MAIN_PATH')), engine = 'xlsxwriter') # pylint: disable=abstract-class-instantiated
    df.to_excel(writer, sheet_name = 'Sheet1', index = False)
    writer.save()
    