#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: wj
nature language generation
"""
'''
confirm对话逻辑:
例子：
正常逻辑：
--请问你要选择“XXX”吗--query
--是/否
--好的，已经选择/好的，已经取消
--非正常情况
1.跨领域
2.领域内
3.其他--retry--我还不明白你的意思，你可以说是或者否
4.继续其他--闲聊
'''
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
                'guide':['请问你要查询哪里的天气'],
                'error_exit':['我还不理解，先退出了']
                    }
        self.slot_nlg={
                'city':{'confirm':
                    {
                            'query':['确认需要查询“<slot/>”的天气吗?'],     
                            'retry':['我还不明白你的意思，您可以说是或者否'],
                            'yes':['好的，将“<slot/>”设置为城市'],
                            'no':['好的，已取消']
                     },
                        'guide':['您要查哪个城市的天气'],
                        }
                
                
                }
nlg_config_models={
        'weather_query':default_weather_query()
        }
