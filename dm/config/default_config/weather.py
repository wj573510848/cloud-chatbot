#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 15:19:01 2019
@author: wj
"""
from dm.config import slot_config
from dm.dm_models import slot_confirm
class query:
    def __init__(self):
        self.essential_slots=['city'] #必须的slot，优先级从前到后
        self.all_slots=['province','city','district','time'] #接受的slot，不在里面的slot将会忽略
        #is_filling=False,
        #is_confirm=False,
        #is_queriable=False,
        #is_retainable=False,
        #is_guided=False
        #is_default=False,
        #is_multiValue=False
        self.slot_config={
                'city':slot_config.config(True,True,False,True,True),
                'province':slot_config.config(is_default=True),
                'time':slot_config.config(is_default=True,is_multiValue=True),
                }
        #confirm,queriable可自定义函数
        self.slot_function_config={
                'city':self.confirm_fn()
                }
    def get_default_slot_config(self):
        return slot_config.config(False,False,False,False,False)
    def confirm_fn(self,**kwargs):
        def c(user_profile,cur_nlg,task,logger):
            return slot_confirm(user_profile,cur_nlg,task,logger,**kwargs)
        return c
            
        