#!/usr/bin/env python3

import os
from dotenv import load_dotenv

import time

import pickle
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

if __name__ == '__main__':

    load_dotenv()

    l = pickle.load(open('{}main/linklist.txt'.format(os.getenv('MAIN_PATH')), 'rb'))
    nums = list(map(lambda x:x.split('/')[len(x.split('/')) - 1], l))

    df = pd.DataFrame({'accessionNumbers': nums, 'links': l})

    writer = pd.ExcelWriter('{}main/prophages.xlsx'.format(os.getenv('MAIN_PATH')), engine = 'xlsxwriter') # pylint: disable=abstract-class-instantiated
    df.to_excel(writer, sheet_name = 'Sheet1', index = False)
    writer.save()

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    bot = webdriver.Chrome(os.getenv('CHROMEDRIVER_PATH'), options = options)

    for ind, num in enumerate(df['accessionNumbers'].tolist()):
        print(df.at[ind, 'accessionNumbers'])
        job = ''
        newuri = ''
        try:
            bot.get('https://phaster.ca/')
            time.sleep(5)
            
            inp = bot.find_element_by_xpath('.//a[@href = "#number-in"]')
            inp.click()
            time.sleep(1)
            inp = bot.find_element_by_xpath('.//input[@placeholder = "Accession"]')
            inp.send_keys(df.at[ind, 'accessionNumbers'])
            inp.send_keys(Keys.RETURN)
            time.sleep(7)
            
            newuri = bot.current_url
            l = newuri.split('/')
            job = l[4]
        except Exception as e:
            print(e)
        finally:
            df.at[ind, 'jobforaccnum'] = job
            df.at[ind, 'joblinkforaccnum'] = newuri

    time.sleep(4)
    bot.close()
    bot.quit()

    writer = pd.ExcelWriter('{}main/prophages.xlsx'.format(os.getenv('MAIN_PATH')), engine = 'xlsxwriter') # pylint: disable=abstract-class-instantiated
    df.to_excel(writer, sheet_name = 'Sheet1', index = False)
    writer.save()
