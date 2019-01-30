#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: wj
用户画像
对用户在一个对话回合内的行为建模
input_res:{'nlu':{'domain':'','intent':'','slots':[]},'qa':[qa1,qa2]}
1.用户id:project_name+user_name
2.更新用户状态
首次：
* 加载配置，得到三种状态，0:解析错误，1:找不到模块，即nlu语义不为null，但是找不到配置，2:定义外语义，即null，3:正常
* 对话层级为0时，更新slot值
3.action type
* Error 程序内部错误
* NoTemplate 没有模板错误
* OutDefinition 定义外
* normal 正常

4.dialog_level 对话所在层级
0:root层，需要进行slot填充
"""

import copy
import logging
from dm import dm_tools
from dm.config import parse_cfg
import traceback

class profile:
    def __init__(self,input_res,project_name,user_name,*args, **kwargs):
        self.logger=kwargs.get('logger',logging)
        self.input_res=input_res
        self.project_name=project_name
        self.user_id=project_name+"_"+user_name
        self.redis_client=dm_tools.get_redis_client()
        self._get_cur_user_state(project_name,user_name)
    
    
    
    def _get_default_user_state(self):
        #1.解析domain intent
        #2.根据project name，domain，intent得到该场景下的对话配置
        default_user_state={
        'user_info':{
                'id':self.user_id,
                },
        'config':{                                  
                },
        'action_type':'normal',
        'dialog_level':0,
        'inputs':{},
        'outputs':{}, #
        'status':0 ,#0:内部错误，1:找不到domain模板，2:定义外语义
        'session_id':0,
        'session_counts':0
        }
        try:#解析nlu结果
            domain=self.input_res['nlu']['domain']
            intent=self.input_res['nlu']['intent']
        except:
            domain=None
        if domain is None:
            self.logger.error("Parse input data: Failed! Can't build user profile!")
            default_user_state['status']=0
        else:
            if domain=='null':
                self.logger.info("Parse input data: domain is 'null'")
                default_user_state['status']=2
            else:
                try:
                    basic_config=parse_cfg(self.project_name,domain,intent,self.logger)
                    basic_config['domain']=domain
                    basic_config['intent']=intent
                    default_user_state['config']=basic_config
                    if len(basic_config)<3:
                        self.logger.error("Parse input data: domain '{}',intent '{}'. Can't find config infomation.".format(domain,intent))
                        default_user_state['status']=1
                    else:
                        self.logger.info("Parse input data: Success! domain '{}',intent '{}'".format(domain,intent))
                        default_user_state['status']=3
                except:
                    self.logger.error("Something wrong during get user config. Please check!")
                    default_user_state['status']=0
        default_user_state['outputs']=copy.deepcopy(default_user_state['config'])
        default_user_state['outputs']['quene']=[] #待处理事物
        #default_user_state['inputs']['nlu']=self.input_res
        return default_user_state
    def _get_cur_user_state(self,project_name,user_name):
        '''
        获取上一轮的用户信息,若没有则新建
        '''
        self.user_state=self.redis_client.get(self.user_id)
        #如果没有用户信息，则新建
        if not self.user_state:
            self.logger.warning("'{}' information not found, build new one!".format(self.user_id))
            self.user_state=self._get_default_user_state()
        self._update_user_state_by_input()
    def _update_user_state_by_input(self):
        #初始化时更新对话信息
        self.user_state['inputs']={}
        self.user_state['inputs']['nlu']=self.input_res
        self.user_state['session_id']+=1
        self.user_state['session_counts']+=1
        if self.user_state['status']==0:
            self.user_state['action_type']='Error'
        elif self.user_state['status']==1:
            self.user_state['action_type']='NoTemplate'
        elif self.user_state['status']==2:
            self.user_state['action_type']='OutDefinition'
        elif self.user_state['status']==3:
            if self.user_state['dialog_level']==0:
                self._slot_value_update()
        else:
            self.logger.error("Get action type failed!")
            self.user_state['action_type']='Error'
    def _slot_value_update(self):
        #填充slot信息
        self.logger.info("update slot value by nlu inputs")
        try:
            slot_infos=self.input_res['nlu']['slots']
            for slot_info in slot_infos:
                slot_name=slot_info['name']
                if slot_name not in self.user_state['config']['all_slots']:
                    self.logger.warning("slot '{}' not in defination.".format(slot_name))
                    continue
                reg_value=slot_info['regValue']
                self.logger.info("Update '{}' for '{}' ".format(reg_value,slot_name))
                self._update_one_slot_value(slot_name,reg_value)
        except:
            traceback.print_exc()
            self.logger.error("Parse nlu results failed!")
            self.user_state['action_type']='Error'
    def _update_one_slot_value(self,slot_name,slot_value):
        if slot_name not in self.user_state['outputs']['slot_values']:
            self.user_state['outputs']['slot_values'][slot_name]=[]
        if slot_value not in self.user_state['outputs']['slot_values'][slot_name]:
            self.user_state['outputs']['slot_values'][slot_name].append(slot_value)
    def set_error_state(self,status=0):
        #用户状态变为错误状态
        self.user_state['status']=0
        self.user_state['action_type']='Error'
        self.user_state['dialog_level']=0
    @property
    def domain_name(self):
        return self.user_state['config']['domain']
    @property
    def intent_name(self):
        return self.user_state['config']['intent']