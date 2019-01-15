#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: wj573510848@126.com
"""

from utils import basic_log
from utils import basic_config

config=basic_config.config()
logger=basic_log.get_logger('chatbot',config.log_file)
logger.info("Starting...")
