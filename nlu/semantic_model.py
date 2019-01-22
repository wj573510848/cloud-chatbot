#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""
from nlu.domain_chat import in_domain_model
from nlu.open_chat.match_based_qa import chat_model

class semantic:
    def __init__(self,word_level_encoder,char_level_encoder,tokenizer,logger):
        self.logger=logger
        self.domain_chat=in_domain_model(word_level_encoder,char_level_encoder,logger)
        self.open_chat=chat_model(tokenizer)
    
    def get_task_results(self,sentence,domain=None,intent=None):
        try:
            if domain is not None and intent is not None:
                self.logger.info("use in domain semantic...")
                return self.domain_chat.domain_predict(sentence,domain,intent)
            else:
                self.logger.info("use top domain semantic...")
                return self.domain_chat.normal_predict(sentence)
        except:
            self.logger.info("Something run during run task model. Sentence:{}".format(sentence))
            return {'domain':'null','intent':'null','slots':[]}
    def get_open_chat_results(self,sentence,default_answer="对不起，我还不明白你的意思。"):
        self.logger.info("use open chat ...")
        try:
            return self.open_chat.response(sentence,default_answer=default_answer)
        except:
            self.logger.info("Something wrong during run open chat. Sentence:{}".format(sentence))
            return default_answer
        