#!/usr/bin/env python3

import os
from dotenv import load_dotenv

import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

if __name__ == '__main__':

    load_dotenv()

    df = pd.read_excel('{}main/prophages.xlsx'.format(os.getenv('MAIN_PATH')), sheet_name = 'Sheet1')

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    bot = webdriver.Chrome(os.getenv('CHROMEDRIVER_PATH'), options = options)

    for ind in range(len(df)):
        
        print('{}: {}'.format(ind, df.at[ind, 'accessionNumbers']))
        text = ''

        try:
            bot.get('https://www.ncbi.nlm.nih.gov/nuccore/{}?report=fasta'.format(df.at[ind, 'accessionNumbers']))
            time.sleep(45)
            for j in bot.find_elements_by_xpath('.//pre'):
                if j.text != '':
                    text += j.text
        
        except:
            pass

        finally:
            f = open('{}main/fastafiles/{}.fna'.format(os.getenv('MAIN_PATH'), df.at[ind, 'accessionNumbers']), 'w+')
            f.write(text)
            f.close()
            df.at[ind, 'fastaSequence'] = 'Stored Locally'
            writer = pd.ExcelWriter('{}main/prophages.xlsx'.format(os.getenv('MAIN_PATH')), engine = 'xlsxwriter') # pylint: disable=abstract-class-instantiated
            df.to_excel(writer, sheet_name = 'Sheet1', index = False)
            writer.save()
        
    time.sleep(4)
    bot.close()
    bot.quit()
    
    writer = pd.ExcelWriter('{}main/prophages.xlsx'.format(os.getenv('MAIN_PATH')), engine = 'xlsxwriter') # pylint: disable=abstract-class-instantiated
    df.to_excel(writer, sheet_name = 'Sheet1', index = False)
    writer.save()
