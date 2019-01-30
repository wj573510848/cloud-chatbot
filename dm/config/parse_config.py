#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 16:38:54 2019
@author: wj
将slot filling配置信息解析为标准格式
1.filling_slots 当前需要填充的slot，若为空，表明slot filling任务结束
2.all_slots 可接受填充的slot
3.slot配置{'slot_name':{}}
is_filling
is_confirm
is_queriable
is_retainable
is_guided
is_default
4.slot_value slot的值
5.process_quene 等待处理的slot队列
"""
import logging
from dm.config import default_config as default_cfg

project_config={
        #'project_name':P(domain,intent)
        }
default_config={
        'weather_query':default_cfg.weather.query
        }

default_config_params={
        'filling_slots':[],
        'all_slots':[],
        'slot_config':{},
        'slot_values':{},
        'process_quene':[],
        }
def parse_slot_property(slot_cfg_cls):
    p= {
            'is_filling':slot_cfg_cls.is_filling,
            'is_confirm':slot_cfg_cls.is_confirm,
            'is_queriable':slot_cfg_cls.is_queriable,
            'is_retainable':slot_cfg_cls.is_retainable,
            'is_guided':slot_cfg_cls.is_guided,
            'is_default':slot_cfg_cls.is_default,
            'is_multiValue':slot_cfg_cls.is_multiValue
            }
    return p
def parse(project_name,domain,intent,logger=logging):
    cfg_key=domain+'_'+intent
    cfg_fun=project_config.get(project_name,None)
    if cfg_fun is None:
        logging.warning("can't find project config for {}-{},use default.".format(domain,intent))
        cfg_fun=default_config.get(cfg_key,None)
    else:
        cfg_fun=cfg_fun.get(cfg_key,None)
    if cfg_fun is None:
        logging.warning("can't find config information for {}-{}-{}".format(project_name,domain,intent))
        return {}
    cfg=cfg_fun()
    filling_slots=cfg.essential_slots
    all_slot_list=cfg.all_slots
    slot_config={}
    for slot_name in all_slot_list:
        if slot_name in cfg.slot_config:
            slot_config[slot_name]=parse_slot_property(cfg.slot_config[slot_name])
        else:
            logging.warning("can't find slot '{}''s config, use default.".format(slot_name))
            slot_config[slot_name]=parse_slot_property(cfg.get_default_slot_config())
    config_params={
        'filling_slots':filling_slots,
        'all_slots':all_slot_list,
        'slot_config':slot_config,
        'slot_values':{},
        'process_quene':[],
        }
    return config_params