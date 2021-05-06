#!/usr/bin/env python3

import sys
import os
from dotenv import load_dotenv

import traceback
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pickle
import pandas as pd

if __name__ == '__main__':

    load_dotenv()

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    bot = webdriver.Chrome(os.getenv('CHROMEDRIVER_PATH'), options = options)

    df = pd.read_excel('{}main/prophages.xlsx'.format(os.getenv('MAIN_PATH')), sheet_name = 'Sheet1')

    totalpro = 0
    
    for ind in range(len(df)):
        
        print('{}: {}'.format(ind, df.at[ind, 'accessionNumbers']))
        link = df.at[ind, 'joblinkforfasta']
        dnas = []
        a = []
        b = []
        c = []

        try:
            bot.get(link)
            time.sleep(6)
            l = bot.find_elements_by_tag_name('p')
            l = list(map(lambda x:x.text, l))
            headl = bot.find_elements_by_tag_name('h5')
            headl = list(map(lambda x:x.text, headl))
            if 'No phage were found in this sequence!' in l:
                df.at[ind, 'statusbyfasta'] = 'Done and no phages in sequence!!'
            elif 'Your submission is processing!' in headl:
                df.at[ind, 'statusbyfasta'] = 'Pending!!'
            else:
                df.at[ind, 'statusbyfasta'] = 'Done and phages found!!'
                a = bot.find_elements_by_xpath('.//tr[@class="intact"]')
                b = bot.find_elements_by_xpath('.//tr[@class="questionable"]')
                c = bot.find_elements_by_xpath('.//tr[@class="incomplete"]')
                
                dnatext = bot.find_elements_by_xpath('.//tr[@class = "intact"]/td/a[@class = "modal-trigger"]')

                if len(dnatext) == 0:
                    raise ValueError

                for i in dnatext:
                    if 'sequence' not in i.get_attribute('href') and 'dna' in i.get_attribute('href'):
                        dnaID = i.get_attribute('href').split('#')[1]
                        i.click()
                        for j in bot.find_elements_by_xpath('.//pre'):
                            if j.text != '':
                                dnas.append(j.text)
                        bot.find_elements_by_xpath('.//div[@id = "' + dnaID + '"]/div[@class = "modal-footer"]/a[contains(text(),"Close")]')[0].click()

        except ValueError:
            pass

        except:
            pass

        finally:
            tot = len(a) + len(b) + len(c)
            print('Total prophages found in this sequence is {}'.format(tot))
            totalpro += tot
            print('Total prophages found is {}'.format(totalpro))
            df.at[ind, 'intactbyfasta'] = len(a)
            df.at[ind, 'questionablebyfasta'] = len(b)
            df.at[ind, 'incompletebyfasta'] = len(c)
            df.at[ind, 'totalbyfasta'] = tot

            if len(dnas) > 0:
                text = ''
                for seq in dnas:
                    text += seq + '\n'
                f = open('{}main/intactphagesfasta/{}.fna'.format(os.getenv('MAIN_PATH'), df.at[ind, 'accessionNumbers']), 'w+')
                f.write(text)
                f.close()

            df.at[ind, 'numbersequencesbyfasta'] = len(dnas)
            if len(dnas) > 0:
                df.at[ind, 'statussequencesbyfasta'] = 'Stored locally!!'
            else:
                df.at[ind, 'statussequencesbyfasta'] = 'No intact phages!!'

            writer = pd.ExcelWriter('{}main/prophages.xlsx'.format(os.getenv('MAIN_PATH')), engine = 'xlsxwriter') # pylint: disable=abstract-class-instantiated
            df.to_excel(writer, sheet_name = 'Sheet1', index = False)
            writer.save()

    time.sleep(4)
    bot.close()
    bot.quit()

    writer = pd.ExcelWriter('{}main/prophages.xlsx'.format(os.getenv('MAIN_PATH')), engine = 'xlsxwriter') # pylint: disable=abstract-class-instantiated
    df.to_excel(writer, sheet_name = 'Sheet1', index = False)
    writer.save()
    