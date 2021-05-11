#!/usr/bin/env python3

import os
from dotenv import load_dotenv

import pandas as pd

if __name__ == '__main__':
    
    load_dotenv()

    df = pd.read_excel('{}main/prophages.xlsx'.format(os.getenv('MAIN_PATH')))
    df = df[['accessionNumbers', 'links', 'size', 'strain', 'type']]
    
    writer = pd.ExcelWriter('{}mainSecond/prophages.xlsx'.format(os.getenv('MAIN_PATH')), engine = 'xlsxwriter') # pylint: disable=abstract-class-instantiated
    df.to_excel(writer, sheet_name = 'Sheet1', index = False)
    writer.save()
