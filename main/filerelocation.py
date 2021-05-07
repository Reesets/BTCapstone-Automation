#!/usr/bin/env python3

import os
from dotenv import load_dotenv

if __name__ == '__main__':
    
    load_dotenv()

    l = os.listdir('{}main/intactphages'.format(os.getenv('MAIN_PATH')))
    for i in l:
        try:
            os.rename('{}main/intactphages/{}/IP.fna'.format(os.getenv('MAIN_PATH'), i),
                      '{}main/intactphages/{}.fna'.format(os.getenv('MAIN_PATH'), i))
        except:
            pass
                  