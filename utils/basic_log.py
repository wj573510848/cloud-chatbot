#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: wj573510848@126.com
"""
import logging

def get_logger(logger_name,log_file,formatter=None,log_level=logging.INFO):
    logger=logging.getLogger(logger_name)
    logger.setLevel(log_level)
    fh=logging.FileHandler(log_file)
    ch=logging.StreamHandler()
    if formatter is None:
        formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    else:
        formatter=logging.Formatter(formatter)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger