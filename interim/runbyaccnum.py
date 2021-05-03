#!/usr/bin/env python3

import os
from dotenv import load_dotenv

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

    df = pd.read_excel('{}main/runfastajobacc.xlsx'.format(os.getenv('MAIN_PATH')), sheet_name = 'Sheet1')

    accnum = []
    intact = []
    question = []
    incomplete = []
    total = []
    sequences = []
    links = []

    totalpro = 0
    
    k = 0

    for ind, link in enumerate(df['links'].tolist()):
        
        print('{}: {}'.format(ind, df.at[ind, 'accession numbers']))
        dnas = []
        a = []
        b = []
        c = []

        try:
            bot.get(link)
            time.sleep(6)

            l = bot.find_elements_by_tag_name('p')
            l = list(map(lambda x:x.text, l))
            if 'No phage were found in this sequence!' in l:
                pass
            else:
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

        except:
            pass

        finally:
            accnum.append(df.at[ind, 'accession numbers'])
            links.append(link)
            intact.append(len(a))
            question.append(len(b))
            incomplete.append(len(c))
            tot = len(a) + len(b) + len(c)
            print('Total prophages found in this sequence is {}'.format(tot))
            totalpro += tot
            print('Total prophages found is {}'.format(totalpro))
            total.append(tot)
            sequences.append(dnas)
            d = {'accession numbers': accnum,
                 'intact': intact,
                 'questionable': question,
                 'incomplete': incomplete,
                 'total': total,
                 'sequences': sequences,
                 'links': links}
            tempDF = pd.DataFrame(d)
            writer = pd.ExcelWriter('{}interim/prophagesbyaccnum.xlsx'.format(os.getenv('MAIN_PATH')), engine = 'xlsxwriter') # pylint: disable=abstract-class-instantiated
            tempDF.to_excel(writer, sheet_name = 'Sheet1', index = False)
            writer.save()

    time.sleep(4)
    bot.close()
    bot.quit()

    tempDF = pd.DataFrame({'accession numbers': accnum,
                    'intact': intact,
                    'questionable': question,
                    'incomplete': incomplete,
                    'total': total,
                    'sequences': sequences,
                    'links': links})

    writer = pd.ExcelWriter('{}interim/prophagesbyaccnum.xlsx'.format(os.getenv('MAIN_PATH')), engine = 'xlsxwriter') # pylint: disable=abstract-class-instantiated
    tempDF.to_excel(writer, sheet_name = 'Sheet1', index = False)
    writer.save()
    