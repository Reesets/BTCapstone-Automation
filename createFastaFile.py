#!/usr/bin/env python3

import os
from dotenv import load_dotenv

import requests

import pickle
import pandas as pd

if __name__ == '__main__':
    
    load_dotenv()

    df = pd.read_excel('{}fastasequences.xlsx'.format(os.getenv('MAIN_PATH')), sheet_name = 'Sheet1')
    df = df[df['status'] != 'Done']

    sequences = ''

    for seq in df['fastaseqs'].tolist():
        
        sequences += seq + '\n'

    sequences = sequences.strip()
    pickle.dump(sequences, open('fastaseqs.fna', 'wb'))