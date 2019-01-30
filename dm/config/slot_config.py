#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 15:24:12 2019

@author: wj
"""

class config:
    def __init__(self,
                 is_filling=False,
                 is_confirm=False,
                 is_queriable=False,
                 is_retainable=False,
                 is_guided=False,
                 is_default=False,
                 is_multiValue=False
                 ):
        self.is_filling=is_filling #是否需要填充
        self.is_confirm=is_confirm #若slot有值，是否通过交互让用户确认此信息（需要提供确认模板）
        self.is_queriable=is_queriable #是否进行查询，slot填充后，是否要进行查询（需要提供查询接口）
        self.is_retainable=is_retainable #是否保存到下一轮会话
        self.is_guided=is_guided #是否需要引导用户（需要提供引导模板）
        self.is_default=is_default #是否需要填充默认值（需要提供默认值接口）
        self.is_multiValue=is_multiValue #是否允许多个值，若允许，需要提供处理函数，若不允许，每次只取第一个词语
        
        
        