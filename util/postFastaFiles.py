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
    bot = webdriver.Chrome('{}chromedriver.exe'.format(os.getenv('CHROMEDRIVER_PATH')), options = options)

    df = pd.read_excel('{}fastasequences.xlsx'.format(os.getenv('MAIN_PATH')), sheet_name = 'Sheet1')
    
    acc = []
    jobids = []
    joblinks = []
    for ind, seq in enumerate(df['fastaseqs'].tolist()):

        if df.at[ind, 'status'] != 'Done':

            job = ''
            newuri = ''
            accnum = df.at[ind, 'accession numbers']
            try:
                bot.get('https://phaster.ca/')
                time.sleep(10)
                
                inp = bot.find_element_by_xpath('.//input[@id = "submission_sequence"]')
                inp.send_keys('C:{}textFiles/{}.fna'.format(os.getenv('MAIN_PATH'), accnum))
                inp = bot.find_element_by_xpath('.//button[@id = "file-submit"]')
                inp.click()
                time.sleep(5)
                
                newuri = bot.current_url
                l = newuri.split('/')
                job = l[len(l) - 2]
            except:
                pass
            finally:
                acc.append(accnum)
                jobids.append(job)
                joblinks.append(newuri)
                writer = pd.ExcelWriter('{}runfastajob1.xlsx'.format(os.getenv('MAIN_PATH')), engine = 'xlsxwriter') # pylint: disable=abstract-class-instantiated
                pd.DataFrame({'accession numbers': acc, 'jobID': jobids, 'links': joblinks}).to_excel(writer, sheet_name = 'Sheet1', index = False)
                writer.save()
                
    time.sleep(4)
    bot.close()
    bot.quit()

    writer = pd.ExcelWriter('{}runfastajob1.xlsx'.format(os.getenv('MAIN_PATH')), engine = 'xlsxwriter') # pylint: disable=abstract-class-instantiated
    pd.DataFrame({'accession numbers': acc, 'jobID': jobids, 'links': joblinks}).to_excel(writer, sheet_name = 'Sheet1', index = False)
    writer.save()