#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created by Ferreira Javier Zambrano on 2018-06-23.
Copyright (c) 2018 - All rights reserved.
"""

import argparse
from textwrap import dedent
import requests
from os import path, getcwd, environ
from requests import RequestException
import sys
from time import sleep, time
import logging
import logging.config
from dotenv import load_dotenv, find_dotenv
from extract_urls import extract_xml_inputs, extract_urls
from urls_db import Storage

# read logger config
logging.config.fileConfig(path.join(getcwd(), 'logging.conf'))
# create logger
logger = logging.getLogger('crawler')

storage = Storage()
DIR_DATASET = ''
TIME_DEFAULT = 10


def print_header(url, method):
    logger.info('\nrequesting...')
    header = dedent('''
    ==============================
    METHOD: {method}
    URL REQUEST: {url}
    =============================='''.format(method=method, url=url))
    logger.info(header)


def print_response(r):
    if r is not None:
        if (r.status_code >= 200 and r.status_code <= 299):
            logger.info('Request Success')
        else:
            logger.error('Request Fail')
            logger.error('Header Status CODE: {code}'.format(code=r.status_code))
    else:
        logger.error('request response is None')
    try:
        logger.info(
            'Content-Type: {content}'.format(content=r.headers['Content-Type']))
    except:
        logger.error('Content-Type was not correct')



def do_request(url, method='GET'):
    print_header(url, method)
    try:
        r = requests.get(url)
        return r
    except ConnectionError as con:
        logger.error('Connection to {url} was not possible'.format(url=url))
        logger.error("Stack of error: {0}".format(con))
    except RequestException as req:
        logger.error('Connection to {url} was not possible'.format(url=url))
        logger.error("Stack of error: {0}".format(req))
    except:
        logger.error('Error unkown', 'red')
        logger.error("Unexpected error:", sys.exc_info()[0])
        raise


def is_visited(url):
    status = False
    logger.info(storage.get(url))
    if (storage.get(url) is not None):
        status = True
    return status


def get_filename():
    filename_sux = int(time())
    return 'document_{number}.html'.format(number=filename_sux)


def save_page(content, filename):
    path_to_file = '{dir}/{filename}'.format(dir=DIR_DATASET, filename=filename)
    logger.info(path_to_file)
    with open(path_to_file, 'wb') as page:
        page.write(content)


def get_page(urls):
    for url in urls:
        if (not is_visited(url)):
            response = do_request(url)
            print_response(response)
            storage.save(url, {'visited': True})
            if (response is not None and response.status_code == 200):
                filename = get_filename()
                logger.info('Saving page: {page}'.format(page=filename))
                save_page(response.content, filename)
                storage.save(filename,url)
            sleep(TIME_DEFAULT)
        else:
            logger.info('URL {url} was visited before'.format(url=url)) 


def crawling(urls_entry_points):
    COUNT_PAGES_TO_VISITED = len(urls_entry_points)
    for url_to_visit in urls_entry_points:
        logger.info('Entry points to visited: {number}'.format(number=str(COUNT_PAGES_TO_VISITED)))
        if (not is_visited(url_to_visit)):
            response = do_request(url_to_visit)
            print_response(response)
            storage.save(url_to_visit, {'visited': True})
            if (response is not None and response.status_code == 200):
                urls_pages = extract_urls(response.content)
                get_page(urls_pages)
            # sleep(TIME_DEFAULT)
        else:
            logger.info('URL {url} was visited before'.format(url=url_to_visit))
        COUNT_PAGES_TO_VISITED -= 1


def entry_points(urls):
    PREFIX = environ.get('URL_PREFIX')
    for url in urls:
        url = '{prefix}{url}'.format(prefix=PREFIX, url=url)
        response = do_request(url)
        print_response(response)
        if (response is not None):
            urls_to_visit = extract_xml_inputs(response.content)
            crawling(urls_to_visit)


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    DIR_DATASET = environ.get('DIR_DATASET')
    TIME_DEFAULT = int(environ.get('TIME_DEFAULT'))
    # DEFINITION OF ARGUMENTS
    parser =  argparse.ArgumentParser(prog='crawler', formatter_class=argparse.RawDescriptionHelpFormatter, description=dedent('''Crawler OLX.
            HAPPY END TESTS
    '''), epilog="And that's how your life is became Cold Toddynho", usage='%(prog)s [options]')
    parser.add_argument('--version', '-v', action='version',
                        version='%(prog)s 0.0.1')
    parser.add_argument('--url',  nargs=1, required=False,
                        help='URL')
    args = parser.parse_args()
    entry_points(['sitemap1.xml'])
