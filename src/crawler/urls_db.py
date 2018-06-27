#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created by Ferreira Javier Zambrano on 2017-03-09.
Copyright (c) 2017 datarisk.io - All rights reserved.
"""

import redis
import os
from dotenv import load_dotenv, find_dotenv
import time
import sys
import json


class Storage():

    host = ''
    port = ''

    def __init__(self):
        load_dotenv(find_dotenv())
        self.host = os.environ.get('REDIS_SERVER_HOST')
        self.port = os.environ.get('REDIS_SERVER_PORT')


    def get_connection(self):
        try:
            pool = redis.ConnectionPool(host=self.host, port=self.port)
            return redis.Redis(connection_pool=pool)
        except:
            return None


    def save(self, key, obj):
        r = self.get_connection()
        try:
            return r.set(key, json.dumps(obj))
        except:
            return False


    def get(self, key):
        r = self.get_connection()
        try:
            obj = r.get(key)
            #return normalize str as JSON
            if (obj is not None):
                return json.loads(obj)
            else:
                return None
        except:
            print("Unexpected error:", sys.exc_info())
            return None


    def delete(self, key):
        r = self.get_connection()
        try:
            r.delete(key)
            return True
        except:
            return False
