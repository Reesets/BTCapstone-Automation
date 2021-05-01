#!/usr/bin/env python3

import os
from dotenv import load_dotenv

import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

if __name__ == '__main__':

    load_dotenv()

    df = pd.read_excel('{}accessiondata.xlsx'.format(os.getenv('MAIN_PATH')), sheet_name = 'Sheet1')

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    bot = webdriver.Chrome(os.getenv('CHROMEDRIVER_PATH'), options = options)

    accnums = df['accession numbers'].tolist()

    failedL = []
    accnumbers = []
    fastaseq = []

    for ind, num in enumerate(accnums):
        
        print('{}: {}'.format(ind, num))
        text = ''

        try:
            bot.get('https://www.ncbi.nlm.nih.gov/nuccore/{}?report=fasta'.format(num))
            
            time.sleep(45)

            for j in bot.find_elements_by_xpath('.//pre'):
                if j.text != '':
                    text += j.text
        
        except:
            failedL.append(num)

        finally:
            accnumbers.append(num)
            fastaseq.append(text)
        
    time.sleep(4)
    bot.close()
    bot.quit()

    print('Fasta sequence could not be obtained for these: \n{}'.format(failedL))

    fastadf = pd.DataFrame({'accession numbers': accnumbers, 'fastaseqs': fastaseq})
    
    writer = pd.ExcelWriter('{}fastasequences.xlsx'.format(os.getenv('MAIN_PATH')), engine = 'xlsxwriter') # pylint: disable=abstract-class-instantiated
    fastadf.to_excel(writer, sheet_name = 'Sheet1', index = False)
    writer.save()

    df = pd.merge(df, fastadf, how = 'left', left_on = 'accession numbers', right_on = 'accession numbers')

    writer = pd.ExcelWriter('{}fastasequences.xlsx'.format(os.getenv('MAIN_PATH')), engine = 'xlsxwriter') # pylint: disable=abstract-class-instantiated
    df.to_excel(writer, sheet_name = 'Sheet1', index = False)
    writer.save()