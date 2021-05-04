#!/usr/bin/env python3

import os
from dotenv import load_dotenv

import time
import requests

import pickle
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

if __name__ == '__main__':
    
    load_dotenv()

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    bot = webdriver.Chrome(os.getenv('CHROMEDRIVER_PATH'), options = options)

    df = pd.read_excel('{}main/prophages.xlsx'.format(os.getenv('MAIN_PATH')), sheet_name = 'Sheet1')
    
    for ind in range(len(df)):

        accnum = df.at[ind, 'accession numbers']
        print('{}: {}'.format(ind, accnum))

        try:
            bot.get('https://phaster.ca/')
            time.sleep(5)
            inp = bot.find_element_by_xpath('.//input[@id = "submission_sequence"]')
            inp.send_keys('C:{}main/fastafiles/{}.fna'.format(os.getenv('MAIN_PATH'), accnum))
            inp = bot.find_element_by_xpath('.//button[@id = "file-submit"]')
            inp.click()
            time.sleep(6)
            newuri = bot.current_url
            l = newuri.split('/')
            job = l[4]
        except:
            pass
        finally:
            df.at[ind, 'jobforfasta'] = job
            df.at[ind, 'joblinkforfasta'] = newuri
            writer = pd.ExcelWriter('{}main/prophages.xlsx'.format(os.getenv('MAIN_PATH')), engine = 'xlsxwriter') # pylint: disable=abstract-class-instantiated
            df.to_excel(writer, sheet_name = 'Sheet1', index = False)
            writer.save()
                
    time.sleep(4)
    bot.close()
    bot.quit()

    writer = pd.ExcelWriter('{}main/prophages.xlsx'.format(os.getenv('MAIN_PATH')), engine = 'xlsxwriter') # pylint: disable=abstract-class-instantiated
    df.to_excel(writer, sheet_name = 'Sheet1', index = False)
    writer.save()
