#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 17:06:50 2019

@author: wj
"""

import pymongo

def get_mongo_db():
    client=pymongo.MongoClient('127.0.0.1')
    db=client.chatDb
    return db

def read_lines(file,encoding='utf8'):
    with open(file,'r',encoding=encoding) as f:
        for line in f:
            line=line.strip()
            if line:
                yield line