#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: wj573510848@126.com
"""
import os

class config:
    def __init__(self):
        self.root_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.log_file=os.path.join(self.root_dir,'log/log.txt')