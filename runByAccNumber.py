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

    links = pickle.load(open('{}linklist.txt'.format(os.getenv('MAIN_PATH')), 'rb'))
    
    accNumbers = list(map(lambda x:x.split('/')[len(x.split('/')) - 1], links))

    intact = []
    question = []
    incomplete = []
    total = []
    sequences = []
    
    k = 0

    for acc in accNumbers:

        k+=1
        print('{}: {}'.format(k, acc))
        url = 'http://phaster.ca/submissions/{}'.format(acc)
        bot.get(url)
        time.sleep(5)
        a = bot.find_elements_by_xpath('.//tr[@class="intact"]')
        b = bot.find_elements_by_xpath('.//tr[@class="questionable"]')
        c = bot.find_elements_by_xpath('.//tr[@class="incomplete"]')
        intact.append(len(a))
        question.append(len(b))
        incomplete.append(len(c))
        total.append(len(a) + len(b) + len(c))
        
        dnas = []

        dnatext = bot.find_elements_by_xpath('.//tr[@class = "intact"]/td/a[@class = "modal-trigger"]')

        if len(dnatext) == 0:
            sequences.append(dnas)
            continue

        for i in dnatext:
            if 'sequence' not in i.get_attribute('href') and 'dna' in i.get_attribute('href'):
                dnaID = i.get_attribute('href').split('#')[1]
                i.click()
                for j in bot.find_elements_by_xpath('.//pre'):
                    if j.text != '':
                        dnas.append(j.text)
                bot.find_elements_by_xpath('.//div[@id = "' + dnaID + '"]/div[@class = "modal-footer"]/a[contains(text(),"Close")]')[0].click()
            
        sequences.append(dnas)

        df = pd.DataFrame({'accession numbers': accNumbers[:len(intact)],
                    'intact': intact,
                    'questionable': question,
                    'incomplete': incomplete,
                    'total': total,
                    'sequences': sequences,
                    'links': links[:len(intact)]})

        writer = pd.ExcelWriter('{}accessionnumbers.xlsx'.format(os.getenv('MAIN_PATH')), engine = 'xlsxwriter') # pylint: disable=abstract-class-instantiated
        df.to_excel(writer, sheet_name = 'Sheet1', index = False)
        writer.save()

    time.sleep(4)
    bot.close()
    bot.quit()

    df = pd.DataFrame({'accession numbers': accNumbers[:len(intact)],
                    'intact': intact,
                    'questionable': question,
                    'incomplete': incomplete,
                    'total': total,
                    'sequences': sequences,
                    'links': links[:len(intact)]})

    writer = pd.ExcelWriter('{}accessionnumbers.xlsx'.format(os.getenv('MAIN_PATH')), engine = 'xlsxwriter') # pylint: disable=abstract-class-instantiated
    df.to_excel(writer, sheet_name = 'Sheet1', index = False)
    writer.save()
    