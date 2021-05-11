#!/usr/bin/env python3

import os
from dotenv import load_dotenv

if __name__ == '__main__':

    load_dotenv()
    
    loc = '{}main/fastafiles'.format(os.getenv('MAIN_PATH'))
    l = os.listdir(loc)
    
    for i in l:
        print(i)
        f = open('{}/{}'.format(loc, i), 'r')
        text = f.read()
        newF = open('{}mainSecond/fastafiles/{}.fasta'.format(os.getenv('MAIN_PATH'), i.split('.')[0]), 'w+')
        newF.write(text)
        f.close()
        newF.close()
