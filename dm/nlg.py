#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 14:12:19 2019

@author: wj
"""
from dm.config import nlg_config
import logging
import traceback
class nlg:
    def __init__(self,project,user_profile,**kwargs):
        self.project_name=project
        self.user_profile=user_profile
        self.logger=kwargs.get('logger',logging)
        self._load_nlg_config()
    
    @property
    def domain(self):
        return self.user_profile.domain_name
    @property
    def intent(self):
        return self.user_profile.intent_name
    def _load_nlg_config(self):
        self.nlg_status=True
        try:
            key_word01=self.project_name+"_"+self.domain+"_"+self.intent
            key_word02=self.domain+"_"+self.intent
            if key_word01 in nlg_config.nlg_config_models:
                self.nlg_config=nlg_config.nlg_config_models[key_word01]
                self.logger.info("Load nlg config from project config.")
            else:
                self.nlg_config=nlg_config.nlg_config_models[key_word02]
                self.logger.info("Load nlg config from default config.")
        except:
            traceback.print_exc()
            self.nlg_status=False
            self.user_profile.set_error_state()
            self.logger.error("Cant find nlg config.")