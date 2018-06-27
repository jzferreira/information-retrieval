#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created by Ferreira Javier Zambrano on 2018-06-26.
Copyright (c) 2018 - All rights reserved.
"""
import argparse
from html.parser import HTMLParser
from os import listdir, makedirs, path, getcwd
from pathlib import Path
# read logger config
logging.config.fileConfig(path.join(getcwd(), 'logging.conf'))
# create logger
logger = logging.getLogger('ir')

#https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def open_collections(dataset_path):
    dataset_dir = Path(dataset_path)
    if (dataset_dir.is_dir()):
        files = listdir(dataset_dir)
        for f in files:
            print(f)

if __name__ == '__main__':
    load_dotenv(find_dotenv())
    DIR_DATASET = environ.get('DIR_DATASET')
    # DEFINITION OF ARGUMENTS
    parser =  argparse.ArgumentParser(prog='information retrieval', formatter_class=argparse.RawDescriptionHelpFormatter, description=dedent('''Crawler OLX.
            HAPPY END TESTS
    '''), epilog="And that's how your life is became Cold Toddynho", usage='%(prog)s [options]')
    parser.add_argument('--version', '-v', action='version',
                        version='%(prog)s 0.0.1')
    args = parser.parse_args()
    open_collections(DIR_DATASET)
