#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 16:27:36 2019

@author: wj
"""
import logging
import random
import re

def get_default_dialog_state():
    #默认的对话状态
    return {
            'task':'',
            'session_counts':0,
            'nlg_res':{
                    'type':'text', #text:文本输出
                    'answer':'',
                    },
            'dialog_type':'',
            'retry':0
            }
def default_multivalue_process(value_list,multi_allowed):
    if isinstance(value_list,list):
        if multi_allowed:
            return ",".join(value_list)
        else:
            return value_list[0]
    else:
        return value_list

class slot_confirm:
    '''
    slot“确认”对话逻辑
    '''
    def __init__(self,user_profile,cur_nlg,task,logger=None,**kwargs):
        '''
        multi_value_fn:处理多个值的函数
        '''
        self.task=task
        self.logger=logger if logger is not None else logging
        self.user_profile=user_profile
        self.cur_nlg=cur_nlg
        self.multi_value_fn=kwargs.get('multi_value_fn',default_multivalue_process)
        
        self.update()
    def update(self):
        state=self.user_profile.user_state
        #如果是第一轮，进行确认
        #对话level提升
        #进入次级对话
        if state['dialog_level']==0:
            self.logger.info("comfirm dialog starting...")
            state['dialog_level']=1
            state['sub_dialog']=get_default_dialog_state()
            state['sub_dialog']['session_counts']+=1
            state['sub_dialog']['dialog_type']='confirm'
            state['sub_dialog']['nlg_res']['type']='text'
            state['sub_dialog']['task']=self.task
            value=state['outputs']['slot_values'][self.task]
            multi_allowed=state['config']['slot_config'][self.task]['is_multiValue']
            value=self.multi_value_fn(value,multi_allowed)
            answer=self.cur_nlg.nlg_config.slot_nlg[self.task]['confirm']['query']
            answer=random.choice(answer)
            answer=re.sub("<slot/>",value,answer)
            state['sub_dialog']['nlg_res']['answer']=answer
        else:
            domain=self.user_profile.domain_name
            intent=self.user_profile.intent_name
            state['sub_dialog']['session_counts']+=1
            if domain=='control' and intent=='yes':
                pass
                
        #如果是yes，no
        #elif state['dialog_level']==1:
        #    pass
            
class  exception:
    def __init__(self,user_profile,cur_nlg,logger=None,**kwargs):
        self.logger=logger if logger is not None else logging
        self.user_profile=user_profile
        self.cur_nlg=cur_nlg       
        self.update()
    def update(self):
        state=self.user_profile.user_state
        state['sub_dialog']=get_default_dialog_state()
        state['sub_dialog']['task']='exception'
        state['sub_dialog']['session_counts']+=1
        state['sub_dialog']['nlg_res']['type']='text'
        #['action_type'] not in ['Error','NoTemplate','OutDefinition']
        try:
            if state['action_type']=='NoTemplate':
                pass
            if state['action_type']=='Error':
                answer=self.cur_nlg.nlg_config.global_nlg['Error']
                answer=random.choice()
            pass
    