#!/usr/bin/env python3

import os
from dotenv import load_dotenv

import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

if __name__ == '__main__':

    load_dotenv()

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    bot = webdriver.Chrome('{}chromedriver.exe'.format(os.getenv('CHROMEDRIVER_PATH')), options = options)

    df = pd.read_excel('{}runfastajob.xlsx'.format(os.getenv('MAIN_PATH')), sheet_name = 'Sheet1')
    links = df['links'].tolist()

    linksDone = []
    failedL = []

    for ind, link in enumerate(links):
        num = df.at[ind, 'accession numbers']
        if link != '':
            try:
                bot.get(link)
                time.sleep(3)
                l = bot.find_elements_by_tag_name('p')
                l = list(map(lambda x:x.text, l))
                if 'No phage were found in this sequence!' in l:
                    print(num)
                    linksDone.append(num)
            except:
                pass
            finally:
                failedL.append(num)
        elif link == '':
            linksDone.append(num)

    time.sleep(2)
    bot.close()
    bot.quit()

    df = pd.read_excel('{}fastasequences.xlsx'.format(os.getenv('MAIN_PATH')), sheet_name = 'Sheet1')

    for ind, num in enumerate(df['accession numbers'].tolist()):
        if num in linksDone:
            df.at[ind, 'status'] = 'Done'
            df.at[ind, 'statusmsg'] = 'Done and 0 phages found'

    writer = pd.ExcelWriter('{}fastasequences.xlsx'.format(os.getenv('MAIN_PATH')), engine = 'xlsxwriter') # pylint: disable=abstract-class-instantiated
    df.to_excel(writer, sheet_name = 'Sheet1', index = False)
    writer.save()

    print(failedL)
