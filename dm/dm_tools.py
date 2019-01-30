#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 18:14:23 2019

@author: wj
"""
import redis
import datetime

def get_redis_client(host='localhost',port=6379,db=0):
    pool = redis.ConnectionPool(host=host, port=port, db=db)
    client=redis.StrictRedis(connection_pool=pool)
    return client

def parse_input_data_normal(input_data):
    '''
    将输入转化为标准格式
    '''
    res_data={}
    res_data['nlu_input']=input_data['nlu_input']
    res_data['open_qa']=input_data['open_qa']
    return res_data
def default_location():
    '''
    获取默认的地址
    '''
    return {
            'province':'上海',
            'city':'上海',
            'district':'浦东新区',
            }
def default_time():
    now=datetime.datetime.now()
    return {
            'year':now.year,
            'month':now.month,
            'day':now.day,
            'hour':now.hour,
            'minute':now.minute,
            'second':now.second
            }
def default_info():
    loc=default_location()
    time=default_time()
    res={}
    res.update(loc)
    res.update(time)
    return res    