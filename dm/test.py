#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: wj
1.获取用户上一轮的信息
2.在0级交互中，做出以下判断
* 是否在异常状态，如果是，直接nlg（status!=3）
* 
3.逻辑
*在最外层的时候，进行slot值的填充，并且更新状态，建立子对话候选序列
"""
import sys
sys.path.append("../")

import json
from dm.profile.user_profile import profile as user_profile
from dm import dm_tools
from dm.nlg import nlg as nlg_template
import collections
import logging
class dm:
    def __init__(self):
        pass
    
    def update(self,input_res,project_name,user_name,*args, **kwargs):
        '''
        parameters:
            input_res:语义解析结果
            project_name:项目名
            user_name:用户名（项目名+用户名必须是唯一的，将作为用户的唯一标识）
            default_fun:获取默认值的函数
        '''
        self.logger=kwargs.get('logger',logging)
        #初始化用户状态
        cur_user_profile=user_profile(input_res,project_name,user_name,*args, **kwargs)
        #获取默认值
        if cur_user_profile.user_state['action_type'] not in ['Error','NoTemplate','OutDefinition']:
            cur_nlg=nlg_template(project_name,cur_user_profile,**kwargs)
            if cur_nlg.nlg_status:
                if cur_user_profile.user_state['dialog_level']==0:
                    if cur_user_profile.user_state['action_type']=='normal':
                        self.do_slot_check(cur_user_profile)
                self.do_nlg(cur_user_profile,cur_nlg)
        print(json.dumps(cur_user_profile.user_state))
    def do_slot_check(self,user_profile):
        #根据输入的slot更新对话状态
        slot_value_list=collections.defaultdict(set)
        for i in user_profile.user_state['inputs']['nlu']['nlu']['slots']:
            if i['name'] not in user_profile.user_state['config']['all_slots']:
                self.logger.warning("Slot '{}' not in defination.".format(i['name']))
                continue
            slot_value_list[i['name']].add(i['regValue'])
        for key in slot_value_list:
            #替换原有值
            #是不是filling
            if key in user_profile.user_state['outputs']['filling_slots']:
                self.logger.info("{} is filling".format(key))
                user_profile.user_state['outputs']['filling_slots'].remove(key)
            #填充slot值
            user_profile.user_state['outputs']['slot_values'][key]=list(slot_value_list[key])
            #检查是否需要进行对话
            slot_config=user_profile.user_state['config']['slot_config'][key]
            if slot_config['is_confirm'] or slot_config['is_queriable']:
                if key not in user_profile.user_state['outputs']['quene']:
                    user_profile.user_state['outputs']['quene'].append(key)
                self.logger.info("add {} to dialog quene!".format(key))
    def do_nlg(self,user_profile,cur_nlg):
        state=user_profile.user_state
        if state['dialog_level']==0:
            #判断是否有对话任务
            if len(state['outputs']['quene'])>0:
                task=a.pop()
                #进入对话任务
            else:
                if len(state['outputs']['filling_slots'])>0:
                    pass
        if state['dialog_level']==1:
            pass
                
if __name__=="__main__":
    model=dm()
    inputs={'nlu':
        {'domain':'weather',
         'intent':'query',
         'slots':[
                 {'name':'city','regValue':'上海'},
                 {'name':'province','regValue':'上海'}
                 ]}}
    model.update(inputs,'','weather','query')