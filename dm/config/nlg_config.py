#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: wj
nature language generation
"""

class default_config:
    def __init__(self):
        #与user profile中的action_type对应
        self.global_nlg={
                'Error':["<BotName>逻辑好像有点错误。"],
                'NoTemplate':['<BotName>还在努力学习这个技能'],
                'OutDefinition':['<BotName>还在努力学习这个技能'],
                'guideReply':[]
                    }
        self.slot_nlg={}

class default_weather_query:
    def __init__(self):
        self.global_nlg={
                'Error':["<BotName>逻辑好像有点错误。"],
                'NoTemplate':['<BotName>还在努力学习这个技能'],
                'OutDefinition':['<BotName>还在努力学习这个技能'],
                'guide':['请问你要查询哪里的天气']
                    }
        self.slot_nlg={
                'city':{'confirm':['确认需要查询<city/>的天气吗'],
                        'guide':['您要查哪个城市的天气']
                        }
                
                
                }
nlg_config_models={
        'weather_query':default_weather_query()
        }