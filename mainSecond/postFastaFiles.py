#!/usr/bin/env python3

import os
from dotenv import load_dotenv

import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

if __name__ == '__main__':

    load_dotenv()

    df = pd.read_excel('{}mainSecond/prophages.xlsx'.format(os.getenv('MAIN_PATH')), sheet_name = 'Sheet1')

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('prefs', {'download.prompt_for_download': False, 'download.directory_upgrade': True})
    bot = webdriver.Chrome(os.getenv('CHROMEDRIVER_PATH'), options = options)

    for ind in range(len(df)):

        accnum = df.at[ind, 'accessionNumbers']
        print('{}: {}'.format(ind, accnum))
        text = ''

        try:
            bot.get('https://pro-hunter.genomics.cn/index.php/Home/hunter/hunter.html')
            time.sleep(3)

            inp = bot.find_element_by_xpath('.//input[@id = "fileinput"]')
            inp.send_keys('C:{}mainSecond/fastafiles/{}.fasta'.format(os.getenv('MAIN_PATH'), accnum))
            time.sleep(0.5)

            inp = bot.find_element_by_xpath('.//input[@value = "user_expreience"]')
            inp.click()
            time.sleep(0.5)

            inp = bot.find_element_by_xpath('.//input[@value = "START HUNTING"]')
            inp.click()
            
            while True:
                try:
                    inp = bot.find_element_by_xpath('.//p/a[@id = "url"]')
                except:
                    continue
                finally:
                    break

            text = inp.get_attribute('href')
            print(text)
            
        except Exception as e:
            print(e)
            
        finally:
            df.at[ind, 'joblink'] = text
            writer = pd.ExcelWriter('{}mainSecond/prophages.xlsx'.format(os.getenv('MAIN_PATH')), engine = 'xlsxwriter') # pylint: disable=abstract-class-instantiated
            df.to_excel(writer, sheet_name = 'Sheet1', index = False)
            writer.save()
        
    time.sleep(4)
    bot.close()
    bot.quit()

    writer = pd.ExcelWriter('{}mainSecond/prophages.xlsx'.format(os.getenv('MAIN_PATH')), engine = 'xlsxwriter') # pylint: disable=abstract-class-instantiated
    df.to_excel(writer, sheet_name = 'Sheet1', index = False)
    writer.save()
