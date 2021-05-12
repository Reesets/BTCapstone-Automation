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
            bot.get('https://www.ncbi.nlm.nih.gov/nuccore/{}?report=fasta'.format(df.at[ind, 'accessionNumbers']))
            time.sleep(2)
            try:
                inp = bot.find_element_by_xpath('.//a[@sourcecontent = "send_to_topmenu"]')
                inp.click()
            except:
                inp = bot.find_element_by_xpath('.//a[@sourcecontent = "send_to_menu"]')
                inp.click()
            finally:
                pass
            time.sleep(0.5)
            inp = bot.find_element_by_xpath('.//label[@for = "dest_File"]')
            inp.click()
            time.sleep(0.5)
            inp = bot.find_element_by_xpath('.//input[@id = "dest_File"]')
            inp.send_keys()
            time.sleep(0.5)
            inp = bot.find_element_by_xpath('.//select[@id = "file_format"]')
            inp.click()
            time.sleep(0.5)
            inp = bot.find_element_by_xpath('.//option[@value = "gff3"]')
            inp.click()
            time.sleep(0.5)
            inp = bot.find_element_by_xpath('.//div[@id = "submenu_File"]/button[@type = "submit"]')
            inp.click()
            time.sleep(0.5)
            l = os.listdir('/Users/ABHINAV/Downloads/')
            l = list(map(lambda x:x.split('.').pop().lower(), l))
            while 'gff3' not in l:
                l = os.listdir('/Users/ABHINAV/Downloads/')
                l = list(map(lambda x:x.split('.').pop(), l))
            time.sleep(3)
            os.rename('/Users/ABHINAV/Downloads/sequence.gff3', '{}mainSecond/gff3files/{}.gff3'.format(os.getenv('MAIN_PATH'), accnum))
            df.at[ind, 'gff3sequence'] = 'Stored Locally'
        except Exception as e:
            print(e)
            if os.path.exists('/Users/ABHINAV/Downloads/sequence.gff3') == True:
                os.remove('/Users/ABHINAV/Downloads/sequence.gff3')
            df.at[ind, 'gff3sequence'] = 'Error'
        finally:
            writer = pd.ExcelWriter('{}mainSecond/prophages2.xlsx'.format(os.getenv('MAIN_PATH')), engine = 'xlsxwriter') # pylint: disable=abstract-class-instantiated
            df.to_excel(writer, sheet_name = 'Sheet1', index = False)
            writer.save()
        
    time.sleep(4)
    bot.close()
    bot.quit()

    writer = pd.ExcelWriter('{}mainSecond/prophages.xlsx'.format(os.getenv('MAIN_PATH')), engine = 'xlsxwriter') # pylint: disable=abstract-class-instantiated
    df.to_excel(writer, sheet_name = 'Sheet1', index = False)
    writer.save()
