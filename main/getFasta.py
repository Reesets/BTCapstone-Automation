#!/usr/bin/env python3

import os
from dotenv import load_dotenv

import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

if __name__ == '__main__':

    load_dotenv()

    df = pd.read_excel('{}fastasequences.xlsx'.format(os.getenv('MAIN_PATH')), sheet_name = 'Sheet1')

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    bot = webdriver.Chrome(os.getenv('CHROMEDRIVER_PATH'), options = options)

    for ind in range(len(df)):
        if df.at[ind, 'fastaseqs'] == '0':
            print('{}: {}'.format(ind, df.at[ind, 'accession numbers']))
            text = ''

            try:
                bot.get('https://www.ncbi.nlm.nih.gov/nuccore/{}?report=fasta'.format(df.at[ind, 'accession numbers']))
                
                if df.at[ind, 'size'] > 3.5:
                    time.sleep(30)
                else:
                    time.sleep(10)

                for j in bot.find_elements_by_xpath('.//pre'):
                    if j.text != '':
                        text += j.text
            
            except KeyboardInterrupt:
                break

            except:
                pass

            finally:
                df.at[ind, 'fastaseqs'] = text
        
    time.sleep(4)
    bot.close()
    bot.quit()
    
    writer = pd.ExcelWriter('{}fastasequences2.xlsx'.format(os.getenv('MAIN_PATH')), engine = 'xlsxwriter') # pylint: disable=abstract-class-instantiated
    df.to_excel(writer, sheet_name = 'Sheet1', index = False)
    writer.save()
