#!/usr/bin/env python3

import os
from dotenv import load_dotenv

import requests

import pickle
import pandas as pd

if __name__ == '__main__':
    
    load_dotenv()

    df = pd.read_excel('{}fastasequences.xlsx'.format(os.getenv('MAIN_PATH')), sheet_name = 'Sheet1')

    sequences = ''

    for ind, seq in enumerate(df['fastaseqs'].tolist()):
        
        if df.at[ind, 'status'] != 'Done':
            sequences += seq + '\n'
            f = open('textFiles/{}.fna'.format(df.at[ind, 'accession numbers']), 'w+')
            f.write(seq)
            f.close()

    sequences = sequences.strip()
    f = open('fastaseqs.fna', 'w+')
    f.write(sequences)
    f.close()