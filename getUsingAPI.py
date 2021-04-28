#!/usr/bin/env python3

import os
from dotenv import load_dotenv

import requests

import pandas as pd

if __name__ == '__main__':
    
    load_dotenv()

    df = pd.read_excel('{}fastasequences.xlsx'.format(os.getenv('MAIN_PATH')), sheet_name = 'Sheet1')
    df['status'] = df['total'].map(lambda x:'Done' if x>0 else 'Pending')
    df['statusmsg'] = df['total'].map(lambda x:'Done and {} phages Found'.format(x) if x>0 else 'Pending')

    failedL = []

    for ind, seq in enumerate(df['accession numbers'].tolist()):
        
        if df.at[ind, 'total'] == 0:

            try:
                f = requests.get('http://phaster.ca/phaster_api?acc={}'.format(seq))
                j = f.json()
                msg = j['status'].lower()

                print('{}: {}'.format(seq, msg))
                
                if msg == 'complete':
                    df.at[ind, 'status'] = 'Done'
                    df.at[ind, 'statusmsg'] = 'Done and 0 phages found'
                else:
                    df.at[ind, 'status'] = 'Pending'
                    df.at[ind, 'statusmsg'] = msg
            except:
                failedL.append(seq)
                df.at[ind, 'status'] = 'Error'
                df.at[ind, 'statusmsg'] = 'An error occured'
            finally:
                pass

    writer = pd.ExcelWriter('{}fastasequences.xlsx'.format(os.getenv('MAIN_PATH')), engine = 'xlsxwriter') # pylint: disable=abstract-class-instantiated
    df.to_excel(writer, sheet_name = 'Sheet1', index = False)
    writer.save()