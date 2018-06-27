#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created by Ferreira Javier Zambrano on 2018-06-23.
Copyright (c) 2018 - All rights reserved.
"""

from bs4 import BeautifulSoup
import logging
import logging.config
from os import path, getcwd

# read logger config
logging.config.fileConfig(path.join(getcwd(), 'logging.conf'))
# create logger
logger = logging.getLogger('crawler')

def extract_xml_inputs(content):
    try:
        url_to_visits = []
        soup = BeautifulSoup(content, 'xml')
        urls = soup.find_all('url')
        for url in urls:
            loc = url.find('loc')
            url_to_visits.append(loc.get_text())
        return url_to_visits
    except:
        raise


def extract_urls(page):
    # main-ad-list
    soup = BeautifulSoup(page, 'html.parser')
    ul = soup.find_all(id='main-ad-list')
    items = ul[0].find_all('li', class_='item')
    urls = []
    for item in items:
        tag_a = item.find_all('a')
        if (len(tag_a) > 0):
            url = tag_a[0]['href']
            urls.append(url)
    return urls

