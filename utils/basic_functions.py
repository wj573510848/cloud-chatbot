#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 17:06:50 2019

@author: wj
"""
import os
import pymongo

Basic_Digits={
        '一':'1',
        '二':'2',
        '三':'3',
        '四':'4',
        '五':'5',
        '六':'6',
        '七':'7',
        '八':'8',
        '九':'9',
        '零':'0',
        '幺':'1'
        }
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
def get_root_dir():
    #获取项目的根目录
    cur_dir=os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(cur_dir)
def to_arabic_numerals(sentence):
    '''
    将文本中的中文数字转化为阿拉伯数字
    '''
    new_sentence=[]
    for i in sentence:
        if i in Basic_Digits:
            new_sentence.append(Basic_Digits[i])
        else:
            new_sentence.append(i)
    return "".join(new_sentence)
    